help: ## Print a help section for all the make commands
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

env: ## Install all the dependencies
	@python3 -m venv .venv
	. ./.venv/bin/activate && pip install -r requirements.txt

freeze: ## Freeze python dependencies
	@. ./.venv/bin/activate && pip freeze > requirements.txt

lab: ## Spin up jupyter lab
	. ./.venv/bin/activate && jupyter lab
