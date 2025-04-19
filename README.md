# Jira Summary Tool

A command-line tool for generating summaries and reports from Jira issues, with AI-powered summarization capabilities.

## Features

- 🔍 Fetch issues from Jira by epic or project
- 🤖 AI-powered summarization using Cohere
- 📊 Generate HTML dashboard reports with status visualization
- 📈 Track issue status distribution
- 🚀 Easy-to-use CLI interface
- 🐳 Docker support for easy deployment

## Prerequisites

- Python 3.11 or higher
- Docker (optional)
- Jira API access
- Cohere API key

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd jira-summary-tool
   ```

2. Create a `.env` file with your credentials:
   ```env
   # Jira API Configuration
   JIRA_SERVER=your-jira-server-url
   JIRA_USER=your-jira-username
   JIRA_API_TOKEN=your-jira-api-token

   # Cohere API Configuration
   COHERE_API_KEY=your-cohere-api-key

   # Application Configuration
   MODE=production
   ```

3. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd jira-summary-tool
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (same as Docker method)

## Usage

### Basic Commands

```bash
# Show help
jira-summary-tool --help

# Show version
jira-summary-tool --version

# Generate summary for an epic
jira-summary-tool epic ABC-123 --output-dir ./reports

# Generate summary for a project
jira-summary-tool project ABC --output-dir ./reports

# List all the project for a user
jira-summary-tool list --type projects

# Set log level
jira-summary-tool --log-level DEBUG epic ABC-123
```

### Output

The tool generates:
1. HTML dashboard with status visualization
2. Text summaries of issues
3. Log files for debugging

Output files are saved in the specified `--output-dir` (defaults to `./outputs`).

## Report Format

The generated HTML dashboard includes:
- Status distribution pie chart
- Issue summaries
- Project/Epic overview
- Detailed issue information

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| JIRA_SERVER | Jira server URL | Yes |
| JIRA_USER | Jira username | Yes |
| JIRA_API_TOKEN | Jira API token | Yes |
| COHERE_API_KEY | Cohere API key | Yes |
| MODE | Application mode (development/production) | No |
| LOG_LEVEL | Logging level | No |

### Logging

The tool supports multiple log levels:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Logs are written to both console and file (`app.log`).

## Development

### Running Tests

```bash
# Using Docker
docker-compose run jira-summary-tool pytest

# Locally
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]

## Support

For support, please [add your support contact information]
