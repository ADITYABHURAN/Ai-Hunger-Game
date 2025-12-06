# AI Hunger Games - Multi-Agent Evolution & Voting Simulator

A Python-based simulation where 8 AI agents compete across multiple rounds by generating answers, voting on answers, and evolving over time using a genetic-algorithm-inspired system.

## Features

- **Multi-Agent System**: 8 AI agents with distinct personalities
- **LLM Integration**: Powered by Ollama for answer generation and voting
- **Voting System**: Single-choice and ranked-choice voting mechanisms
- **Evolution & Mutation**: Genetic algorithm-inspired agent evolution
- **Comprehensive Logging**: JSON and CSV exports for analysis
- **Optional Web Interface**: FastAPI backend with HTML/JS dashboard

## Project Structure

```
ai_hunger_games/
│── main.py                  # Entry point for simulation
│── simulation.py            # Core simulation engine
│── agent.py                 # Agent class definition
│── voting.py                # Voting system implementation
│── evolution.py             # Evolution and mutation logic
│── llm_interface.py         # Ollama API integration
│── logger.py                # Logging utilities
│── config.py                # Configuration settings
│── data/                    # Simulation logs and results
│── prompts/                 # Agent personality definitions
│── api/                     # FastAPI backend
│── ui/                      # Web interface
│── requirements.txt         # Python dependencies
│── README.md                # This file
```

## Prerequisites

1. **Python 3.9+**
2. **Ollama installed and running**
   - Install from: https://ollama.ai
   - Pull a model: `ollama pull llama2`
   - Verify: `ollama list`

## Installation

1. Clone or download this project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is running:
```bash
ollama serve
```

## Quick Start

### Step-by-Step Guide

**Step 1: Check Ollama is running**
```powershell
ollama list
```
(If this shows models, Ollama is running. If not, it auto-starts on Windows - just wait 5 seconds and try again)

**Step 2: Navigate to project**
```powershell
cd "C:\Users\Aditya Bhuran\OneDrive - Pace University\Desktop\Ai Hunger Game\ai_hunger_games"
```

**Step 3: Activate virtual environment**
```powershell
..\.venv\Scripts\Activate.ps1
```

**Step 4: Run the simulation**

Quick demo (2 minutes):
```powershell
python main.py --rounds 2 --agents 4
```

Interactive demo (best for presentations):
```powershell
python main.py --interactive --rounds 3 --agents 6
```

Full simulation (8 rounds):
```powershell
python main.py
```

### Other Options

Run with custom questions:
```bash
python main.py --questions "What is AI?" "How does evolution work?"
```

Run with different model:
```bash
python main.py --model mistral
```

## Configuration

Edit `config.py` to customize:

- **Ollama Settings**: Model name, base URL, timeout
- **Simulation**: Number of agents, rounds, voting rules
- **Evolution**: Mutation rate, mutation traits
- **Logging**: Output paths, verbosity

## How It Works

### Round Flow

1. **Question Phase**: A question is presented to all agents
2. **Answer Generation**: Each agent generates an answer using their personality
3. **Voting Phase**: Agents vote on the best answer (excluding their own)
4. **Elimination**: The agent with the fewest votes is eliminated
5. **Evolution**: A new agent is created by inheriting traits from top agents + mutations
6. **Repeat**: Continue until all rounds are complete

### Agent Evolution

- **Inheritance**: New agents inherit personality traits from successful agents
- **Mutation**: Random traits are added to create diversity
- **Memory**: Agents remember past rounds to inform future responses

### Voting Methods

- **Single-Choice**: Each agent votes for one answer
- **Ranked-Choice**: Agents rank answers by preference (optional)

## Optional: Web Interface

Start the API server:
```bash
python -m ai_hunger_games.api.server
```

Then open `ui/index.html` in your browser to view the dashboard.

## Output Files

- `data/simulation_log.json`: Complete simulation history
- `data/simulation_results.csv`: Round-by-round results
- Console output: Real-time round summaries

## Example Output

```
=== ROUND 1 ===
Question: What is the most important quality for survival?

Agent: The Philosopher
Answer: Adaptability is the cornerstone of survival...

[Voting Results]
The Philosopher: 3 votes
The Scientist: 2 votes
The Poet: 1 vote
...

Eliminated: The Pessimist
New Agent: The Optimistic Realist (evolved from The Philosopher)
```

## Customization

### Add Custom Personalities

Edit `prompts/base_personalities.json` to define new agent personalities.

### Change Voting Logic

Modify `voting.py` to implement custom voting algorithms.

### Add New Mutation Traits

Update `MUTATION_TRAITS` in `config.py`.

## Troubleshooting

**Ollama Connection Error**
- Ensure Ollama is running: `ollama serve`
- Check the base URL in `config.py`

**Slow Response Times**
- Use a faster model: `ollama pull phi`
- Increase timeout in `config.py`

**Memory Issues**
- Reduce `NUM_AGENTS` or `NUM_ROUNDS` in `config.py`

## License

MIT License - Feel free to modify and distribute.

## Contributing

Contributions welcome! Please submit pull requests or open issues for bugs and feature requests.
