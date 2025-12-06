"""
Voting system for AI Hunger Games.
Implements single-choice and ranked-choice voting mechanisms.
"""

from typing import Dict, List, Tuple, Any
from collections import Counter, defaultdict
from agent import Agent
from llm_interface import LLMInterface


class VotingSystem:
    """
    Manages the voting process for agent answers.
    
    Supports multiple voting methods:
    - Single-choice: Each agent votes for one answer
    - Ranked-choice: Agents rank answers by preference
    """
    
    def __init__(self, method: str = "single-choice", allow_self_voting: bool = False):
        """
        Initialize the voting system.
        
        Args:
            method: Voting method ("single-choice" or "ranked-choice")
            allow_self_voting: Whether agents can vote for themselves
        """
        self.method = method
        self.allow_self_voting = allow_self_voting
        self.vote_history: List[Dict[str, Any]] = []
    
    def conduct_vote(
        self,
        agents: List[Agent],
        question: str,
        answers: Dict[str, str],
        round_num: int,
        llm_interface: LLMInterface
    ) -> Dict[str, Any]:
        """
        Conduct a voting round among agents.
        
        Args:
            agents: List of participating agents
            question: The question that was asked
            answers: Dictionary mapping agent names to their answers
            round_num: Current round number
            llm_interface: LLM interface for generating votes
            
        Returns:
            Dictionary containing vote results and details
        """
        if self.method == "single-choice":
            return self._single_choice_vote(
                agents, question, answers, round_num, llm_interface
            )
        elif self.method == "ranked-choice":
            return self._ranked_choice_vote(
                agents, question, answers, round_num, llm_interface
            )
        else:
            raise ValueError(f"Unknown voting method: {self.method}")
    
    def _single_choice_vote(
        self,
        agents: List[Agent],
        question: str,
        answers: Dict[str, str],
        round_num: int,
        llm_interface: LLMInterface
    ) -> Dict[str, Any]:
        """
        Conduct single-choice voting where each agent votes for one answer.
        
        Args:
            agents: List of participating agents
            question: The question that was asked
            answers: Dictionary mapping agent names to their answers
            round_num: Current round number
            llm_interface: LLM interface for generating votes
            
        Returns:
            Dictionary with vote tallies and justifications
        """
        votes: Dict[str, int] = defaultdict(int)
        vote_details: List[Dict[str, str]] = []
        justifications: Dict[str, List[str]] = defaultdict(list)
        
        print(f"\n🗳️  Voting in progress...")
        
        for agent in agents:
            # Each agent votes
            voted_for, justification = agent.vote_on_answers(
                question,
                answers,
                round_num,
                llm_interface,
                self.allow_self_voting
            )
            
            votes[voted_for] += 1
            vote_details.append({
                "voter": agent.name,
                "voted_for": voted_for,
                "justification": justification
            })
            justifications[voted_for].append(f"{agent.name}: {justification}")
            
            print(f"  ✓ {agent.name} voted for {voted_for}")
        
        # Update agent vote counts
        for agent in agents:
            if agent.name in votes:
                agent.votes_received += votes[agent.name]
        
        result = {
            "method": "single-choice",
            "round": round_num,
            "question": question,
            "votes": dict(votes),
            "vote_details": vote_details,
            "justifications": dict(justifications),
            "total_votes": len(agents)
        }
        
        self.vote_history.append(result)
        return result
    
    def _ranked_choice_vote(
        self,
        agents: List[Agent],
        question: str,
        answers: Dict[str, str],
        round_num: int,
        llm_interface: LLMInterface
    ) -> Dict[str, Any]:
        """
        Conduct ranked-choice voting where agents rank all answers.
        
        Uses instant-runoff method for determining winner.
        
        Args:
            agents: List of participating agents
            question: The question that was asked
            answers: Dictionary mapping agent names to their answers
            round_num: Current round number
            llm_interface: LLM interface for generating votes
            
        Returns:
            Dictionary with ranked vote results
        """
        rankings: List[List[str]] = []
        vote_details: List[Dict[str, Any]] = []
        
        print(f"\n🗳️  Ranked voting in progress...")
        
        for agent in agents:
            # Get ranked preferences from agent
            ranked_list, justification = self._get_agent_rankings(
                agent,
                question,
                answers,
                round_num,
                llm_interface
            )
            
            rankings.append(ranked_list)
            vote_details.append({
                "voter": agent.name,
                "rankings": ranked_list,
                "justification": justification
            })
            
            print(f"  ✓ {agent.name} submitted rankings")
        
        # Calculate ranked-choice results
        points = defaultdict(float)
        num_candidates = len(answers)
        
        # Award points: 1st place gets n points, 2nd gets n-1, etc.
        for ranking in rankings:
            for idx, agent_name in enumerate(ranking):
                points[agent_name] += (num_candidates - idx)
        
        result = {
            "method": "ranked-choice",
            "round": round_num,
            "question": question,
            "points": dict(points),
            "vote_details": vote_details,
            "total_votes": len(agents)
        }
        
        self.vote_history.append(result)
        return result
    
    def _get_agent_rankings(
        self,
        agent: Agent,
        question: str,
        answers: Dict[str, str],
        round_num: int,
        llm_interface: LLMInterface
    ) -> Tuple[List[str], str]:
        """
        Get ranked preferences from a single agent.
        
        Args:
            agent: The agent providing rankings
            question: The question being voted on
            answers: All answers to rank
            round_num: Current round number
            llm_interface: LLM interface
            
        Returns:
            Tuple of (ranked list of agent names, justification)
        """
        # Filter out self if self-voting not allowed
        available_answers = {k: v for k, v in answers.items() 
                           if self.allow_self_voting or k != agent.name}
        
        if not available_answers:
            return [agent.name], "No other options available."
        
        # Build ranking prompt
        answers_text = "\n\n".join([
            f"Agent {name}:\n{answer}" 
            for name, answer in available_answers.items()
        ])
        
        ranking_prompt = f"""You are {agent.name}. Rank ALL of the following answers from BEST to WORST.

Question: {question}

Answers:
{answers_text}

Provide your ranking as a numbered list with the agent names, followed by a brief justification.

Format:
1. [Agent Name]
2. [Agent Name]
3. [Agent Name]
...

Justification: [Your reasoning]"""

        response = llm_interface.generate(ranking_prompt, agent.model)
        
        # Parse rankings
        ranked_list = []
        justification = ""
        
        lines = response.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.lower().startswith('justification'):
                justification = line.split(':', 1)[1].strip() if ':' in line else ""
            elif line and (line[0].isdigit() or line.startswith('-')):
                # Extract agent name from numbered list
                parts = line.split('.', 1) if '.' in line else line.split('-', 1)
                if len(parts) > 1:
                    name = parts[1].strip()
                    if name in available_answers:
                        ranked_list.append(name)
        
        # Fallback: if parsing failed, use random order
        if not ranked_list:
            import random
            ranked_list = list(available_answers.keys())
            random.shuffle(ranked_list)
            justification = "Ranking parsing failed, random order used."
        
        return ranked_list, justification
    
    def get_vote_summary(self, vote_result: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of vote results.
        
        Args:
            vote_result: Vote result dictionary
            
        Returns:
            Formatted summary string
        """
        summary = f"\n{'='*60}\n"
        summary += f"📊 VOTING RESULTS - Round {vote_result['round']}\n"
        summary += f"{'='*60}\n\n"
        
        if vote_result['method'] == 'single-choice':
            votes = vote_result['votes']
            sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
            
            summary += "Vote Tally:\n"
            for agent_name, count in sorted_votes:
                bar = "█" * count
                summary += f"  {agent_name:20} | {bar} {count} vote(s)\n"
            
            summary += f"\n🏆 Most votes: {sorted_votes[0][0]} ({sorted_votes[0][1]} votes)\n"
            summary += f"❌ Least votes: {sorted_votes[-1][0]} ({sorted_votes[-1][1]} votes)\n"
            
        elif vote_result['method'] == 'ranked-choice':
            points = vote_result['points']
            sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
            
            summary += "Points (Ranked Choice):\n"
            for agent_name, pts in sorted_points:
                summary += f"  {agent_name:20} | {pts:.1f} points\n"
            
            summary += f"\n🏆 Highest score: {sorted_points[0][0]} ({sorted_points[0][1]:.1f} points)\n"
            summary += f"❌ Lowest score: {sorted_points[-1][0]} ({sorted_points[-1][1]:.1f} points)\n"
        
        summary += f"\n{'='*60}\n"
        return summary
    
    def get_loser(self, vote_result: Dict[str, Any]) -> str:
        """
        Determine which agent has the fewest votes/points.
        
        Args:
            vote_result: Vote result dictionary
            
        Returns:
            Name of the agent with lowest score
        """
        if vote_result['method'] == 'single-choice':
            votes = vote_result['votes']
            if not votes:
                return ""
            return min(votes.items(), key=lambda x: x[1])[0]
        elif vote_result['method'] == 'ranked-choice':
            points = vote_result['points']
            if not points:
                return ""
            return min(points.items(), key=lambda x: x[1])[0]
        return ""
    
    def get_winner(self, vote_result: Dict[str, Any]) -> str:
        """
        Determine which agent has the most votes/points.
        
        Args:
            vote_result: Vote result dictionary
            
        Returns:
            Name of the agent with highest score
        """
        if vote_result['method'] == 'single-choice':
            votes = vote_result['votes']
            if not votes:
                return ""
            return max(votes.items(), key=lambda x: x[1])[0]
        elif vote_result['method'] == 'ranked-choice':
            points = vote_result['points']
            if not points:
                return ""
            return max(points.items(), key=lambda x: x[1])[0]
        return ""
