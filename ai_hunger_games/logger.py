"""
Logger module for AI Hunger Games.
Handles JSON and CSV export of simulation data.
"""

import json
import csv
import os
from typing import Dict, List, Any
from datetime import datetime
from config import LOG_DIR, LOG_FILE, CSV_FILE


class SimulationLogger:
    """
    Logs all simulation data for analysis and replay.
    
    Outputs:
    - JSON: Complete simulation history with all details
    - CSV: Tabular data for easy analysis in spreadsheets
    """
    
    def __init__(self, log_dir: str = LOG_DIR):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to save log files
        """
        self.log_dir = log_dir
        self.simulation_data: Dict[str, Any] = {
            "metadata": {},
            "config": {},
            "rounds": [],
            "agents": [],
            "evolution_history": [],
            "final_stats": {}
        }
        
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
    
    def initialize_log(self, config: Dict[str, Any]) -> None:
        """
        Initialize the log with metadata and configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.simulation_data["metadata"] = {
            "simulation_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        self.simulation_data["config"] = config
    
    def log_round(
        self,
        round_num: int,
        question: str,
        answers: Dict[str, str],
        vote_results: Dict[str, Any],
        eliminated_agent: str,
        new_agent: Dict[str, Any],
        current_agents: List[Dict[str, Any]]
    ) -> None:
        """
        Log data from a single round.
        
        Args:
            round_num: Round number
            question: Question asked
            answers: Dictionary of agent answers
            vote_results: Voting results
            eliminated_agent: Name of eliminated agent
            new_agent: Dictionary representation of new agent
            current_agents: List of current agent dictionaries
        """
        round_data = {
            "round_number": round_num,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answers": answers,
            "vote_results": vote_results,
            "eliminated_agent": eliminated_agent,
            "new_agent": new_agent,
            "surviving_agents": [agent["name"] for agent in current_agents],
            "agent_count": len(current_agents)
        }
        
        self.simulation_data["rounds"].append(round_data)
    
    def log_agent(self, agent_dict: Dict[str, Any]) -> None:
        """
        Log an agent's complete information.
        
        Args:
            agent_dict: Dictionary representation of agent
        """
        # Check if agent already logged
        existing = [a for a in self.simulation_data["agents"] if a["name"] == agent_dict["name"]]
        
        if not existing:
            self.simulation_data["agents"].append(agent_dict)
        else:
            # Update existing agent data
            for i, a in enumerate(self.simulation_data["agents"]):
                if a["name"] == agent_dict["name"]:
                    self.simulation_data["agents"][i] = agent_dict
                    break
    
    def log_evolution_event(
        self,
        event_type: str,
        round_num: int,
        agent_name: str,
        details: Dict[str, Any]
    ) -> None:
        """
        Log an evolution event (elimination or creation).
        
        Args:
            event_type: "elimination" or "creation"
            round_num: Round number
            agent_name: Agent name
            details: Additional details
        """
        event = {
            "type": event_type,
            "round": round_num,
            "agent_name": agent_name,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        self.simulation_data["evolution_history"].append(event)
    
    def finalize_log(self, final_agents: List[Dict[str, Any]], stats: Dict[str, Any]) -> None:
        """
        Finalize the log with end-of-simulation data.
        
        Args:
            final_agents: List of surviving agents
            stats: Final statistics
        """
        self.simulation_data["metadata"]["end_time"] = datetime.now().isoformat()
        self.simulation_data["final_stats"] = stats
        self.simulation_data["final_agents"] = final_agents
    
    def save_json(self, filename: str = None) -> str:
        """
        Save simulation data to JSON file.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            sim_id = self.simulation_data["metadata"].get("simulation_id", "unknown")
            filename = f"simulation_{sim_id}.json"
        
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.simulation_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved JSON log to: {filepath}")
        return filepath
    
    def save_csv(self, filename: str = None) -> str:
        """
        Save simulation data to CSV file (round-by-round summary).
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            sim_id = self.simulation_data["metadata"].get("simulation_id", "unknown")
            filename = f"simulation_{sim_id}.csv"
        
        filepath = os.path.join(self.log_dir, filename)
        
        # Prepare CSV rows
        rows = []
        for round_data in self.simulation_data["rounds"]:
            row = {
                "Round": round_data["round_number"],
                "Question": round_data["question"][:100] + "...",
                "Eliminated": round_data["eliminated_agent"],
                "New Agent": round_data["new_agent"].get("name", "N/A"),
                "Agent Count": round_data["agent_count"]
            }
            
            # Add vote counts if available
            if "votes" in round_data["vote_results"]:
                for agent, votes in round_data["vote_results"]["votes"].items():
                    row[f"{agent}_votes"] = votes
            
            rows.append(row)
        
        if rows:
            # Write CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            print(f"💾 Saved CSV log to: {filepath}")
        
        return filepath
    
    def save_agents_csv(self, filename: str = None) -> str:
        """
        Save agent data to a separate CSV file.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            sim_id = self.simulation_data["metadata"].get("simulation_id", "unknown")
            filename = f"agents_{sim_id}.csv"
        
        filepath = os.path.join(self.log_dir, filename)
        
        agents = self.simulation_data["agents"]
        
        if agents:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    "name", "generation", "parent_name", "birth_round",
                    "votes_received", "votes_cast", "rounds_survived", "answers_given"
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(agents)
            
            print(f"💾 Saved agents CSV to: {filepath}")
        
        return filepath
    
    def save_all(self) -> Dict[str, str]:
        """
        Save all log formats.
        
        Returns:
            Dictionary with paths to all saved files
        """
        return {
            "json": self.save_json(),
            "csv": self.save_csv(),
            "agents_csv": self.save_agents_csv()
        }
    
    def print_summary(self) -> None:
        """Print a summary of logged data."""
        print("\n" + "="*60)
        print("📊 SIMULATION LOG SUMMARY")
        print("="*60)
        
        metadata = self.simulation_data["metadata"]
        print(f"\nSimulation ID: {metadata.get('simulation_id', 'N/A')}")
        print(f"Start Time: {metadata.get('start_time', 'N/A')}")
        
        if "end_time" in metadata:
            print(f"End Time: {metadata['end_time']}")
        
        print(f"\nTotal Rounds: {len(self.simulation_data['rounds'])}")
        print(f"Total Agents Tracked: {len(self.simulation_data['agents'])}")
        print(f"Evolution Events: {len(self.simulation_data['evolution_history'])}")
        
        if self.simulation_data.get("final_agents"):
            print(f"Final Survivors: {len(self.simulation_data['final_agents'])}")
            print("\nFinal Agent List:")
            for agent in self.simulation_data["final_agents"]:
                print(f"  - {agent['name']} (Gen {agent['generation']})")
        
        print("\n" + "="*60)
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get the complete simulation data.
        
        Returns:
            Complete simulation data dictionary
        """
        return self.simulation_data
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load simulation data from a JSON file.
        
        Args:
            filepath: Path to JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            self.simulation_data = json.load(f)
        
        print(f"📂 Loaded simulation data from: {filepath}")


def create_logger(log_dir: str = LOG_DIR) -> SimulationLogger:
    """
    Factory function to create a new logger.
    
    Args:
        log_dir: Directory for log files
        
    Returns:
        New SimulationLogger instance
    """
    return SimulationLogger(log_dir)
