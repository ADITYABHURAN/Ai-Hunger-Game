"""
Agent class for AI Hunger Games simulation.
Each agent has a personality, memory, and can generate answers and vote.
"""

from typing import Dict, List, Optional, Any
import random
from datetime import datetime


class Agent:
    """
    Represents an AI agent in the Hunger Games simulation.
    
    Attributes:
        name: The agent's unique name
        personality_prompt: The personality description that guides the agent's behavior
        memory: List of past interactions and learnings
        model: The Ollama model name to use for this agent
        generation: Which generation this agent belongs to (0 for original)
        parent_name: Name of the parent agent (if evolved)
        birth_round: The round in which this agent was created
    """
    
    def __init__(
        self,
        name: str,
        personality_prompt: str,
        model: str = "llama2",
        generation: int = 0,
        parent_name: Optional[str] = None,
        birth_round: int = 0
    ):
        """
        Initialize a new Agent.
        
        Args:
            name: Agent's unique name
            personality_prompt: Description of agent's personality and behavior
            model: Ollama model to use
            generation: Generation number (0 for original agents)
            parent_name: Name of parent agent if evolved
            birth_round: Round number when agent was created
        """
        self.name: str = name
        self.personality_prompt: str = personality_prompt
        self.memory: List[Dict[str, Any]] = []
        self.model: str = model
        self.generation: int = generation
        self.parent_name: Optional[str] = parent_name
        self.birth_round: int = birth_round
        self.votes_received: int = 0
        self.votes_cast: int = 0
        self.rounds_survived: int = 0
        self.answers_given: int = 0
        
    def add_memory(self, memory_type: str, content: str, round_num: int) -> None:
        """
        Add a memory to the agent's memory buffer.
        
        Args:
            memory_type: Type of memory (e.g., "question", "answer", "vote", "elimination")
            content: The content of the memory
            round_num: The round number when this memory was created
        """
        memory_entry = {
            "type": memory_type,
            "content": content,
            "round": round_num,
            "timestamp": datetime.now().isoformat()
        }
        self.memory.append(memory_entry)
        
        # Limit memory size (keep most recent memories)
        from config import MAX_MEMORY_SIZE
        if len(self.memory) > MAX_MEMORY_SIZE:
            self.memory = self.memory[-MAX_MEMORY_SIZE:]
    
    def get_memory_context(self, max_memories: int = 5) -> str:
        """
        Get recent memories as a formatted string for context.
        
        Args:
            max_memories: Maximum number of recent memories to include
            
        Returns:
            Formatted string of recent memories
        """
        if not self.memory:
            return "No previous memories."
        
        recent_memories = self.memory[-max_memories:]
        context = "Recent memories:\n"
        for mem in recent_memories:
            context += f"- Round {mem['round']} ({mem['type']}): {mem['content'][:100]}...\n"
        return context
    
    def generate_answer(
        self,
        question: str,
        round_num: int,
        llm_interface: Any  # Type hint for LLMInterface
    ) -> str:
        """
        Generate an answer to the given question using the agent's personality.
        
        Args:
            question: The question to answer
            round_num: Current round number
            llm_interface: The LLM interface to use for generation
            
        Returns:
            The generated answer string
        """
        # Build the prompt with personality and memory context
        memory_context = self.get_memory_context()
        
        full_prompt = f"""You are {self.name}, an AI agent with the following personality:
{self.personality_prompt}

{memory_context}

Question: {question}

Provide a thoughtful answer that reflects your unique personality and perspective. Be concise but insightful (2-4 sentences)."""

        # Generate answer using LLM interface
        answer = llm_interface.generate(full_prompt, self.model)
        
        # Store in memory
        self.add_memory("answer", f"Q: {question} | A: {answer}", round_num)
        self.answers_given += 1
        
        return answer
    
    def vote_on_answers(
        self,
        question: str,
        answers: Dict[str, str],
        round_num: int,
        llm_interface: Any,
        allow_self_voting: bool = False
    ) -> tuple[str, str]:
        """
        Vote on the best answer from the provided options.
        
        Args:
            question: The question that was asked
            answers: Dictionary mapping agent names to their answers
            round_num: Current round number
            llm_interface: The LLM interface to use for generation
            allow_self_voting: Whether the agent can vote for itself
            
        Returns:
            Tuple of (voted_agent_name, justification)
        """
        # Filter out self if self-voting not allowed
        available_answers = {k: v for k, v in answers.items() 
                           if allow_self_voting or k != self.name}
        
        if not available_answers:
            # Edge case: only self answer available
            return self.name, "No other options available."
        
        # Build voting prompt
        answers_text = "\n\n".join([
            f"Agent {name}:\n{answer}" 
            for name, answer in available_answers.items()
        ])
        
        voting_prompt = f"""You are {self.name}, an AI agent with this personality:
{self.personality_prompt}

Question that was asked: {question}

Here are the answers from different agents:

{answers_text}

Based on your personality and values, which agent gave the BEST answer? 
Respond with ONLY the agent's name on the first line, followed by a 1-2 sentence justification on the next line.

Format:
Agent Name
Justification here."""

        # Generate vote
        vote_response = llm_interface.generate(voting_prompt, self.model)
        
        # Parse response
        lines = vote_response.strip().split('\n', 1)
        voted_for = lines[0].strip()
        justification = lines[1].strip() if len(lines) > 1 else "No justification provided."
        
        # Validate vote (must be one of the available agents)
        if voted_for not in available_answers:
            # Fallback: pick random agent
            voted_for = random.choice(list(available_answers.keys()))
            justification = "Vote parsing failed, random selection made."
        
        # Store in memory
        self.add_memory("vote", f"Voted for {voted_for}: {justification}", round_num)
        self.votes_cast += 1
        
        return voted_for, justification
    
    def mutate(self, mutation_traits: List[str], mutation_rate: float = 0.3) -> str:
        """
        Create a mutated version of the personality prompt.
        
        Args:
            mutation_traits: List of possible mutation traits to add
            mutation_rate: Probability of adding mutations
            
        Returns:
            New mutated personality prompt
        """
        mutated_prompt = self.personality_prompt
        
        # Add mutations based on mutation rate
        if random.random() < mutation_rate:
            num_mutations = random.randint(1, 2)
            selected_traits = random.sample(mutation_traits, min(num_mutations, len(mutation_traits)))
            
            mutation_text = ", ".join(selected_traits)
            mutated_prompt += f"\n\nEvolved traits: You are now {mutation_text} compared to your predecessor."
        
        return mutated_prompt
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert agent to dictionary for logging and serialization.
        
        Returns:
            Dictionary representation of the agent
        """
        return {
            "name": self.name,
            "personality_prompt": self.personality_prompt,
            "model": self.model,
            "generation": self.generation,
            "parent_name": self.parent_name,
            "birth_round": self.birth_round,
            "votes_received": self.votes_received,
            "votes_cast": self.votes_cast,
            "rounds_survived": self.rounds_survived,
            "answers_given": self.answers_given,
            "memory_count": len(self.memory),
            "recent_memories": self.memory[-3:] if self.memory else []
        }
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"Agent(name='{self.name}', generation={self.generation}, survived={self.rounds_survived})"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        parent_info = f", parent: {self.parent_name}" if self.parent_name else ""
        return f"{self.name} (Gen {self.generation}{parent_info})"
