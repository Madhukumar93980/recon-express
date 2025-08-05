import os
try:
    import html
    from datetime import datetime
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise

from utils.logger import logger


def generate_html_report(target: str, results: dict, output_path: str) -> None:
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        timestamp = datetime.now()
        html_target = html.escape(target)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rapid Recon Report - {html_target}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            background-color: #f0f2f5;
            color: #2c3e50;
        }}
        nav {{
            width: 240px;
            background: #1d3557;
            color: #fff;
            min-height: 100vh;
            padding: 2rem 1rem;
            position: fixed;
        }}
        nav h2 {{
            font-size: 1.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }}
        nav ul {{
            list-style: none;
        }}
        nav ul li {{
            margin: 1rem 0;
        }}
        nav ul li a {{
            color: #fff;
            text-decoration: none;
            font-size: 1rem;
            display: block;
            padding: 0.6rem;
            border-radius: 6px;
            transition: background 0.3s ease;
        }}
        nav ul li a:hover {{
            background: #457b9d;
        }}
        main {{
            margin-left: 240px;
            padding: 2rem;
            flex: 1;
        }}
        header {{
            background: #fff;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }}
        header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        header p {{
            color: #6b7280;
        }}
        .card {{
            background: #fff;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        }}
        h2 {{
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: #1d3557;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }}
        table th, table td {{
            border: 1px solid #e2e8f0;
            padding: 0.75rem;
            text-align: left;
        }}
        table th {{
            background: #f1f5f9;
            font-weight: 600;
        }}
        .badge {{
            padding: 0.4rem 0.7rem;
            border-radius: 5px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .success {{
            background-color: #d1fae5;
            color: #065f46;
        }}
        .fail {{
            background-color: #fee2e2;
            color: #991b1b;
        }}
        .sub-card {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 0.8rem;
            margin-bottom: 0.6rem;
        }}
        footer {{
            text-align: center;
            font-size: 0.85rem;
            color: #6b7280;
            margin-top: 2rem;
        }}
    </style>
</head>
<body>

<nav>
    <h2>Rapid Recon</h2>
    <ul>
        <li><a href="#summary">📋 Summary</a></li>"""

        for section in results:
            html_content += f"<li><a href='#{section}'>{html.escape(section.replace('_', ' ').title())}</a></li>"

        html_content += f"""</ul>
</nav>

<main>
    <header>
        <h1>🛡️ Recon Report</h1>
        <p>Target: <strong>{html_target}</strong> | Generated on {timestamp.strftime("%Y-%m-%d %H:%M:%S")}</p>
    </header>

    <div class="card" id="summary">
        <h2>📋 Summary</h2>
        <table>
            <tr><th>Section</th><th>Status</th></tr>"""

        for section in results:
            readable = section.replace("_", " ").title()
            status = "✔️ Collected" if results[section] else "⚠️ Missing"
            badge_class = "success" if results[section] else "fail"
            html_content += f"<tr><td>{html.escape(readable)}</td><td><span class='badge {badge_class}'>{status}</span></td></tr>"

        html_content += "</table></div>"

        for section, content in results.items():
            html_content += f"""<div class="card" id="{section}">
        <h2>📂 {html.escape(section.replace('_', ' ').title())}</h2>
        {format_content_as_html(content)}
    </div>"""

        html_content += f"""<footer>
        &copy; {timestamp.year} Rapid Recon | Report generated for <strong>{html_target}</strong>
    </footer>
</main>

</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"[✓] HTML report saved to {output_path}")
    except Exception as e:
        logger.error(f"[!] Failed to generate HTML report: {e}")


def format_content_as_html(content):
    if isinstance(content, dict):
        output = "<table>"
        output += "<tr><th>Key</th><th>Value</th></tr>"
        for k, v in content.items():
            value = format_content_as_html(v)
            output += f"<tr><td>{html.escape(str(k))}</td><td>{value}</td></tr>"
        output += "</table>"
        return output
    elif isinstance(content, list):
        if all(isinstance(item, dict) for item in content):
            output = ""
            for item in content:
                output += "<div class='sub-card'>"
                for k, v in item.items():
                    output += f"<strong>{html.escape(str(k))}</strong>: {html.escape(str(v))}<br>"
                output += "</div>"
            return output
        else:
            return "<ul>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in content) + "</ul>"
    elif content is None:
        return "<span class='badge fail'>No Data</span>"
    else:
        return html.escape(str(content))

