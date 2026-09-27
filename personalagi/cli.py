from __future__ import annotations
import argparse
import json
from pathlib import Path
from personalagi.agent.core import PersonalAGIAgent
from personalbench.runner import run_detailed_comparison


def _demo() -> int:
    agent = PersonalAGIAgent('demo-user')
    messages = [
        'I prefer concise answers.',
        'My goal is finish my conference talk by Friday.',
        'I prefer working in the evening.',
        "Keep me on track, but don't nag me.",
        'Actually, mornings work better for me now.',
    ]
    for message in messages:
        agent.observe(message)
    decision = agent.proactive_decision(
        goal_relevance=.95, urgency=.9, confidence=.91,
        stakes=.2, reversibility=.95, interruptibility=.8,
    )
    print(json.dumps({
        'state': agent.explain_state(),
        'decision': {
            'action': decision.action.value,
            'score': decision.score,
            'confidence': decision.confidence,
            'factors': decision.factors,
        },
    }, indent=2, default=str))
    return 0


def _eval(args: argparse.Namespace) -> int:
    result = run_detailed_comparison(args.users, args.turns, args.seed)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2))
        print(path)
    else:
        print(json.dumps(result, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='personametrica', description='PersonaMetrica research prototype')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('demo', help='Run a deterministic longitudinal demo')
    p_eval = sub.add_parser('eval', help='Run PersonalBench comparison')
    p_eval.add_argument('--users', type=int, default=100)
    p_eval.add_argument('--turns', type=int, default=60)
    p_eval.add_argument('--seed', type=int, default=7)
    p_eval.add_argument('--output')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == 'demo':
        return _demo()
    if args.command == 'eval':
        return _eval(args)
    return 2
