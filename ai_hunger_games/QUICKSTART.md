# Quick Start Guide - AI Hunger Games

## Prerequisites

1. **Python 3.9 or higher**
   ```powershell
   python --version
   ```

2. **Ollama installed and running**
   - Download from: https://ollama.ai
   - Install and run:
   ```powershell
   ollama serve
   ```

3. **Pull a model**
   ```powershell
   ollama pull llama2
   ```

## Installation

1. **Install dependencies**
   ```powershell
   cd ai_hunger_games
   pip install -r requirements.txt
   ```

## Running the Simulation

### Option 1: Basic Run (Command Line)

```powershell
python main.py
```

### Option 2: Custom Configuration

```powershell
# Run with 10 agents and 12 rounds
python main.py --agents 10 --rounds 12

# Use a different model
python main.py --model mistral

# Use ranked-choice voting
python main.py --voting ranked-choice

# Custom questions
python main.py --questions "What is AI?" "How does learning work?" "What is consciousness?"
```

### Option 3: Web Interface

1. **Start the API server**
   ```powershell
   python -m ai_hunger_games.api.server
   ```

2. **Open the dashboard**
   - Open `ui/index.html` in your web browser
   - Or navigate to: `file:///[path-to-project]/ai_hunger_games/ui/index.html`

3. **Configure and run**
   - Set your parameters in the web interface
   - Click "Start Simulation"
   - Watch the results in real-time

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if the model is available: `ollama list`
- Verify the base URL in `config.py`

### "Module not found"
- Ensure you're in the correct directory
- Run: `pip install -r requirements.txt`

### Slow performance
- Use a smaller/faster model: `ollama pull phi`
- Update `config.py`: `OLLAMA_MODEL = "phi"`
- Reduce number of agents or rounds

### Web interface not connecting
- Make sure API server is running on port 8000
- Check for CORS issues in browser console
- Try accessing: http://localhost:8000/docs

## Output Files

After running, check the `data/` folder for:
- `simulation_YYYYMMDD_HHMMSS.json` - Complete simulation data
- `simulation_YYYYMMDD_HHMMSS.csv` - Round summaries
- `agents_YYYYMMDD_HHMMSS.csv` - Agent statistics

## Next Steps

1. **Analyze results** - Open the CSV files in Excel/Google Sheets
2. **Customize personalities** - Edit `prompts/base_personalities.json`
3. **Modify configuration** - Adjust settings in `config.py`
4. **Add mutations** - Update `MUTATION_TRAITS` in `config.py`

## Example Session

```
🎮 Initializing 8 agents...
  ✓ Created: The Philosopher
  ✓ Created: The Scientist
  ✓ Created: The Artist
  ...

🎯 ROUND 1/8
📝 Question: What is the most important quality for survival?

💬 Collecting answers...
  ✓ The Philosopher: Adaptability is the cornerstone...

🗳️ Voting in progress...
  ✓ The Philosopher voted for The Strategist

💀 ELIMINATED: The Pessimist
✨ NEW AGENT EVOLVED: The Optimistic Realist

🏆 FINAL SURVIVORS:
  1. The Philosopher (Gen 0, 8 rounds, 15 votes)
  2. The Strategist Enhanced (Gen 3, 6 rounds, 12 votes)
  ...
```

Enjoy the simulation! 🎮
