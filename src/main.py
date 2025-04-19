"""
Jira Summary Tool CLI.

This module provides the command-line interface for the Jira Summary Tool,
using Click for argument parsing and command handling.
"""

import sys
import logging
from typing import List

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.client.client import JiraClient
from src.config.config import load_config
import src.config.logger as logger
import src.utils.summarizer as summarizer
import src.utils.report as report


# Initialize console for rich output
console = Console()


@click.group()
@click.version_option(version="1.0.0")
@click.option(
    "--log-level",
    envvar="LOG_LEVEL",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level",
)
def cli(log_level: str) -> None:
    """Jira Summary Tool - Generate summaries and reports from Jira issues."""
    logger.setup_logging(log_level)
    
    # Set log level from CLI
    logging.getLogger().setLevel(log_level)


# @cli.command()
# @click.argument("epic_key")
# @click.option(
#     "--output-dir",
#     type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
#     default="./outputs",
#     help="Directory to save generated reports",
# )
# def epic(epic_key: str, output_dir: str) -> None:
#     """Generate summary for all issues in an epic.
    
#     EPIC_KEY is the key of the epic (e.g., ABC-123).
#     """
#     log = logging.getLogger("jira_summary_tool")
    
#     try:
#         console.print(Panel.fit("🚀 Starting Jira summarization tool"))
        
#         # Initialize client and fetch issues
#         client = JiraClient(load_config())
#         jira = client.connect()
#         issues = client.fetch_issues_by_epic(epic_key)
        
#         log.info(f"Fetched {len(issues)} issues from epic {epic_key}")
        
#         # Process issues
#         text = "\n".join(client.extract_issue_text(issue) for issue in issues)
#         high_level = summarizer.summarize_issue(text, load_config())
        
#         # Generate reports
#         html_path = report.generate_html_dashboard(issues, high_level, load_config())
        
#         console.print(Panel.fit(
#             f"📊 Dashboard generated: {html_path}\n"
#             f"✅ Jira summarization completed successfully!",
#             title="Success",
#             border_style="green"
#         ))
        
#     except Exception as e:
#         log.error(f"Error: {e}")
#         log.debug("Exception details:", exc_info=True)
#         console.print(Panel.fit(
#             f"❌ An error occurred: {e}\nSee log file for details.",
#             title="Error",
#             border_style="red"
#         ))
#         sys.exit(1)


@cli.command()
@click.argument("project_key")
@click.option(
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    default="./outputs",
    help="Directory to save generated reports",
)
def project(project_key: str, output_dir: str) -> None:
    """Generate summary for all issues in a project.
    
    PROJECT_KEY is the key of the project (e.g., ABC).
    """
    log = logging.getLogger("jira_summary_tool")
    
    try:
        console.print(Panel.fit("🚀 Starting Jira summarization tool"))
        
        # Load config
        config = load_config()

        # Initialize client and fetch issues
        client = JiraClient(config)
        client.connect()
        issues = client.fetch_issues_by_project(project_key)
        # Process issues
        text = "\n".join(client.extract_issue_text(issue) for issue in issues)

        # # Get a summary
        # high_level = summarizer.Summarizer(config.cohere_api_key).summarize_issue(text)
        
        # # Generate reports
        # html_path = report.ReportGenerator(
        #     report.ReportConfig(config.output_dir)
        #     ).generate_html_dashboard(issues, high_level)

        # Generate reports
        html_path = report.ReportGenerator(
            report.ReportConfig(config.output_dir)
            ).generate_html_dashboard(issues, text)
        
        console.print(Panel.fit(
            f"📊 Dashboard generated: {html_path}\n"
            f"✅ Jira summarization completed successfully!",
            title="Success",
            border_style="green"
        ))
        
    except Exception as e:
        log.error(f"Error: {e}")
        log.debug("Exception details:", exc_info=True)
        console.print(Panel.fit(
            f"❌ An error occurred: {e}\nSee log file for details.",
            title="Error",
            border_style="red"
        ))
        sys.exit(1)

@cli.command()
@click.option(
    "--type",
    type=click.Choice(["projects"]),
    help="Set the entity you want to list",
)
def list(type: str) -> None:
    """List all projects/epics available to the user.
    
    type is the entity type  (e.g., project/epic).
    """
    log = logging.getLogger("jira_summary_tool")
    
    try:
        console.print(Panel.fit("🚀 Starting Jira summarization tool"))
        
        # Load config
        config = load_config()

        # Initialize client and fetch issues
        client = JiraClient(config)
        client.connect()
        
        data = []
        if type == "projects":
            data = client.client.projects()

            table = Table(show_header=True, header_style="bold blue", title="Jira Projects")
            table.add_column("Key", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("ID", style="magenta")

            for project in data:
                table.add_row(project.key, project.name, project.id)

        console.print(Panel.fit(
            table,
        ))
        
    except Exception as e:
        log.error(f"Error: {e}")
        log.debug("Exception details:", exc_info=True)
        console.print(Panel.fit(
            f"❌ An error occurred: {e}\nSee log file for details.",
            title="Error",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == "__main__":
    # Load envs
    load_config()

    # Run the CLI tool
    cli()
