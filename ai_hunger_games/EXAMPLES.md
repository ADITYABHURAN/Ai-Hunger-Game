# AI Hunger Games - Usage Examples

## Command-Line Examples

### Basic Usage

```powershell
# Run with default settings (8 agents, 8 rounds, llama2)
python main.py

# Quiet mode (less verbose output)
python main.py --quiet
```

### Custom Configuration

```powershell
# More agents and rounds
python main.py --agents 12 --rounds 15

# Different model
python main.py --model mistral
python main.py --model phi
python main.py --model codellama

# Ranked-choice voting
python main.py --voting ranked-choice

# Combine options
python main.py --agents 10 --rounds 12 --model mistral --voting ranked-choice
```

### Custom Questions

```powershell
# Single question
python main.py --questions "What is artificial intelligence?"

# Multiple questions
python main.py --questions "What is AI?" "How does learning work?" "What is consciousness?" "Should AI have rights?"

# Many rounds with custom questions
python main.py --rounds 10 --questions "Q1" "Q2" "Q3" "Q4" "Q5" "Q6" "Q7" "Q8" "Q9" "Q10"
```

### Using Custom Personalities

```powershell
# Create your own personalities.json file
python main.py --personalities my_custom_personalities.json
```

## Python API Examples

### Basic Simulation

```python
from ai_hunger_games import create_simulation

# Create and run simulation
sim = create_simulation(
    num_agents=8,
    num_rounds=8,
    model="llama2",
    voting_method="single-choice",
    verbose=True
)

results = sim.run_simulation()

# Access results
print(f"Final agents: {len(results['final_agents'])}")
print(f"Total rounds: {results['statistics']['total_rounds']}")
```

### Custom Questions Programmatically

```python
from ai_hunger_games import create_simulation

questions = [
    "What is the nature of consciousness?",
    "How should AI make ethical decisions?",
    "What is the meaning of intelligence?",
    "How can we solve climate change?",
    "What makes a good leader?",
    "Should AI have rights?",
    "What is the future of humanity?",
    "How do we balance progress with safety?"
]

sim = create_simulation()
results = sim.run_simulation(questions=questions)
```

### Access Simulation Data

```python
from ai_hunger_games import create_simulation

sim = create_simulation()
results = sim.run_simulation()

# Get complete simulation data
data = sim.get_simulation_data()

# Access specific information
rounds = data['rounds']
agents = data['agents']
evolution_history = data['evolution_history']
final_stats = data['final_stats']

# Analyze results
for round_data in rounds:
    print(f"Round {round_data['round_number']}")
    print(f"Question: {round_data['question']}")
    print(f"Eliminated: {round_data['eliminated_agent']}")
    print(f"New Agent: {round_data['new_agent']['name']}")
    print()
```

### Custom Agent Creation

```python
from ai_hunger_games import Agent, create_simulation
from ai_hunger_games.llm_interface import get_llm_interface

# Create custom agent
custom_agent = Agent(
    name="The Maverick",
    personality_prompt="You are a rebellious thinker who challenges norms and conventional wisdom.",
    model="llama2",
    generation=0,
    birth_round=0
)

# Use in simulation
sim = create_simulation()

# Replace one agent with custom agent
sim.agents[0] = custom_agent
sim.all_agents_history.append(custom_agent)

# Run simulation
results = sim.run_simulation()
```

### Loading and Analyzing Past Simulations

```python
from ai_hunger_games import SimulationLogger

# Load previous simulation
logger = SimulationLogger()
logger.load_from_file('data/simulation_20231205_143022.json')

# Get data
data = logger.get_data()

# Analyze
print(f"Simulation ran on: {data['metadata']['start_time']}")
print(f"Total rounds: {len(data['rounds'])}")
print(f"Final survivors: {len(data['final_agents'])}")

# Find most successful agent
agents = data['agents']
top_agent = max(agents, key=lambda a: a['votes_received'])
print(f"Most votes: {top_agent['name']} with {top_agent['votes_received']} votes")
```

## Web API Examples

### Starting the Server

```powershell
# Start on default port (8000)
python -m ai_hunger_games.api.server

# Start on custom port
python -m ai_hunger_games.api.server 9000
```

### Using the REST API

