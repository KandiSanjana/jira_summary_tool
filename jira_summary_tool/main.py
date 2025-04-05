# main.py
import sys, argparse, logging
from jira_summary_tool import config, logger, jira_client, summarizer, report

def main():
    cfg = config.load_config()
    logger.setup_logging(cfg)
    log = logging.getLogger("jira_summary_tool")
    
    parser = argparse.ArgumentParser(description="Fetch Jira issues and generate summaries.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--epic", help="Epic issue key (e.g. ABC-123) to fetch all child issues")
    group.add_argument("--project", help="Project key (e.g. ABC) to fetch issues from")
    args = parser.parse_args()
    
    try:
        log.info("🚀 Starting Jira summarization tool")
        jira = jira_client.connect_jira(cfg)
        # Fetch issues based on input
        if args.epic:
            issues = jira_client.fetch_issues_by_epic(jira, args.epic)
            context = f"epic {args.epic}"
        else:
            issues = jira_client.fetch_issues_by_project(jira, args.project)
            context = f"project {args.project}"
        log.info(f"Fetched {len(issues)} issues from {context}")
        
        # Summarize each issue
        summaries = []
        for issue in issues:
            text = jira_client.extract_issue_text(issue)
            high_level, detailed = summarizer.summarize_issue(text, cfg)
            summaries.append((issue.key, high_level, detailed))
            log.debug(f"Summarized issue {issue.key}: {high_level[:50]}...")
        
        # Generate reports
        html_path = report.generate_html_dashboard(issues, summaries, cfg)
        pdf_path = report.generate_pdf_report(issues, summaries, cfg)
        log.info(f"📊 Dashboard generated: {html_path}")
        log.info(f"📝 PDF report generated: {pdf_path}")
        log.info("✅ Jira summarization completed successfully!")
    except Exception as e:
        log.error(f"Error: {e}")
        log.debug("Exception details: ", exc_info=True)  # Log traceback in debug file log
        print(f"An error occurred: {e}. See log file for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
