# AI Hunger Games - System Architecture

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAIN ENTRY POINT                            │
│                            (main.py)                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SIMULATION ENGINE                              │
│                       (simulation.py)                               │
│                                                                     │
│  • Initializes all components                                      │
│  • Manages round flow                                              │
│  • Coordinates agent interactions                                  │
└─┬─────────┬─────────┬──────────┬──────────┬───────────────────────┘
  │         │         │          │          │
  ▼         ▼         ▼          ▼          ▼
┌──────┐ ┌──────┐ ┌───────┐ ┌────────┐ ┌───────┐
│AGENTS│ │ LLM  │ │VOTING │ │EVOLVE  │ │LOGGER │
│      │ │      │ │       │ │        │ │       │
└──────┘ └──────┘ └───────┘ └────────┘ └───────┘


## Round Flow

ROUND START
    │
    ├─► [1] Present Question
    │       │
    │       ▼
    │   ┌─────────────────┐
    │   │  All Agents     │
    │   │  Generate       │
    │   │  Answers        │───► LLM Interface
    │   │  (via Ollama)   │     (llm_interface.py)
    │   └─────────────────┘
    │       │
    │       ▼
    ├─► [2] Collect All Answers
    │       │
    │       ▼
    │   ┌─────────────────┐
    │   │  All Agents     │
    │   │  Vote on        │
    │   │  Best Answer    │───► Voting System
    │   │  (w/ reasoning) │     (voting.py)
    │   └─────────────────┘
    │       │
    │       ▼
    ├─► [3] Tally Votes
    │       │
    │       ├─► Determine Winner (most votes)
    │       └─► Determine Loser (least votes)
    │           │
    │           ▼
    ├─► [4] Eliminate Loser
    │       │
    │       └─► Evolution Manager
    │           (evolution.py)
    │           │
    │           ├─► Remove agent from population
    │           └─► Record elimination details
    │               │
    │               ▼
    ├─► [5] Create Evolved Agent
    │       │
    │       ├─► Select parent (weighted by votes)
    │       ├─► Inherit personality traits
    │       ├─► Apply random mutations
    │       └─► Add to population
    │           │
    │           ▼
    ├─► [6] Log Round Data
    │       │
    │       └─► Logger
    │           (logger.py)
    │           │
    │           ├─► Save to JSON
    │           └─► Save to CSV
    │               │
    │               ▼
    └─► NEXT ROUND or END


## Data Flow

INPUT                     PROCESSING                    OUTPUT
┌────────────┐           ┌──────────────┐            ┌──────────────┐
│ Questions  │──────────►│  Simulation  │───────────►│ JSON Logs    │
└────────────┘           │    Engine    │            └──────────────┘
                         └──────────────┘
┌────────────┐                  │                    ┌──────────────┐
│Personalities│─────────►        │       ───────────►│ CSV Reports  │
└────────────┘                  │                    └──────────────┘
                                │
┌────────────┐                  │                    ┌──────────────┐
│Config File │─────────►        │       ───────────►│ Console Out  │
└────────────┘                  │                    └──────────────┘
                                │
                                ▼                    ┌──────────────┐
                         ┌──────────────┐           │ Web Dashboard│
                         │ Ollama API   │◄──────────┤ (Optional)   │
                         └──────────────┘           └──────────────┘


## Agent Lifecycle

CREATION                SURVIVAL                ELIMINATION
    │                       │                         │
    ▼                       ▼                         ▼
┌────────┐            ┌─────────┐              ┌──────────┐
│Initial │            │ Answer  │              │ Receive  │
│8 agents│────────────│Questions│──────────────│ Fewest   │
│ Gen 0  │            │  Vote   │              │  Votes   │
└────────┘            └─────────┘              └──────────┘
    │                       │                         │
    │                       ▼                         ▼
    │                  ┌─────────┐              ┌──────────┐
    │                  │Accumulate│             │ Removed  │
    │                  │  Votes   │             │   from   │
    │                  │  Memory  │             │Population│
    │                  └─────────┘              └──────────┘
    │                       │                         │
    │                       ▼                         ▼
    │                  ┌─────────┐              ┌──────────┐
    │                  │ Survive │              │  Logged  │
    │                  │ Multiple│              │Evolution │
    │                  │ Rounds  │              │ History  │
    │                  └─────────┘              └──────────┘
    │                       │
    └───────────────────────┼─────────────────────────┘
                            │
                            ▼
                      ┌──────────┐
                      │ Become   │
                      │ Parent   │────► NEW EVOLVED AGENT
                      │for Next  │      (Gen N+1)
                      │ Gen      │
                      └──────────┘


## API Architecture (Optional Web Interface)

┌─────────────────────────────────────────────────────────┐
│                    WEB BROWSER                          │
│                   (ui/index.html)                       │
│                                                         │
│  ┌────────────┐  ┌─────────────┐  ┌────────────────┐  │
│  │ Config     │  │  Start      │  │  Results       │  │
│  │ Form       │  │  Button     │  │  Display       │  │
│  └────────────┘  └─────────────┘  └────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Requests (JSON)
                         ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI SERVER                             │
│              (api/server.py)                            │
│                                                         │
│  POST /simulation/start   ──► Start simulation         │
│  GET  /simulation/status  ──► Get current status       │
│  GET  /simulation/results ──► Get final results        │
│  GET  /simulation/logs    ──► List all logs            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  Simulation Engine     │
            │  (runs in background)  │
            └────────────────────────┘


## Technology Stack

┌────────────────┬──────────────────────────────────┐
│ Component      │ Technology                       │
├────────────────┼──────────────────────────────────┤
│ Language       │ Python 3.9+                      │
│ LLM Provider   │ Ollama (Local)                   │
│ API Framework  │ FastAPI + Uvicorn                │
│ Frontend       │ HTML + CSS + Vanilla JavaScript  │
│ Data Format    │ JSON + CSV                       │
│ HTTP Client    │ requests library                 │
│ Type Hints     │ Native Python typing module      │
└────────────────┴──────────────────────────────────┘
```

## Key Design Principles

1. **Modularity** - Each component is independent and testable
2. **Type Safety** - Comprehensive type hints throughout
3. **Error Handling** - Graceful degradation and informative errors
4. **Logging** - Complete audit trail of all decisions
5. **Configurability** - Easy to customize without code changes
6. **Extensibility** - Simple to add new features
7. **Documentation** - Clear docstrings and comments

## File Dependencies

```
main.py
├── simulation.py
│   ├── agent.py
│   │   └── llm_interface.py
│   ├── voting.py
│   │   └── llm_interface.py
│   ├── evolution.py
│   │   └── agent.py
│   ├── logger.py
│   └── config.py
└── config.py

api/server.py
├── simulation.py (all dependencies above)
└── config.py
```
