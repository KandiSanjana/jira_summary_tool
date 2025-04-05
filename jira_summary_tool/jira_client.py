# jira_client.py
from jira import JIRA

def connect_jira(cfg):
    """Connect to Jira and return a JIRA client instance."""
    auth = (cfg.jira_user, cfg.jira_api_token)
    options = {"server": cfg.jira_server}
    jira = JIRA(options=options, basic_auth=auth)
    return jira

def fetch_issues_by_epic(jira, epic_key):
    jql = f'"Epic Link" = {epic_key} AND assignee = currentUser()'
    issues = jira.search_issues(jql, maxResults=False)  # maxResults=False to fetch all
    return issues

def fetch_issues_by_project(jira, project_key):
    jql = f'project = {project_key} AND assignee = currentUser()'
    issues = jira.search_issues(jql, maxResults=False)
    return issues

def extract_issue_text(issue):
    """Extract relevant text from a Jira issue (summary, description, comments)."""
    summary = issue.fields.summary or ""
    description = issue.fields.description or ""
    # Concatenate all comments text
    comments = ""
    if hasattr(issue.fields, "comment"):
        for comment in issue.fields.comment.comments:
            comments += f"\nComment by {comment.author.displayName}: {comment.body}"
    text = f"Summary: {summary}\nDescription: {description}\n{comments}"
    return text
