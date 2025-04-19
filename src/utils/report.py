# report.py
import logging
import os
from collections import Counter
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from jira import Issue

logger = logging.getLogger(__name__)

@dataclass
class ReportConfig:
    output_dir: str
    chart_colors: List[str] = None

    def __post_init__(self):
        if self.chart_colors is None:
            self.chart_colors = ['#36A2EB', '#FF6384', '#FFCE56', '#32a852', '#a8329e']

class ReportGenerator:
    def __init__(self, config: ReportConfig):
        self.config = config
        os.makedirs(config.output_dir, exist_ok=True)

    def _generate_chart_data(self, issues: List[Issue]) -> Dict[str, Any]:
        """Generate data for the status chart."""
        statuses = [issue.fields.status.name for issue in issues]
        status_data = {}
        for status, count in Counter(statuses).items():
            status_data[status] = count

        issues_values = {}
        for issue in issues:
            issues_values[issue] = {
                "status": issue.fields.status or "",
                "assignee": issue.fields.assignee or "",
                "summary": issue.fields.summary or "",
                "update": issue.fields.comment
            }
        
        return {
            "total_issues": len(issues),
            'status_counts': status_data,
            'issue_values': issues_values,
        }
    
    def _generate_chart_script(self, chart_data: Dict[str, Any]) -> str:
        """Generate the JavaScript code for the chart."""
        return f"""
        <script>
            var ctx = document.getElementById('statusChart').getContext('2d');
            var chart = new Chart(ctx, {{
                type: 'pie',
                data: {{
                    labels: {list(chart_data.keys())},
                    datasets: [{{
                        data: {list(chart_data.values())},
                        backgroundColor: {self.config.chart_colors}
                    }}]
                }}
            }});
        </script>
        """

    def _generate_table_script(self, chart_data: Dict[str, Any]) -> str:
        """Generate the HTML code for the table."""
        table_rows = ""

        for key, val in chart_data.items():
            table_rows += f"""
            <tr>
                <td>{key}</td>
                <td>{val['summary']}</td>
                <td>{val['status']}</td>
                <td>{val['assignee']}</td>
                <td>{val['update']}</td>
            </tr>
            """

        return f"""
        <table class="issues-table">
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Summary</th>
                    <th>Status</th>
                    <th>Assignee</th>
                    <th>Update</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """
    
    def _generate_css_content(self) -> str:
        """Generate the HTML code for the report"""
        return """
        <style>
            :root {
            --primary: #0052cc;
            --accent: #36cfc9;
            --success: #28a745;
            --warning: #ffc107;
            --light: #f4f6f8;
            --dark: #1a1a1a;
            --white: #ffffff;
            --radius: 12px;
            --shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
            }

            * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            }

            body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--light);
            color: var(--dark);
            padding: 2rem;
            line-height: 1.6;
            }

            .dashboard {
            max-width: 1200px;
            margin: 0 auto;
            animation: fadeIn 1s ease;
            }

            h1 {
                text-align: center;
                font-size: 2.5rem;
                font-weight: 600;
                margin-bottom: 2rem;
                color: var(--primary);
            }

            .top-section {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 2rem;
                animation: slideIn 0.8s ease;
            }

            .summary-cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); /* slightly smaller min-width */
                gap: 0.75rem; /* tighter spacing */
            }

            .card {
            background-color: var(--white);
            border-radius: var(--radius);
            padding: 0.75rem 1rem; /* more compact padding */
            box-shadow: var(--shadow);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
            }

            .card h2 {
            font-size: 0.9rem; /* smaller header */
            color: var(--primary);
            margin-bottom: 0.3rem;
            }

            .card p {
            font-size: 1.25rem; /* reduced from 1.5rem */
            font-weight: 600;
            color: var(--dark);
            }

            .chart-container {
            background-color: var(--white);
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: center;
            height: 300px; /* Set fixed height to match the summary below */
            }

            .highlights {
            background: var(--white);
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            margin-top: 2rem;
            animation: fadeIn 1.2s ease;
            }

            .highlights h3 {
            color: var(--primary);
            margin-bottom: 0.75rem;
            }

            .issues-table {
            margin-top: 2rem;
            width: 100%;
            border-collapse: collapse;
            background: var(--white);
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            animation: fadeIn 1.3s ease;
            }

            .issues-table th,
            .issues-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #eaeaea;
            }

            .issues-table th {
            background-color: #f5f7fa;
            color: #333;
            font-weight: 600;
            }

            .issues-table td {
            color: #444;
            }

            .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 500;
            color: white;
            }

            .update-field {
            max-width: 200px;
            word-wrap: break-word;
            color: #555;
            font-size: 0.9rem;
            }

            @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
            }

            @keyframes slideIn {
            0% { opacity: 0; transform: translateX(-40px); }
            100% { opacity: 1; transform: translateX(0); }
            }

            @media (max-width: 768px) {
            .top-section {
                grid-template-columns: 1fr;
            }

            .chart-container {
                margin-top: 1rem;
            }

            .dashboard {
                display: flex;
                gap: 2rem;
                justify-content: space-between;
                align-items: flex-start;
                flex-wrap: wrap;
            }

            .chart-container canvas {
                max-width: 100%;
                height: auto;
            }
        </style>
        """

    def _generate_html_content(self, data: Dict[str, Any], summaries: str) -> str:
        """Generate the HTML content for the dashboard."""

        total_issues = data.get("total_issues")
        chart_data = data.get("status_counts")
        # in_progress_count = chart_data
        
        table_data = data.get("issue_values")

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Jira Summary Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        {self._generate_css_content()}
        </head>
        <body>
        <div class="dashboard">
            <h1>Jira Summary Dashboard</h1>

            <div class="top-section">
            <!-- Left section with summary cards -->
            <div class="summary-cards">
                <div class="card">
                <h2>Total Issues</h2>
                <p>{total_issues}</p>
                </div>
                <div class="card">
                <h2>Completed</h2>
                <p>18</p>
                </div>
                <div class="card">
                <h2>In Progress</h2>
                <p>12</p>
                </div>
            </div>

            <!-- Right section with chart container -->
            <div class="chart-container">
                <canvas id="statusChart" width="300" height="300"></canvas>
            </div>
            </div>

            <!-- High-Level Summary placed below the widgets -->
            <div class="highlights">
            <h3>High-Level Summary</h3>
            <p>The sprint focused on improving the authentication module, optimizing database queries, and fixing bugs in the UI layer. The team worked hard to address high-priority issues, including optimizing search queries and implementing additional security measures.</p>
            </div>

            {self._generate_table_script(table_data)}
            
        </div>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        {self._generate_chart_script(chart_data)}
        </body>
        </html>
        """

    def generate_html_dashboard(self, issues: List[Issue], summaries: str) -> str:
        """
        Generate an HTML dashboard with status visualization.
        
        Args:
            issues: List of Jira issues
            summaries: Text summaries of the issues
            
        Returns:
            Path to the generated HTML file
        """
        try:
            chart_data = self._generate_chart_data(issues)
            html_content = self._generate_html_content(chart_data, summaries)
            
            output_path = os.path.join(self.config.output_dir, "summary.html")
            
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(html_content)
        
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate HTML dashboard: {e}")
            raise

    def generate_pdf_report(self, issues: List[Issue], summaries: str) -> str:
        """
        Generate a PDF report from the HTML dashboard.
        
        Args:
            issues: List of Jira issues
            summaries: Text summaries of the issues
            
        Returns:
            Path to the generated PDF file
        """
        try:
            html_path = self.generate_html_dashboard(issues, summaries)
            pdf_path = os.path.join(self.config.output_dir, "report.pdf")
            
            # TODO: Implement PDF generation when pdfkit is properly configured
            # pdfkit.from_file(html_path, pdf_path)
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {e}")
            raise
