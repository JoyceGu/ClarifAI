# ClarifAI - Requirement Management and Optimization System

ClarifAI is an intelligent requirement management system designed to help Product Managers (PMs) better formulate and refine product requirements, enabling researchers and data scientists to solve problems more efficiently.

## Key Features

### 1. User Authentication
- Support for multi-role login (PM/Researcher)
- Test accounts provided:
  - PM account: pm@test.com / password123
  - Researcher account: researcher@test.com / password123

### 2. PM Requirement Submission Interface
- Business goal and data scope definition
- File upload support
- Expected output selection
- Timeline setting
- AI intelligent feedback based on Azure OpenAI (GPT-4o-mini)
- "Verify Requirement" feature for real-time AI analysis
- Requirement Scorecard including:
  - Clarity
  - Feasibility
  - Completeness

### 3. Researcher Feedback Interface
- View requirement details
- Provide solutions
- Interactive discussion with PMs

## Technology Stack

- Backend: FastAPI
- Frontend: HTML + CSS + JavaScript
- Database: SQLite
- AI Model: Azure OpenAI GPT-4o-mini for requirement analysis

## Project Structure

```
ClarifAI/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── ai_service.py        # Azure OpenAI integration
│   ├── models/              # Data models
│   ├── routers/             # API routes
│   ├── static/              # Static files
│   └── templates/           # HTML templates
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (not tracked by Git)
└── README.md                # Project documentation
```

## Installation and Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Azure OpenAI:
Create a `.env` file in the root directory with the following content:
```
# Azure OpenAI API Configuration
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Access the system:
Open your browser and go to http://localhost:8000

## Using the Requirement Verification Feature

1. Fill out all fields in the requirement form
2. Click the "Verify Requirement" button
3. The system will analyze your requirement using Azure OpenAI and provide:
   - Clarity Score
   - Feasibility Score
   - Completeness Score
   - Detailed feedback with suggestions for improvement
4. If the Clarity Score is at least 70%, the "Submit Requirement" button will be enabled
5. Make any necessary improvements based on the AI feedback
6. Submit the finalized requirement when ready 