"""
AI Hunger Games - Multi-Agent Evolution & Voting Simulator

A Python-based simulation where AI agents compete through answering questions,
voting on answers, and evolving over time using genetic algorithm principles.
"""

__version__ = "1.0.0"
__author__ = "AI Hunger Games Team"

from .agent import Agent
from .simulation import HungerGamesSimulation, create_simulation
from .llm_interface import LLMInterface, get_llm_interface
from .voting import VotingSystem
from .evolution import EvolutionManager
from .logger import SimulationLogger, create_logger

__all__ = [
    "Agent",
    "HungerGamesSimulation",
    "create_simulation",
    "LLMInterface",
    "get_llm_interface",
    "VotingSystem",
    "EvolutionManager",
    "SimulationLogger",
    "create_logger"
]
