"""
Simulation engine for AI Hunger Games.
Orchestrates rounds, manages agents, and coordinates all components.
"""

from typing import List, Dict, Any, Optional
import json
import os
from agent import Agent
from llm_interface import LLMInterface, get_llm_interface
from voting import VotingSystem
from evolution import EvolutionManager
from logger import SimulationLogger, create_logger
from config import (
    NUM_AGENTS, NUM_ROUNDS, OLLAMA_MODEL, VOTING_METHOD,
    ALLOW_SELF_VOTING, MUTATION_RATE, MUTATION_TRAITS, VERBOSE,
    get_config, DEFAULT_QUESTIONS
)


class HungerGamesSimulation:
    """
    Main simulation engine for AI Hunger Games.
    
    Manages the complete lifecycle:
    1. Initialize agents
    2. Run rounds (question -> answer -> vote -> eliminate -> evolve)
    3. Log all data
    4. Generate reports
    """
    
    def __init__(
        self,
        num_agents: int = NUM_AGENTS,
        num_rounds: int = NUM_ROUNDS,
        model: str = OLLAMA_MODEL,
        voting_method: str = VOTING_METHOD,
        verbose: bool = VERBOSE
    ):
        """
        Initialize the simulation.
        
        Args:
            num_agents: Number of agents to start with
            num_rounds: Number of rounds to simulate
            model: Default Ollama model
            voting_method: Voting method to use
            verbose: Whether to print detailed output
        """
        self.num_agents = num_agents
        self.num_rounds = num_rounds
        self.model = model
        self.verbose = verbose
        
        # Initialize components
        self.llm = get_llm_interface()
        self.voting_system = VotingSystem(voting_method, ALLOW_SELF_VOTING)
        self.evolution_manager = EvolutionManager(MUTATION_RATE, MUTATION_TRAITS)
        self.logger = create_logger()
        
        # Simulation state
        self.agents: List[Agent] = []
        self.current_round: int = 0
        self.all_agents_history: List[Agent] = []
        
        # Initialize logger
        self.logger.initialize_log(get_config())
    
    def load_initial_personalities(self, personalities_file: str = None) -> List[Dict[str, str]]:
        """
        Load initial agent personalities from JSON file.
        
        Args:
            personalities_file: Path to personalities JSON file
            
        Returns:
            List of personality dictionaries
        """
        if personalities_file is None:
            personalities_file = os.path.join("prompts", "base_personalities.json")
        
        if not os.path.exists(personalities_file):
            print(f"⚠️  Personalities file not found: {personalities_file}")
            print("    Using default personalities...")
            return self._get_default_personalities()
        
        try:
            with open(personalities_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("personalities", [])
        except Exception as e:
            print(f"❌ Error loading personalities: {e}")
            return self._get_default_personalities()
    
    def _get_default_personalities(self) -> List[Dict[str, str]]:
        """Generate default personalities if file not found."""
        return [
            {"name": "The Philosopher", "personality": "You are a deep thinker who values wisdom, logic, and contemplation. You approach problems with careful reasoning and always seek the deeper meaning."},
            {"name": "The Scientist", "personality": "You are analytical and evidence-based. You rely on data, experiments, and the scientific method to understand the world."},
            {"name": "The Artist", "personality": "You are creative and emotional. You see beauty in everything and express yourself through metaphor and artistic vision."},
            {"name": "The Pragmatist", "personality": "You are practical and results-oriented. You focus on what works and what can be implemented in the real world."},
            {"name": "The Optimist", "personality": "You always see the bright side and believe in positive outcomes. You inspire hope and encourage others."},
            {"name": "The Skeptic", "personality": "You question everything and demand proof. You are cautious and always look for potential flaws or problems."},
            {"name": "The Empath", "personality": "You deeply understand emotions and human nature. You prioritize compassion, connection, and emotional intelligence."},
            {"name": "The Strategist", "personality": "You think several steps ahead and excel at planning. You analyze situations from all angles to find the optimal path."}
        ]
    
    def initialize_agents(self, personalities: List[Dict[str, str]] = None) -> None:
        """
        Create initial agent population.
        
        Args:
            personalities: List of personality dictionaries (optional)
        """
        if personalities is None:
            personalities = self.load_initial_personalities()
        
        # Ensure we have enough personalities
        if len(personalities) < self.num_agents:
            print(f"⚠️  Only {len(personalities)} personalities available, need {self.num_agents}")
            # Duplicate some personalities if needed
            while len(personalities) < self.num_agents:
                personalities.append(personalities[len(personalities) % len(personalities)])
        
        print(f"\n🎮 Initializing {self.num_agents} agents...")
        
        for i in range(self.num_agents):
            personality = personalities[i]
            agent = Agent(
                name=personality["name"],
                personality_prompt=personality["personality"],
                model=self.model,
                generation=0,
                birth_round=0
            )
            self.agents.append(agent)
            self.all_agents_history.append(agent)
            self.logger.log_agent(agent.to_dict())
            
            if self.verbose:
                print(f"  ✓ Created: {agent.name}")
        
        print(f"\n✅ {len(self.agents)} agents ready to compete!\n")
    
    def run_round(self, round_num: int, question: str) -> Dict[str, Any]:
        """
        Run a single round of the simulation.
        
        Args:
            round_num: Current round number
            question: Question to ask agents
            
        Returns:
            Dictionary with round results
        """
        print(f"\n{'='*60}")
        print(f"🎯 ROUND {round_num}/{self.num_rounds}")
        print(f"{'='*60}")
        print(f"\n📝 Question: {question}\n")
        
        # Update rounds survived for current agents
        for agent in self.agents:
            agent.rounds_survived += 1
        
        # Phase 1: Collect answers
        answers = {}
        print("💬 Collecting answers...")
        for agent in self.agents:
            if self.verbose:
                print(f"  Asking {agent.name}...")
            
            answer = agent.generate_answer(question, round_num, self.llm)
            answers[agent.name] = answer
            
            if self.verbose:
                print(f"  ✓ {agent.name}: {answer[:100]}{'...' if len(answer) > 100 else ''}\n")
        
        # Phase 2: Voting
        vote_results = self.voting_system.conduct_vote(
            self.agents,
            question,
            answers,
            round_num,
            self.llm
        )
        
        # Print vote summary
        if self.verbose:
            print(self.voting_system.get_vote_summary(vote_results))
        
        # Phase 3: Elimination
        loser_name = self.voting_system.get_loser(vote_results)
        eliminated_agent = self.evolution_manager.eliminate_agent(
            self.agents,
            loser_name,
            round_num
        )
        
        if eliminated_agent:
            self.logger.log_evolution_event(
                "elimination",
                round_num,
                eliminated_agent.name,
                eliminated_agent.to_dict()
            )
        
        # Phase 4: Evolution
        new_agent = self.evolution_manager.create_evolved_agent(
            self.agents,
            round_num,
            self.model
        )
        
        self.agents.append(new_agent)
        self.all_agents_history.append(new_agent)
        self.logger.log_agent(new_agent.to_dict())
        self.logger.log_evolution_event(
            "creation",
            round_num,
            new_agent.name,
            new_agent.to_dict()
        )
        
        # Log round data
        self.logger.log_round(
            round_num,
            question,
            answers,
            vote_results,
            loser_name,
            new_agent.to_dict(),
            [agent.to_dict() for agent in self.agents]
        )
        
        # Print current population
        print(f"\n👥 Current Population ({len(self.agents)} agents):")
        for agent in self.agents:
            gen_info = f"Gen {agent.generation}"
            if agent.parent_name:
                gen_info += f" (from {agent.parent_name})"
            print(f"  • {agent.name:25} | {gen_info}")
        
        return {
            "round": round_num,
            "question": question,
            "answers": answers,
            "votes": vote_results,
            "eliminated": loser_name,
            "evolved": new_agent.name
        }
    
    def run_simulation(self, questions: List[str] = None) -> Dict[str, Any]:
        """
        Run the complete simulation.
        
        Args:
            questions: List of questions to ask (uses defaults if None)
            
        Returns:
            Final simulation results
        """
        # Check Ollama connection
        print("🔌 Checking Ollama connection...")
        if not self.llm.check_connection():
            print("\n❌ Cannot connect to Ollama!")
            print("   Make sure Ollama is running: ollama serve")
            print(f"   Make sure you have a model: ollama pull {self.model}")
            return {}
        
        print(f"✅ Connected to Ollama")
        print(f"📋 Available models: {', '.join(self.llm.list_models())}\n")
        
        # Use default questions if none provided
        if questions is None:
            questions = DEFAULT_QUESTIONS[:self.num_rounds]
        
        # Ensure we have enough questions
        if len(questions) < self.num_rounds:
            print(f"⚠️  Only {len(questions)} questions provided, need {self.num_rounds}")
            # Repeat questions if needed
            while len(questions) < self.num_rounds:
                questions.append(questions[len(questions) % len(questions)])
        
        # Initialize agents
        self.initialize_agents()
        
        # Run rounds
        print(f"\n🎬 Starting simulation: {self.num_rounds} rounds\n")
        
        for round_num in range(1, self.num_rounds + 1):
            question = questions[round_num - 1]
            self.run_round(round_num, question)
            self.current_round = round_num
        
        # Finalize
        return self.finalize()
    
    def finalize(self) -> Dict[str, Any]:
        """
        Finalize simulation and generate reports.
        
        Returns:
            Final statistics and results
        """
        print(f"\n\n{'='*60}")
        print("🏁 SIMULATION COMPLETE")
        print(f"{'='*60}\n")
        
        # Calculate final statistics
        final_stats = {
            "total_rounds": self.current_round,
            "total_agents_created": len(self.all_agents_history),
            "surviving_agents": len(self.agents),
            "llm_stats": self.llm.get_stats(),
            "generation_stats": self.evolution_manager.get_generation_stats(self.agents)
        }
        
        # Print final survivors
        print("🏆 FINAL SURVIVORS:\n")
        for i, agent in enumerate(sorted(self.agents, key=lambda a: a.votes_received, reverse=True), 1):
            print(f"  {i}. {agent.name}")
            print(f"     Generation: {agent.generation}")
            print(f"     Rounds Survived: {agent.rounds_survived}")
            print(f"     Votes Received: {agent.votes_received}")
            if agent.parent_name:
                print(f"     Parent: {agent.parent_name}")
            print()
        
        # Print evolution summary
        if self.verbose:
            print(self.evolution_manager.get_evolution_summary())
        
        # Finalize logger
        final_agent_dicts = [agent.to_dict() for agent in self.agents]
        self.logger.finalize_log(final_agent_dicts, final_stats)
        self.logger.print_summary()
        
        # Save logs
        saved_files = self.logger.save_all()
        
        print("\n✅ Simulation data saved successfully!")
        print(f"   JSON: {saved_files['json']}")
        print(f"   CSV: {saved_files['csv']}")
        print(f"   Agents CSV: {saved_files['agents_csv']}")
        
        return {
            "final_agents": final_agent_dicts,
            "statistics": final_stats,
            "saved_files": saved_files
        }
    
    def get_simulation_data(self) -> Dict[str, Any]:
        """Get complete simulation data."""
        return self.logger.get_data()


def create_simulation(**kwargs) -> HungerGamesSimulation:
    """
    Factory function to create a new simulation.
    
    Args:
        **kwargs: Configuration overrides
        
    Returns:
        New HungerGamesSimulation instance
    """
    return HungerGamesSimulation(**kwargs)
