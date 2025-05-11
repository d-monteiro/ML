.PHONY: env run deactivate

env:
	python3 -m venv venv
	@echo "Run 'source venv/bin/activate'"

run:
	python3 data_pipeline.py
	python3 features.py
	python3 model.py

run_single:
	python3 $(file)

stop:
	@echo "Run 'deactivate'"