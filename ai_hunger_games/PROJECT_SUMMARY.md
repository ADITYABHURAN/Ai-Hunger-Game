# 🎮 AI Hunger Games - Project Complete! 🎮

## ✅ Project Successfully Generated

Your AI Hunger Games simulation is fully set up and ready to run!

## 📁 Project Structure

```
ai_hunger_games/
├── main.py                          # Main entry point
├── config.py                        # Configuration settings
├── agent.py                         # Agent class with personality & memory
├── llm_interface.py                 # Ollama API integration
├── voting.py                        # Single & ranked-choice voting
├── evolution.py                     # Elimination & mutation logic
├── simulation.py                    # Main simulation engine
├── logger.py                        # JSON & CSV logging
├── __init__.py                      # Package initialization
│
├── prompts/
│   └── base_personalities.json     # 8 diverse agent personalities
│
├── data/
│   └── README.md                   # Log files go here
│
├── api/
│   ├── __init__.py
│   └── server.py                   # FastAPI backend
│
├── ui/
│   └── index.html                  # Web dashboard
│
├── requirements.txt                # Python dependencies
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
└── .gitignore                      # Git ignore file
```

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
cd ai_hunger_games
pip install -r requirements.txt
```

### 2. Ensure Ollama is Running
```powershell
# In a separate terminal
ollama serve

# Pull a model if you haven't
ollama pull llama2
```

### 3. Run the Simulation
```powershell
python main.py
```

## 🎯 Features Implemented

### Core Features ✅
- ✅ 8 AI agents with unique personalities
- ✅ Answer generation using Ollama
- ✅ Single-choice voting system
- ✅ Ranked-choice voting (optional)
- ✅ Agent elimination based on votes
- ✅ Genetic evolution with mutations
- ✅ Agent memory system
- ✅ Configurable simulation parameters

### Logging & Analytics ✅
- ✅ JSON export with complete data
- ✅ CSV export for round summaries
- ✅ Agent statistics tracking
- ✅ Evolution history logging
- ✅ Vote justifications captured

### Optional Features ✅
- ✅ FastAPI REST API backend
- ✅ Web-based dashboard (HTML/JS)
- ✅ Real-time status monitoring
- ✅ Beautiful UI with gradients
- ✅ Command-line arguments support
- ✅ Custom questions support

## 📊 What Happens in Each Round

1. **Question Phase** - A question is presented to all agents
2. **Answer Generation** - Each agent generates an answer based on their personality
3. **Voting Phase** - Agents vote on the best answer (can't vote for themselves)
4. **Elimination** - Agent with fewest votes is eliminated
5. **Evolution** - New agent is created by inheriting traits + mutations
6. **Logging** - All data is saved for analysis

## 🎨 Agent Personalities

1. **The Philosopher** - Deep thinker, values wisdom and logic
2. **The Scientist** - Analytical, evidence-based reasoning
3. **The Artist** - Creative, emotional, metaphorical
4. **The Pragmatist** - Practical, results-oriented
5. **The Optimist** - Positive, hopeful, encouraging
6. **The Skeptic** - Questioning, cautious, critical
7. **The Empath** - Compassionate, emotionally intelligent
8. **The Strategist** - Forward-thinking, tactical planner

## 🧬 Evolution System

- **Inheritance** - New agents inherit parent's personality traits
- **Mutation** - Random traits added (analytical, creative, skeptical, etc.)
- **Generation Tracking** - Each agent knows its generation and lineage
- **Adaptive Selection** - Successful agents more likely to be parents

## 📈 Example Commands

```powershell
# Basic run
python main.py

# Custom configuration
python main.py --agents 10 --rounds 12 --model mistral

# Ranked-choice voting
python main.py --voting ranked-choice

# Custom questions
python main.py --questions "What is AI?" "How does evolution work?"

# Quiet mode (less output)
python main.py --quiet

# Start web API
python -m ai_hunger_games.api.server
```

## 🌐 Web Interface

1. Start the API server:
   ```powershell
   python -m ai_hunger_games.api.server
   ```

2. Open `ui/index.html` in your browser

3. Configure and start simulation from the web UI

4. View real-time results and statistics

## 📝 Configuration Options

Edit `config.py` to customize:

- **Ollama Settings** - Base URL, model, timeout
- **Simulation** - Number of agents, rounds, voting rules
- **Evolution** - Mutation rate, available traits
- **Logging** - Output paths, verbosity
- **Questions** - Default questions for rounds

## 📂 Output Files

After each simulation, find in `data/`:

- `simulation_[timestamp].json` - Complete simulation data
- `simulation_[timestamp].csv` - Round-by-round summary
- `agents_[timestamp].csv` - Agent statistics

## 🔧 Code Architecture

### Agent Class (`agent.py`)
- Personality prompt and memory
- `generate_answer()` - Creates responses
- `vote_on_answers()` - Votes on other agents
- `mutate()` - Creates evolved personality
- `to_dict()` - Serialization for logging

### LLM Interface (`llm_interface.py`)
- Connects to Ollama API
- Handles retries and timeouts
- Tracks API statistics
- Provides singleton access

### Voting System (`voting.py`)
- Single-choice and ranked-choice methods
- Vote tallying and justifications
- Determines winners and losers
- Generates vote summaries

### Evolution Manager (`evolution.py`)
- Eliminates weakest agents
- Selects parent based on success
- Applies mutations to create offspring
- Tracks lineage and generations

### Simulation Engine (`simulation.py`)
- Orchestrates all components
- Manages round flow
- Coordinates logging
- Generates final reports

### Logger (`logger.py`)
- JSON and CSV export
- Round and agent tracking
- Evolution history
- Final statistics

## 🎓 Type Hints & Documentation

All code includes:
- Comprehensive docstrings
- Type hints for better IDE support
- Inline comments for complex logic
- Clear parameter descriptions

## 🚨 Error Handling

- Connection checks for Ollama
- Retry logic for API failures
- Graceful degradation
- Informative error messages
- Keyboard interrupt handling

## 🎉 Ready to Run!

Your project is complete and production-ready. Start with:

```powershell
python main.py
```

And watch your AI agents compete for survival! 🎮

---

**Need help?** Check `QUICKSTART.md` or `README.md` for detailed instructions.

**Want to customize?** Edit `config.py` or `prompts/base_personalities.json`.

**Enjoy the simulation!** 🏆
