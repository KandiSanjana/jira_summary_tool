# Build stage
FROM python:3.11-slim-buster as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy setup files and dependencies
COPY setup.py requirements.txt ./
COPY src/ src/

# Install the package using setuptools
RUN pip install --no-cache-dir .

# Final stage
FROM python:3.11-slim-buster

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Set working directory
WORKDIR /app

# Copy application source for runtime (not strictly needed, but optional for CLI debugging/logging)
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser outputs/ outputs/
COPY --chown=appuser:appuser tests/ tests/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Run the CLI command
# CMD ["jira_summary_tool", "project", "JST"]
CMD ["sh", "-c", "jira_summary_tool && while true; do sleep 30; done"]