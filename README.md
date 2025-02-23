# Calendar Assistant

A natural language calendar assistant that uses AI to help manage your Google Calendar events.

## Prerequisites

- Python 3.12+
- Poetry (Python package manager)
- Google Calendar API credentials
- OpenAI API key

## Setup

1. **Install Poetry**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Clone the repository**
```bash
git clone <repository-url>
cd calendar-assistant
```

3. **Install dependencies**
```bash
poetry install
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your-openai-api-key
```

5. **Set up Google Calendar API**
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a new project
- Enable the Google Calendar API
- Create OAuth 2.0 credentials
- Download the credentials and save as `credentials.json` in the project root

## Running the Application

1. **Start the virtual environment**
```bash
poetry shell
```

2. **Start the server**
```bash
python src/app.py
```

3. **In a new terminal, run the client**
```bash
python src/client/calendar_client.py
```

## Testing

1. **Create a test environment file**

Create a `.env.test` file in the root directory:
```bash
OPENAI_API_KEY=your-openai-api-key
```

2. **Run all tests**
```bash
pytest
```

3. **Run specific test files**
```bash
pytest src/tests/test_llm_service.py
```

4. **Run tests with verbose output**
```bash
pytest -v
```

## Project Structure
```
src/
├── __init__.py
├── app.py              # Main Flask application
├── routes/            
│   ├── __init__.py
│   ├── calendar_routes.py
│   ├── health_routes.py
│   └── nlp_routes.py
├── services/
│   ├── __init__.py
│   ├── calendar_service.py
│   ├── llm_service.py
│   └── nlp_service.py
├── client/
│   └── calendar_client.py
└── tests/
    ├── __init__.py
    ├── test_llm_service.py
    └── test_calendar_client.py
```

## Usage

After starting both the server and client:

1. The client will prompt you for natural language queries
2. Example queries:
   - "Schedule a team meeting tomorrow at 2pm for one hour"
   - "Create a dentist appointment next Friday at 3pm"
   - "Set up grocery shopping for Saturday morning"

## Development

1. **Adding new dependencies**
```bash
poetry add package-name
```

2. **Adding development dependencies**
```bash
poetry add --dev package-name
```

3. **Updating dependencies**
```bash
poetry update
```

## Common Issues

1. **"OPENAI_API_KEY environment variable is not set"**
   - Ensure your `.env` file exists and contains your OpenAI API key
   - Make sure you're running the application from the project root

2. **"credentials.json not found"**
   - Download OAuth credentials from Google Cloud Console
   - Save as `credentials.json` in project root

3. **"Could not connect to server"**
   - Ensure the Flask server is running (`python src/app.py`)
   - Check that you're using the correct port (default: 5000)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
