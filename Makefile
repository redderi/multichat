.PHONY: run_t, run_w

run_t:
	uv run src/multichat/main.py -t

run_w:
	uv run src/multichat/main.py