"""
Jira API Client Module.

This module provides functionality to interact with the Jira API, including:
- Establishing connections
- Fetching issues by epic or project
- Extracting issue details
"""

from typing import List, Optional
from jira import JIRA, Issue

from src.config.config import Config


class JiraClient:
    """Client for interacting with the Jira API.
    
    This class provides methods to connect to Jira and perform various operations
    such as fetching issues and extracting their details.
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize the Jira client with configuration.
        
        Args:
            config: Configuration object containing Jira credentials and settings.
        """
        self.config = config
        self.client: Optional[JIRA] = None
    
    def connect(self) -> JIRA:
        """Establish connection to Jira and return the client instance.
        
        Returns:
            JIRA: Authenticated Jira client instance.
            
        Raises:
            Exception: If connection to Jira fails.
        """
        auth = (self.config.jira_user, self.config.jira_api_token)
        options = {"server": self.config.jira_server}
        
        try:
            self.client = JIRA(options=options, basic_auth=auth)
            self._validate_connection()
            return self.client
        except Exception as e:
            raise Exception(f"Failed to connect to Jira: {str(e)}")
    
    def _validate_connection(self) -> None:
        """Validate the Jira connection by checking projects and user info.
        
        Raises:
            Exception: If connection validation fails.
        """
        if not self.client:
            raise Exception("Jira client not initialized")
            
        try:
            current_user = self.client.current_user()
            print(f"Connected to Jira successfully!")
            print(f"Authenticated user: {current_user}")
        except Exception as e:
            raise Exception(f"Failed to validate Jira connection: {str(e)}")
    
    def fetch_issues_by_epic(self, epic_key: str) -> List[Issue]:
        """Fetch all issues linked to a specific epic.
        
        Args:
            epic_key: The key of the epic (e.g., 'PROJ-123').
            
        Returns:
            List[Issue]: List of issues linked to the epic.
            
        Raises:
            Exception: If client is not connected or fetch fails.
        """
        if not self.client:
            raise Exception("Jira client not connected")
            
        try:
            jql = f'"Epic Link" = {epic_key}'
            return self.client.search_issues(jql, maxResults=False)
        except Exception as e:
            raise Exception(f"Failed to fetch issues for epic {epic_key}: {str(e)}")
    
    def fetch_issues_by_project(self, project_key: str) -> List[Issue]:
        """Fetch all issues in a specific project.
        
        Args:
            project_key: The key of the project (e.g., 'PROJ').
            
        Returns:
            List[Issue]: List of issues in the project.
            
        Raises:
            Exception: If client is not connected or fetch fails.
        """
        if not self.client:
            raise Exception("Jira client not connected")
            
        try:
            jql = f'project = {project_key}'
            return self.client.search_issues(jql, maxResults=False)
        except Exception as e:
            raise Exception(f"Failed to fetch issues for project {project_key}: {str(e)}")
    
    @staticmethod
    def extract_issue_text(issue: Issue) -> str:
        """Extract relevant text from a Jira issue.
        
        Args:
            issue: The Jira issue object.
            
        Returns:
            str: Concatenated text from summary, description, and comments.
        """
        summary = issue.fields.summary or ""
        description = issue.fields.description or ""
        
        comments = []
        if hasattr(issue.fields, "comment"):
            for comment in issue.fields.comment.comments:
                comments.append(
                    f"Comment by {comment.author.displayName}: {comment.body}"
                )

        return "\n".join([
            f"Summary: {summary}",
            f"Description: {description}",
            *comments
        ])