```python
import requests
import time

API_BASE = "http://localhost:8000"

# Start simulation
config = {
    "num_agents": 8,
    "num_rounds": 8,
    "model": "llama2",
    "voting_method": "single-choice",
    "questions": None  # Use defaults
}

response = requests.post(f"{API_BASE}/simulation/start", json=config)
print(response.json())

# Poll for status
while True:
    status = requests.get(f"{API_BASE}/simulation/status").json()
    print(f"Status: {status['status']} - {status['message']}")
    
    if status['status'] in ['completed', 'error']:
        break
    
    time.sleep(2)

# Get results
if status['status'] == 'completed':
    results = requests.get(f"{API_BASE}/simulation/results").json()
    print(f"Final agents: {len(results['final_agents'])}")

# List all logs
logs = requests.get(f"{API_BASE}/simulation/logs").json()
print(f"Available logs: {len(logs['logs'])}")

# Get specific log
if logs['logs']:
    log_filename = logs['logs'][0]['filename']
    log_data = requests.get(f"{API_BASE}/simulation/logs/{log_filename}").json()
    print(f"Loaded log with {len(log_data['rounds'])} rounds")
```

### Using cURL

```bash
# Start simulation
curl -X POST http://localhost:8000/simulation/start \
  -H "Content-Type: application/json" \
  -d '{
    "num_agents": 8,
    "num_rounds": 8,
    "model": "llama2",
    "voting_method": "single-choice"
  }'

# Check status
curl http://localhost:8000/simulation/status

# Get results
curl http://localhost:8000/simulation/results

# List logs
curl http://localhost:8000/simulation/logs

# Health check
curl http://localhost:8000/health
```

## Configuration Examples

### Creating Custom config.py

```python
# config.py modifications

# Use a different model
OLLAMA_MODEL = "mistral"

# More agents and rounds
NUM_AGENTS = 12
NUM_ROUNDS = 15

# Enable self-voting
ALLOW_SELF_VOTING = True

# Ranked-choice voting
VOTING_METHOD = "ranked-choice"

# Higher mutation rate
MUTATION_RATE = 0.5

# Custom mutation traits
MUTATION_TRAITS = [
    "more aggressive",
    "more cautious",
    "more innovative",
    "more traditional",
    "more collaborative",
    "more independent"
]

# Custom questions
DEFAULT_QUESTIONS = [
    "How do you define success?",
    "What is the role of technology in society?",
    "How should resources be distributed?",
    "What is the best form of government?",
    # ... more questions
]
```

### Custom Personalities JSON

```json
{
  "description": "Custom agent personalities",
  "personalities": [
    {
      "name": "The Hacker",
      "personality": "You are a creative problem-solver who thinks outside the box. You love finding unconventional solutions and breaking down complex systems."
    },
    {
      "name": "The Diplomat",
      "personality": "You excel at finding common ground and building consensus. You value harmony and believe in win-win solutions."
    },
    {
      "name": "The Entrepreneur",
      "personality": "You are risk-tolerant and opportunity-focused. You see potential where others see problems and are always ready to innovate."
    },
    {
      "name": "The Guardian",
      "personality": "You prioritize safety, stability, and protecting what works. You are cautious about change and value proven approaches."
    }
  ]
}
```

## Advanced Usage

### Batch Simulations

```python
from ai_hunger_games import create_simulation
import json

# Run multiple simulations with different configurations
configs = [
    {"num_agents": 8, "voting_method": "single-choice"},
    {"num_agents": 8, "voting_method": "ranked-choice"},
    {"num_agents": 12, "voting_method": "single-choice"},
    {"num_agents": 12, "voting_method": "ranked-choice"},
]

all_results = []

for i, config in enumerate(configs):
    print(f"\nRunning simulation {i+1}/{len(configs)}")
    sim = create_simulation(**config, verbose=False)
    results = sim.run_simulation()
    all_results.append({
        "config": config,
        "results": results
    })

# Save comparative results
with open('data/batch_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)
```

### Statistical Analysis

