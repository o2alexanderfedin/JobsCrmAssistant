# JobsCRM Assistant

An AI-powered swarm of agents designed to automate and optimize the job search and application process.

## Overview

JobsCRM Assistant is an intelligent system that leverages multiple AI agents working together to streamline the job search and application process. The system helps job seekers by automating various aspects of the job search, from finding relevant positions to managing communications with recruiters and hiring managers.

## Features

- **Job Search Agent**: Automatically searches and identifies relevant job positions based on user preferences and qualifications
- **Application Agent**: Handles the job application process, including form filling and submission
- **Communication Agent**: Manages interactions with recruiters and hiring managers
- **Resume Optimization Agent**: Analyzes job requirements and suggests resume improvements
- **Follow-up Agent**: Handles post-interview communications and follow-ups
- **Analytics Agent**: Tracks application status and provides insights on the job search process

## Project Structure

```
JobsCRMAssistant/
├── agents/           # Individual agent implementations
├── core/            # Core functionality and shared components
├── data/            # Data storage and management
├── api/             # API integrations (job boards, email, etc.)
├── utils/           # Utility functions and helpers
└── config/          # Configuration files
```

## Setup

These steps install the package from `pyproject.toml` and start the API
server.

```bash
git clone https://github.com/o2alexanderfedin/JobsCrmAssistant.git
cd JobsCrmAssistant
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

`requirements.txt` is not the install path: it does not install the
package itself, so the server cannot find `jobs_crm_assistant`.

### Environment variables

Set them in the shell, or in a `.env` file in the directory you start
the server from.

- `OPENAI_API_KEY`: your OpenAI API key. The current API does not call
  OpenAI yet, so the server also starts without it.
- `CORS_ORIGINS`: the websites allowed to call the API from a browser,
  as a JSON list, for example `CORS_ORIGINS='["http://localhost:3000"]'`.
  A plain URL without the brackets and quotes stops the server at
  startup. The default is an empty list: no other website may call it.

```bash
export OPENAI_API_KEY=sk-your-key
```

### Run the server

```bash
uvicorn jobs_crm_assistant.api.app:app
```

Then open http://127.0.0.1:8000/health (it answers
`{"status":"healthy"}`) or http://127.0.0.1:8000/docs.

### Run the tests and checks

```bash
pytest
pre-commit run --all-files
```

## Requirements

- Python 3.9 or newer (see `pyproject.toml`)
- OpenAI API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Contact

For questions and support, please open an issue in the repository.
