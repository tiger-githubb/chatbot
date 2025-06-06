# by default, we settle down in this region
AWS_REGION ?= eu-west-3

.PHONY: clean venv install build deploy-local deploy serve test test-jenkins test-endpoint

clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf test-results

venv: clean
	python3 -m venv venv

install:
	venv/bin/pip install -r requirements.txt

build:
	sam build --use-container -t infrastructure/template.yaml

deploy-local:
	sam local start-api

deploy:
	@echo "Deploying to " ${env}
	# Extract env from the branch name
	@if [ -f .env ]; then \
		echo "Loading environment variables from .env..."; \
		TELEGRAM_BOT_TOKEN=$$(grep '^TELEGRAM_BOT_TOKEN' .env | cut -d'=' -f2 | tr -d ' '); \
		MISTRAL_API_KEY=$$(grep '^MISTRAL_API_KEY' .env | cut -d'=' -f2 | tr -d ' '); \
		TELEGRAM_WEBHOOK_URL=$$(grep '^TELEGRAM_WEBHOOK_URL' .env | cut -d'=' -f2 | tr -d ' ' || echo ""); \
		sam deploy --resolve-s3 --template-file .aws-sam/build/template.yaml --stack-name multi-stack-${env} \
			--capabilities CAPABILITY_IAM --region ${AWS_REGION} \
			--parameter-overrides \
			EnvironmentName=${env} \
			TelegramBotToken="$$TELEGRAM_BOT_TOKEN" \
			MistralApiKey="$$MISTRAL_API_KEY" \
			TelegramWebhookUrl="$$TELEGRAM_WEBHOOK_URL" \
			--no-fail-on-empty-changeset; \
	else \
		echo "Error: .env file not found. Cannot deploy without environment variables."; \
		exit 1; \
	fi

serve:
	venv/bin/fastapi dev src/main.py

test:
	@echo "Running tests..."
	PYTHONPATH=. venv/bin/pytest tests/ --ignore=tools/

test-jenkins:
	@echo "Running Jenkins tests with environment validation..."
	@if [ -f .env ]; then \
		echo "Environment file found, validating..."; \
		sed 's/ *= */=/g' .env > .env.clean && \
		export $$(cat .env.clean | grep -v '^#' | grep -v '^$$' | xargs) && \
		PYTHONPATH=. venv/bin/pytest tests/ --ignore=tools/ -v; \
	else \
		echo "Warning: No .env file found"; \
		PYTHONPATH=. venv/bin/pytest tests/ --ignore=tools/ -v; \
	fi

test-endpoint:
	@echo "Running endpoint tests..."
	aws cloudformation describe-stacks --stack-name multi-stack-${env} --region ${AWS_REGION} \
		--query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text | xargs -I {} curl -X GET {}

format:
	@echo "Formatting code with black..."
	venv/bin/black src/ tests/

lint:
	@echo "Linting code with flake8..."
	venv/bin/flake8 src/ tests/

quality: format lint
	@echo "All quality checks passed!"

security-scan:
	@echo "Running security scans..."
	venv/bin/bandit -r src/ -f json -o bandit-report.json