"""
Configuration file for AI Hunger Games simulation.
"""

from typing import Dict, Any


# Ollama Configuration
OLLAMA_BASE_URL: str = "http://localhost:11434"
OLLAMA_MODEL: str = "llama2"  # Default model for all agents
OLLAMA_TIMEOUT: int = 120  # Timeout in seconds

# Simulation Configuration
NUM_AGENTS: int = 8
NUM_ROUNDS: int = 8
ALLOW_SELF_VOTING: bool = False

# Voting Configuration
VOTING_METHOD: str = "single-choice"  # Options: "single-choice", "ranked-choice"

# Evolution Configuration
MUTATION_RATE: float = 0.3  # Probability of adding mutations
MUTATION_TRAITS: list[str] = [
    "more analytical",
    "more creative",
    "more skeptical",
    "more optimistic",
    "more concise",
    "more detailed",
    "more humorous",
    "more serious",
    "more technical",
    "more philosophical",
    "more practical",
    "more abstract",
    "more empathetic",
    "more logical",
    "more intuitive"
]

# Logging Configuration
LOG_DIR: str = "data"
LOG_FILE: str = "simulation_log.json"
CSV_FILE: str = "simulation_results.csv"
VERBOSE: bool = True

# Predefined Questions (optional - can be overridden)
DEFAULT_QUESTIONS: list[str] = [
    "What is the most important quality for survival in a competitive environment?",
    "How should AI systems make ethical decisions?",
    "What is the meaning of intelligence?",
    "How can we solve climate change effectively?",
    "What makes a good leader?",
    "Should AI have rights?",
    "What is the future of human-AI collaboration?",
    "How do we balance innovation with safety?"
]

# Agent Memory Configuration
MAX_MEMORY_SIZE: int = 10  # Maximum number of memories to keep

# API Configuration (for optional web interface)
API_HOST: str = "0.0.0.0"
API_PORT: int = 8000


def get_config() -> Dict[str, Any]:
    """
    Returns the complete configuration as a dictionary.
    
    Returns:
        Dict[str, Any]: Complete configuration dictionary
    """
    return {
        "ollama": {
            "base_url": OLLAMA_BASE_URL,
            "model": OLLAMA_MODEL,
            "timeout": OLLAMA_TIMEOUT
        },
        "simulation": {
            "num_agents": NUM_AGENTS,
            "num_rounds": NUM_ROUNDS,
            "allow_self_voting": ALLOW_SELF_VOTING
        },
        "voting": {
            "method": VOTING_METHOD
        },
        "evolution": {
            "mutation_rate": MUTATION_RATE,
            "mutation_traits": MUTATION_TRAITS
        },
        "logging": {
            "log_dir": LOG_DIR,
            "log_file": LOG_FILE,
            "csv_file": CSV_FILE,
            "verbose": VERBOSE
        },
        "memory": {
            "max_size": MAX_MEMORY_SIZE
        },
        "api": {
            "host": API_HOST,
            "port": API_PORT
        },
        "default_questions": DEFAULT_QUESTIONS
    }
