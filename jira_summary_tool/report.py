# report.py
import pdfkit, os
from collections import Counter

def generate_html_dashboard(issues, summaries, cfg):
    # Calculate status breakdown for chart
    statuses = [issue.fields.status.name for issue in issues]
    status_counts = Counter(statuses)
    # Prepare data for Chart.js
    chart_data = {
        'labels': list(status_counts.keys()),
        'values': list(status_counts.values())
    }
    # Build HTML content
    html_parts = []
    html_parts.append("<html><head><title>Jira Summary Dashboard</title>")
    # Include Chart.js via CDN
    html_parts.append("<script src='https://cdn.jsdelivr.net/npm/chart.js'></script></head><body>")
    html_parts.append("<h1>Jira Issue Summary Report</h1>")
    # Insert a canvas for the chart
    html_parts.append("<h2>Issue Status Breakdown</h2><canvas id='statusChart' width='400' height='400'></canvas>")
    # Script to render the chart
    html_parts.append(f"""
    <script>
      var ctx = document.getElementById('statusChart').getContext('2d');
      var chart = new Chart(ctx, {{
          type: 'pie',
          data: {{
              labels: {chart_data['labels']},
              datasets: [{{
                  data: {chart_data['values']},
                  backgroundColor: ['#36A2EB','#FF6384','#FFCE56','#32a852','#a8329e']
              }}]
          }}
      }});
    </script>
    """)
    # List issues with summaries
    html_parts.append("<h2>Issue Summaries</h2><ul>")
    for issue, (issue_key, high_level, detailed) in zip(issues, summaries):
        html_parts.append(f"<li><b>{issue_key} - {issue.fields.summary}</b> ({issue.fields.status.name})")
        html_parts.append(f"<p><i>High-level:</i> {high_level}</p>")
        html_parts.append(f"<p><i>Detailed:</i> {detailed}</p></li>")
    html_parts.append("</ul>")
    html_parts.append("</body></html>")
    html_content = "".join(html_parts)
    # Write to an HTML file
    output_path = os.path.join(cfg.output_dir, "dashboard.html")
    with open(output_path, "w") as f:
        f.write(html_content)
    return output_path

def generate_pdf_report(issues, summaries, cfg):
    # Reuse the dashboard HTML (or generate a separate print-friendly HTML)
    html_path = generate_html_dashboard(issues, summaries, cfg)
    pdf_path = os.path.join(cfg.output_dir, "report.pdf")
    # Convert the HTML file to PDF
    pdfkit.from_file(html_path, pdf_path)
    return pdf_path
