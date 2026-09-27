# Failure-driven trajectory training data

This artifact turns evaluation failures into explicit correction pairs. It demonstrates the data-flywheel plumbing; it is not evidence that a frontier model has been post-trained on these pairs.

- Trajectories: 800
- False-accept correction pairs: 254

Each pair is generated only when a weaker grader accepts a gold-failing trajectory and the robust evidence-recomputing grader rejects it.

## Files

- `data/agent_trajectories.jsonl`
- `data/trajectory_failure_pairs.jsonl`
- `data/trajectory_corrections.jsonl`
