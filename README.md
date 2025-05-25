# ChatBot Project

A serverless AI-powered chatbot application built with FastAPI and Mistral AI, deployed to AWS Lambda using SAM.

## Overview

This project implements a conversational chatbot that leverages the Mistral AI API for natural language processing. The application is designed as a serverless solution that runs on AWS Lambda and uses DynamoDB for conversation history storage.

## Features

- **AI-Powered Responses**: Integrates with Mistral AI to generate intelligent responses
- **Conversation Management**: Tracks conversations with unique IDs and maintains conversation history
- **RESTful API**: Complete API for chat interactions and conversation management
- **Serverless Architecture**: Deployed as AWS Lambda function
- **CI/CD Pipeline**: Automated testing and deployment with Jenkins

## Architecture

- **API Layer**: FastAPI application with Mangum adapter for AWS Lambda
- **AI Integration**: Mistral AI client for generating responses
- **Data Storage**: DynamoDB for storing conversation history
- **Infrastructure**: AWS SAM template for CloudFormation deployment

## Prerequisites

- Python 3.12+
- AWS CLI configured with appropriate permissions
- AWS SAM CLI
- Mistral AI API key

## Setup

1. Clone the repository:

   ```
   git clone <repository-url>
   cd chatbot
   ```

2. Create and activate a virtual environment:

   ```
   make venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   make install
   ```

4. Create a `.env` file with the following variables:
   ```
   ENV_NAME=local
   AWS_REGION_NAME=eu-west-3
   DYNAMO_TABLE=your-dynamo-table-name
   AWS_PROFILE=your-aws-profile
   MISTRAL_API_KEY=your-mistral-api-key
   ```

## Development

### Running locally

Start the API locally with:

```
make serve
```

Or using SAM local:

```
make deploy-local
```

### Testing

Run unit tests:

```
make test
```

## Deployment

### Building the application

Build the SAM application:

```
make build
```

### Deploying to AWS

Deploy to AWS environment:

```
make deploy env=dev
```

Available environments:

- `aristidekarbou`
- `dev`
- `dev-branch`

### Testing deployed endpoint

After deployment, you can test the endpoint with:

```
make test-endpoint env=dev
```

## API Endpoints

- `GET /`: Redirects to API documentation
- `GET /chat?question=<question>`: Send a question to the chatbot
- `POST /conversation/start`: Start a new conversation
- `GET /conversation/{conversation_id}/history`: Get conversation history
- `POST /conversation/message`: Save a conversation message
- `GET /conversation/history/{telegram_id}`: Get user conversation history
- `POST /conversation/{conversation_id}/close`: Close a conversation
- `GET /conversation/active/{telegram_id}`: Get user's last active conversation

## CI/CD Pipeline

The project includes a Jenkins pipeline that:

1. Sets up the environment
2. Injects environment variables
3. Runs unit tests
4. Builds the application
5. Deploys to AWS
6. Tests the deployed endpoint

## Project Structure

```
.
├── .env                  # Environment variables (not in git)
├── Jenkinsfile           # CI/CD pipeline definition
├── Makefile              # Build automation
├── infrastructure/       # AWS SAM templates
│   └── template.yaml     # CloudFormation template
├── src/                  # Application source code
│   ├── config.py         # Configuration management
│   ├── main.py           # FastAPI application
│   └── utils.py          # Utility functions
└── tests/                # Unit tests
    └── test_main.py      # API tests
```

## License

This project is created for educational purposes.
