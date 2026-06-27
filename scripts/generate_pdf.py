"""Generate styled HTML and PDF from markdown reports using Chrome headless."""
import re
import subprocess
import sys
import os

def md_to_styled_html(md_path, html_path):
    """Convert markdown to styled HTML with proper Chinese font and blue links."""
    # Use pandoc for md→html
    subprocess.run([
        "pandoc", md_path, "-o", html_path,
        "--standalone", "--metadata", "title= "
    ], check=True)

    with open(html_path, "r") as f:
        html = f.read()

    # Remove pandoc's default style
    html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)

    style = """<style>
body {
    font-family: "PingFang SC", -apple-system, "Helvetica Neue", sans-serif;
    font-size: 14px;
    line-height: 1.8;
    padding: 40px 50px;
    max-width: 920px;
    margin: 0 auto;
    color: #222;
}
a {
    color: #0056b3;
    text-decoration: underline;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 13px;
}
th, td {
    border: 1px solid #ccc;
    padding: 7px 10px;
    text-align: left;
}
th {
    background-color: #f0f0f0;
    font-weight: bold;
}
blockquote {
    border-left: 3px solid #0056b3;
    padding: 8px 14px;
    margin: 1em 0;
    color: #333;
    background: #f8f9fa;
}
code {
    background: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 12px;
    font-family: "SF Mono", Menlo, monospace;
}
pre {
    background: #f4f4f4;
    padding: 14px;
    border-radius: 4px;
    overflow-x: auto;
}
pre code {
    padding: 0;
    background: none;
}
h1 {
    font-size: 22px;
    border-bottom: 2px solid #333;
    padding-bottom: 8px;
}
h2 {
    font-size: 17px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 5px;
    margin-top: 2em;
}
h3 { font-size: 15px; }
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 2em 0;
}
</style>"""

    html = html.replace("</head>", style + "\n</head>")

    with open(html_path, "w") as f:
        f.write(html)

    return html_path


def html_to_pdf(html_path, pdf_path):
    """Use Chrome headless to generate PDF from HTML."""
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    result = subprocess.run([
        chrome, "--headless", "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        "--no-margins",
        html_path
    ], capture_output=True, text=True)
    
    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"  PDF: {pdf_path} ({size // 1024}KB)")
    else:
        print(f"  ERROR: PDF generation failed")
        print(result.stderr[-500:] if result.stderr else "No error output")


def process_report(md_path):
    """Generate both HTML and PDF from a markdown report."""
    base = md_path.rsplit('.md', 1)[0]
    html_path = base + '.html'
    pdf_path = base + '.pdf'

    print(f"Processing: {md_path}")
    md_to_styled_html(md_path, html_path)
    print(f"  HTML: {html_path}")
    html_to_pdf(html_path, pdf_path)


if __name__ == "__main__":
    reports = sys.argv[1:] if len(sys.argv) > 1 else [
        "report/测控技术与仪器_专业分析.md",
        "report/shandong_605_major_selection_brief.md",
    ]
    for r in reports:
        process_report(r)
    print("\nDone.")
