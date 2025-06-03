
# by default, we settle down in this region
AWS_REGION ?= eu-west-3

clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf .pytest_cache

venv: clean
	python3 -m venv venv

install:
	python -m pip install -r requirements.txt

build:
	sam build --use-container -t infrastructure/template.yaml

deploy-local:
	sam local start-api

deploy:
	@echo "Deploying to " ${env}
	# Extract env from the branch name

	sam deploy --resolve-s3 --template-file .aws-sam/build/template.yaml --stack-name multi-stack-${env} \
         --capabilities CAPABILITY_IAM --region ${AWS_REGION} --parameter-overrides EnvironmentName=${env} --no-fail-on-empty-changeset


serve:
	python -m uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

test:
	@echo "Running minimal tests for CI/CD..."
	python -m pytest tests/test_ci_minimal.py tests/test_minimal_fixed.py -v --tb=short --disable-warnings

test-all:
	@echo "Running all tests..."
	python -m pytest tests/ -v --tb=short --disable-warnings

test-unit:
	@echo "Running unit tests only..."
	python -m pytest tests/ -m unit -v --tb=short --disable-warnings

test-endpoint:
	@echo "Testing deployed AWS endpoint..."
	python tests/test_aws_deployment.py

configure-webhook:
	@echo "Configuring Telegram webhook for AWS deployment..."
	python tools/set_webhook_aws.py