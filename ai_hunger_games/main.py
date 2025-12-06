"""
Main entry point for AI Hunger Games simulation.
Run this file to start the simulation.
"""

import argparse
import sys
from simulation import create_simulation
from config import (
    NUM_AGENTS, NUM_ROUNDS, OLLAMA_MODEL, 
    VOTING_METHOD, DEFAULT_QUESTIONS
)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Hunger Games - Multi-Agent Evolution & Voting Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --rounds 10 --agents 12
  python main.py --model mistral --voting ranked-choice
  python main.py --questions "What is AI?" "How does evolution work?"
        """
    )
    
    parser.add_argument(
        '--agents',
        type=int,
        default=NUM_AGENTS,
        help=f'Number of agents to start with (default: {NUM_AGENTS})'
    )
    
    parser.add_argument(
        '--rounds',
        type=int,
        default=NUM_ROUNDS,
        help=f'Number of rounds to simulate (default: {NUM_ROUNDS})'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default=OLLAMA_MODEL,
        help=f'Ollama model to use (default: {OLLAMA_MODEL})'
    )
    
    parser.add_argument(
        '--voting',
        type=str,
        choices=['single-choice', 'ranked-choice'],
        default=VOTING_METHOD,
        help=f'Voting method (default: {VOTING_METHOD})'
    )
    
    parser.add_argument(
        '--questions',
        nargs='+',
        help='Custom questions to ask (space-separated)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )
    
    parser.add_argument(
        '--personalities',
        type=str,
        help='Path to custom personalities JSON file'
    )
    
    return parser.parse_args()


def print_banner():
    """Print welcome banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🎮  AI HUNGER GAMES  🎮                            ║
║                                                              ║
║        Multi-Agent Evolution & Voting Simulator              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point."""
    print_banner()
    
    # Parse arguments
    args = parse_arguments()
    
    # Display configuration
    print("⚙️  Configuration:")
    print(f"   Agents: {args.agents}")
    print(f"   Rounds: {args.rounds}")
    print(f"   Model: {args.model}")
    print(f"   Voting: {args.voting}")
    print(f"   Verbose: {not args.quiet}")
    print()
    
    # Prepare questions
    questions = None
    if args.questions:
        questions = args.questions
        print(f"📝 Using {len(questions)} custom questions")
    else:
        questions = DEFAULT_QUESTIONS[:args.rounds]
        print(f"📝 Using default questions")
    
    print()
    
    try:
        # Create simulation
        sim = create_simulation(
            num_agents=args.agents,
            num_rounds=args.rounds,
            model=args.model,
            voting_method=args.voting,
            verbose=not args.quiet
        )
        
        # Load personalities if custom file provided
        if args.personalities:
            print(f"📂 Loading personalities from: {args.personalities}")
            personalities = sim.load_initial_personalities(args.personalities)
            sim.initialize_agents(personalities)
        
        # Run simulation
        results = sim.run_simulation(questions)
        
        # Print final message
        if results:
            print("\n" + "="*60)
            print("✅ Simulation completed successfully!")
            print("="*60)
            print("\n🎉 Thank you for playing AI Hunger Games!")
            print("   Check the 'data' folder for detailed logs.\n")
        else:
            print("\n❌ Simulation failed. Please check Ollama connection.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulation interrupted by user.")
        print("   Partial results may be saved in the data folder.")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
