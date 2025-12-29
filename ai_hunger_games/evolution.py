"""
Evolution module for AI Hunger Games.
Handles agent elimination and creation of evolved agents.
"""



from typing import List, Optional, Dict, Any
import random
from agent import Agent
from config import MUTATION_TRAITS, MUTATION_RATE


class EvolutionManager:
    """
    Manages the evolution process: elimination and creation of new agents.
    
    Uses genetic algorithm concepts:
    - Selection: Eliminate weakest agent
    - Crossover: Inherit traits from successful agents
    - Mutation: Add random variations to create diversity
    """
    
    def __init__(self, mutation_rate: float = MUTATION_RATE, mutation_traits: List[str] = None):
        """
        Initialize the evolution manager.
        
        Args:
            mutation_rate: Probability of mutations (0.0 to 1.0)
            mutation_traits: List of possible mutation traits
        """
        self.mutation_rate = mutation_rate
        self.mutation_traits = mutation_traits or MUTATION_TRAITS
        self.elimination_history: List[Dict[str, Any]] = []
        self.creation_history: List[Dict[str, Any]] = []
    
    def eliminate_agent(
        self,
        agents: List[Agent],
        loser_name: str,
        round_num: int,
        reason: str = "Received fewest votes"
    ) -> Optional[Agent]:
        """
        Remove the eliminated agent from the population.
        
        Args:
            agents: List of current agents
            loser_name: Name of the agent to eliminate
            round_num: Current round number
            reason: Reason for elimination
            
        Returns:
            The eliminated agent, or None if not found
        """
        eliminated_agent = None
        
        for i, agent in enumerate(agents):
            if agent.name == loser_name:
                eliminated_agent = agents.pop(i)
                break
        
        if eliminated_agent:
            elimination_record = {
                "round": round_num,
                "agent_name": eliminated_agent.name,
                "generation": eliminated_agent.generation,
                "parent": eliminated_agent.parent_name,
                "rounds_survived": eliminated_agent.rounds_survived,
                "votes_received": eliminated_agent.votes_received,
                "answers_given": eliminated_agent.answers_given,
                "reason": reason,
                "personality": eliminated_agent.personality_prompt[:200] + "..."
            }
            
            self.elimination_history.append(elimination_record)
            
            print(f"\n💀 ELIMINATED: {eliminated_agent.name}")
            print(f"   Generation: {eliminated_agent.generation}")
            print(f"   Survived: {eliminated_agent.rounds_survived} rounds")
            print(f"   Reason: {reason}")
        
        return eliminated_agent
    
    def create_evolved_agent(
        self,
        existing_agents: List[Agent],
        round_num: int,
        model: str = "llama2",
        base_name: Optional[str] = None
    ) -> Agent:
        """
        Create a new evolved agent based on existing successful agents.
        
        Args:
            existing_agents: Current surviving agents
            round_num: Current round number
            model: Ollama model to use
            base_name: Base name for the new agent (optional)
            
        Returns:
            Newly created evolved agent
        """
        if not existing_agents:
            raise ValueError("Cannot create evolved agent with no existing agents")
        
        # Select parent: prioritize agents with more votes
        parent = self._select_parent(existing_agents)
        
        # Create evolved personality
        new_personality = self._evolve_personality(parent)
        
        # Generate name
        new_name = self._generate_evolved_name(parent, base_name)
        
        # Create new agent
        new_agent = Agent(
            name=new_name,
            personality_prompt=new_personality,
            model=model,
            generation=parent.generation + 1,
            parent_name=parent.name,
            birth_round=round_num
        )
        
        # Record creation
        creation_record = {
            "round": round_num,
            "agent_name": new_agent.name,
            "generation": new_agent.generation,
            "parent": parent.name,
            "personality": new_personality[:200] + "...",
            "mutations_applied": self._extract_mutations(new_personality)
        }
        
        self.creation_history.append(creation_record)
        
        print(f"\n✨ NEW AGENT EVOLVED: {new_agent.name}")
        print(f"   Parent: {parent.name} (Gen {parent.generation})")
        print(f"   Generation: {new_agent.generation}")
        print(f"   Traits inherited and mutated")
        
        return new_agent
    
    def _select_parent(self, agents: List[Agent]) -> Agent:
        """
        Select a parent agent for evolution (weighted by success).
        
        Args:
            agents: List of agents to select from
            
        Returns:
            Selected parent agent
        """
        # Weight by votes received (successful agents more likely to be parents)
        weights = [agent.votes_received + 1 for agent in agents]  # +1 to avoid zero weights
        
        # If all weights are equal, also consider rounds survived
        if len(set(weights)) == 1:
            weights = [agent.rounds_survived + 1 for agent in agents]
        
        parent = random.choices(agents, weights=weights, k=1)[0]
        return parent
    
    def _evolve_personality(self, parent: Agent) -> str:
        """
        Create an evolved personality from a parent agent.
        
        Args:
            parent: Parent agent to evolve from
            
        Returns:
            New evolved personality prompt
        """
        # Start with parent's personality
        evolved_personality = parent.personality_prompt
        
        # Apply mutations
        if random.random() < self.mutation_rate:
            num_mutations = random.randint(1, 3)
            selected_traits = random.sample(
                self.mutation_traits, 
                min(num_mutations, len(self.mutation_traits))
            )
            
            mutation_text = "\n\nEvolved traits: "
            mutation_text += f"You have evolved to be {', '.join(selected_traits)}. "
            mutation_text += f"You inherit your parent's core values but express them through these new traits."
            
            evolved_personality += mutation_text
        else:
            # Minor refinement without major mutations
            evolved_personality += "\n\nYou are a refined version of your predecessor, maintaining their core philosophy."
        
        return evolved_personality
    
    def _generate_evolved_name(self, parent: Agent, base_name: Optional[str] = None) -> str:
        """
        Generate a name for the evolved agent.
        
        Args:
            parent: Parent agent
            base_name: Optional base name to use
            
        Returns:
            Name for the new agent
        """
        if base_name:
            return f"{base_name} II"
        
        # Generate evolved name variants
        evolution_suffixes = [
            "Evolved", "2.0", "Redux", "Reborn", "Neo",
            "Next", "Prime", "Enhanced", "Advanced", "Plus"
        ]
        
        suffix = random.choice(evolution_suffixes)
        
        # Sometimes use parent name, sometimes modify it
        if random.random() < 0.6:
            return f"{parent.name} {suffix}"
        else:
            # Create a variant name
            adjectives = [
                "Adaptive", "Strategic", "Resilient", "Dynamic", "Innovative",
                "Insightful", "Cunning", "Wise", "Bold", "Swift"
            ]
            nouns = [
                "Thinker", "Scholar", "Mind", "Sage", "Oracle",
                "Strategist", "Visionary", "Pioneer", "Master", "Expert"
            ]
            
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            return f"The {adj} {noun}"
    
    def _extract_mutations(self, personality: str) -> List[str]:
        """
        Extract mutation traits from personality prompt.
        
        Args:
            personality: Personality prompt string
            
        Returns:
            List of mutation traits found
        """
        mutations = []
        for trait in self.mutation_traits:
            if trait in personality.lower():
                mutations.append(trait)
        return mutations
    
    def get_evolution_summary(self) -> str:
        """
        Generate a summary of the evolution history.
        
        Returns:
            Formatted evolution history string
        """
        summary = "\n" + "="*60 + "\n"
        summary += "🧬 EVOLUTION HISTORY\n"
        summary += "="*60 + "\n\n"
        
        summary += f"Total Eliminations: {len(self.elimination_history)}\n"
        summary += f"Total New Agents: {len(self.creation_history)}\n\n"
        
        summary += "Elimination Timeline:\n"
        for record in self.elimination_history:
            summary += f"  Round {record['round']}: {record['agent_name']} "
            summary += f"(Gen {record['generation']}, survived {record['rounds_survived']} rounds)\n"
        
        summary += "\nCreation Timeline:\n"
        for record in self.creation_history:
            summary += f"  Round {record['round']}: {record['agent_name']} "
            summary += f"(Gen {record['generation']}, parent: {record['parent']})\n"
        
        summary += "\n" + "="*60 + "\n"
        return summary
    
    def get_generation_stats(self, agents: List[Agent]) -> Dict[str, Any]:
        """
        Calculate statistics about agent generations.
        
        Args:
            agents: Current list of agents
            
        Returns:
            Dictionary with generation statistics
        """
        generations = [agent.generation for agent in agents]
        
        return {
            "average_generation": sum(generations) / len(generations) if generations else 0,
            "max_generation": max(generations) if generations else 0,
            "min_generation": min(generations) if generations else 0,
            "generation_diversity": len(set(generations))
        }
    
    def get_lineage(self, agent: Agent, all_history: List[Agent]) -> List[str]:
        """
        Trace the lineage of an agent back to its original ancestor.
        
        Args:
            agent: Agent to trace
            all_history: Complete history of all agents
            
        Returns:
            List of ancestor names from oldest to newest
        """
        lineage = [agent.name]
        current = agent
        
        while current.parent_name:
            lineage.append(current.parent_name)
            # Find parent in history
            parent_found = False
            for historical_agent in all_history:
                if historical_agent.name == current.parent_name:
                    current = historical_agent
                    parent_found = True
                    break
            
            if not parent_found:
                break
        
        return list(reversed(lineage))
