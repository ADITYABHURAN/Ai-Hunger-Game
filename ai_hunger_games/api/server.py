"""
FastAPI server for AI Hunger Games web interface.
Provides REST API endpoints for running simulations and retrieving results.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import create_simulation
from config import NUM_AGENTS, NUM_ROUNDS, OLLAMA_MODEL, get_config


# Pydantic models for API
class SimulationConfig(BaseModel):
    """Configuration for starting a simulation."""
    num_agents: int = NUM_AGENTS
    num_rounds: int = NUM_ROUNDS
    model: str = OLLAMA_MODEL
    voting_method: str = "single-choice"
    questions: Optional[List[str]] = None


class SimulationStatus(BaseModel):
    """Status of a running simulation."""
    status: str  # "idle", "running", "completed", "error"
    current_round: int = 0
    total_rounds: int = 0
    message: str = ""


# Global state
app = FastAPI(
    title="AI Hunger Games API",
    description="REST API for multi-agent evolution simulation",
    version="1.0.0"
)

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulation state
current_simulation = None
simulation_status = SimulationStatus(status="idle", message="No simulation running")
simulation_results = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AI Hunger Games API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "config": "/config",
            "start": "/simulation/start",
            "status": "/simulation/status",
            "results": "/simulation/results",
            "logs": "/simulation/logs"
        }
    }


@app.get("/config")
async def get_config_endpoint():
    """Get current configuration."""
    return get_config()


@app.post("/simulation/start")
async def start_simulation(
    config: SimulationConfig,
    background_tasks: BackgroundTasks
):
    """
    Start a new simulation.
    
    Args:
        config: Simulation configuration
        background_tasks: FastAPI background tasks
        
    Returns:
        Status message
    """
    global simulation_status, current_simulation, simulation_results
    
    if simulation_status.status == "running":
        raise HTTPException(
            status_code=400,
            detail="A simulation is already running"
        )
    
    # Reset state
    simulation_results = None
    simulation_status = SimulationStatus(
        status="running",
        current_round=0,
        total_rounds=config.num_rounds,
        message="Simulation starting..."
    )
    
    # Run simulation in background
    background_tasks.add_task(
        run_simulation_background,
        config
    )
    
    return {
        "message": "Simulation started",
        "config": config.dict()
    }


def run_simulation_background(config: SimulationConfig):
    """
    Run simulation in background.
    
    Args:
        config: Simulation configuration
    """
    global simulation_status, current_simulation, simulation_results
    
    try:
        # Create simulation
        sim = create_simulation(
            num_agents=config.num_agents,
            num_rounds=config.num_rounds,
            model=config.model,
            voting_method=config.voting_method,
            verbose=False
        )
        
        current_simulation = sim
        
        # Run simulation
        results = sim.run_simulation(config.questions)
        
        simulation_results = results
        simulation_status = SimulationStatus(
            status="completed",
            current_round=config.num_rounds,
            total_rounds=config.num_rounds,
            message="Simulation completed successfully"
        )
        
    except Exception as e:
        simulation_status = SimulationStatus(
            status="error",
            message=f"Simulation failed: {str(e)}"
        )


@app.get("/simulation/status")
async def get_simulation_status():
    """Get current simulation status."""
    return simulation_status


@app.get("/simulation/results")
async def get_simulation_results():
    """Get simulation results (only available when completed)."""
    if simulation_status.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Simulation not completed yet"
        )
    
    if simulation_results is None:
        raise HTTPException(
            status_code=404,
            detail="No results available"
        )
    
    return simulation_results


@app.get("/simulation/logs")
async def get_simulation_logs():
    """Get list of available simulation logs."""
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        return {"logs": []}
    
    log_files = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.json') and filename.startswith('simulation_'):
            filepath = os.path.join(data_dir, filename)
            log_files.append({
                "filename": filename,
                "path": filepath,
                "size": os.path.getsize(filepath),
                "modified": os.path.getmtime(filepath)
            })
    
    # Sort by modified time (newest first)
    log_files.sort(key=lambda x: x['modified'], reverse=True)
    
    return {"logs": log_files}


@app.get("/simulation/logs/{filename}")
async def get_log_file(filename: str):
    """
    Get contents of a specific log file.
    
    Args:
        filename: Name of the log file
        
    Returns:
        Log file contents
    """
    filepath = os.path.join("data", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Log file not found"
        )
    
    if not filename.endswith('.json'):
        raise HTTPException(
            status_code=400,
            detail="Only JSON log files are supported"
        )
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading log file: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Start the FastAPI server.
    
    Args:
        host: Host to bind to
        port: Port to listen on
    """
    print("="*60)
    print("🚀 Starting AI Hunger Games API Server")
    print("="*60)
    print(f"\nServer running at: http://{host}:{port}")
    print(f"API documentation: http://{host}:{port}/docs")
    print(f"Interactive API: http://{host}:{port}/redoc")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import sys
    from config import API_HOST, API_PORT
    
    # Parse command-line arguments
    host = API_HOST
    port = API_PORT
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    start_server(host, port)
