.PHONY: test demo reviewer cold-start hiring-audit eval data training ablations dashboard page-qa reproduce release all

test:
	python -m pytest -q

demo:
	python demo.py

reviewer:
	python scripts/reviewer_demo.py

cold-start:
	python scripts/cold_start_audit.py

hiring-audit:
	python scripts/hiring_surface_audit.py

eval:
	python evals/run_eval.py --users 100 --turns 60 --seed 7

data:
	python data/generate_dataset.py --users 100 --turns 60
	python experiments/build_preference_data.py

training:
	python experiments/build_preference_data.py
	python scripts/audit_training_data.py
	python scripts/train_reward_baseline.py

ablations:
	python experiments/run_ablations.py

dashboard:
	python dashboard/build_dashboard.py

page-qa:
	python scripts/project_page_qa.py

reproduce:
	python scripts/reproduce.py

release:
	python scripts/build_manifest.py
	python scripts/release_check.py

all: test eval data training ablations dashboard