```python
import pandas as pd
from ai_hunger_games import SimulationLogger

# Load simulation data
logger = SimulationLogger()
logger.load_from_file('data/simulation_20231205_143022.json')
data = logger.get_data()

# Convert to DataFrame for analysis
agents_df = pd.DataFrame(data['agents'])

# Analyze
print("Agent Statistics:")
print(agents_df[['name', 'generation', 'votes_received', 'rounds_survived']].describe())

# Find correlations
print("\nCorrelation between generation and votes:")
print(agents_df[['generation', 'votes_received']].corr())

# Generation distribution
print("\nAgents by generation:")
print(agents_df['generation'].value_counts().sort_index())
```

### Custom Voting Logic

```python
from ai_hunger_games.voting import VotingSystem

# Extend VotingSystem for custom logic
class WeightedVotingSystem(VotingSystem):
    def _single_choice_vote(self, agents, question, answers, round_num, llm_interface):
        # Get standard votes
        result = super()._single_choice_vote(agents, question, answers, round_num, llm_interface)
        
        # Apply generation weighting
        weighted_votes = {}
        for agent_name, votes in result['votes'].items():
            agent = next(a for a in agents if a.name == agent_name)
            weight = 1.0 + (agent.generation * 0.1)  # Newer generations get slight boost
            weighted_votes[agent_name] = votes * weight
        
        result['votes'] = weighted_votes
        return result

# Use custom voting
from ai_hunger_games import create_simulation
sim = create_simulation()
sim.voting_system = WeightedVotingSystem()
results = sim.run_simulation()
```

## Troubleshooting Examples

### Check Ollama Connection

```python
from ai_hunger_games.llm_interface import get_llm_interface

llm = get_llm_interface()

if llm.check_connection():
    print("✅ Ollama is connected")
    models = llm.list_models()
    print(f"Available models: {models}")
else:
    print("❌ Cannot connect to Ollama")
    print("Make sure Ollama is running: ollama serve")
```

### Test Generation

```python
from ai_hunger_games.llm_interface import get_llm_interface

llm = get_llm_interface()

# Test prompt
response = llm.generate(
    prompt="Say hello in one sentence.",
    model="llama2"
)

print(f"Response: {response}")
print(f"Stats: {llm.get_stats()}")
```

### Debug Mode

```python
from ai_hunger_games import create_simulation

# Create simulation with verbose output
sim = create_simulation(verbose=True)

# Run single round for debugging
sim.initialize_agents()
result = sim.run_round(1, "What is the meaning of life?")

print("Round result:", result)
```

## Integration Examples

### Integrate with Discord Bot

```python
import discord
from ai_hunger_games import create_simulation

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('!hunger-games'):
        await message.channel.send("Starting AI Hunger Games simulation...")
        
        sim = create_simulation(verbose=False)
        results = sim.run_simulation()
        
        # Send results to Discord
        final_agents = results['final_agents']
        response = "🏆 **Final Survivors:**\n"
        for i, agent in enumerate(final_agents[:3], 1):
            response += f"{i}. {agent['name']} - {agent['votes_received']} votes\n"
        
        await message.channel.send(response)

client.run('YOUR_BOT_TOKEN')
```

### Export to Database

```python
import sqlite3
from ai_hunger_games import create_simulation

# Run simulation
sim = create_simulation()
results = sim.run_simulation()

# Save to database
conn = sqlite3.connect('hunger_games.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS simulations (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        num_agents INTEGER,
        num_rounds INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY,
        simulation_id INTEGER,
        name TEXT,
        generation INTEGER,
        votes_received INTEGER,
        rounds_survived INTEGER,
        FOREIGN KEY (simulation_id) REFERENCES simulations (id)
    )
''')

# Insert data
sim_data = sim.get_simulation_data()
cursor.execute(
    "INSERT INTO simulations VALUES (NULL, ?, ?, ?)",
    (sim_data['metadata']['start_time'], len(results['final_agents']), 
     results['statistics']['total_rounds'])
)
sim_id = cursor.lastrowid

for agent in results['final_agents']:
    cursor.execute(
        "INSERT INTO agents VALUES (NULL, ?, ?, ?, ?, ?)",
        (sim_id, agent['name'], agent['generation'], 
         agent['votes_received'], agent['rounds_survived'])
    )

conn.commit()
conn.close()
```

Enjoy experimenting with AI Hunger Games! 🎮
