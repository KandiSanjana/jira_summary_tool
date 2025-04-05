# Dockerfile
FROM python:3.11-slim-buster

# Install system dependencies (wkhtmltopdf for PDF generation)
RUN apt-get update && apt-get install -y --no-install-recommends wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY jira_summary_tool/ jira_summary_tool/
COPY jira_summary_tool/main.py jira_summary_tool/main.py

# Set default environment (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1

# Entrypoint to run the CLI (by default, will show help without arguments)
ENTRYPOINT ["python", "-m", "jira_summary_tool.main"]
