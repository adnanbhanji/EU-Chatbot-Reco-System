from weasyprint import HTML
from datetime import datetime

def generate_enhanced_pdf(data, file_name):
    # Get the keys and values from the data dictionary
    keys = list(data.keys())
    values = list(data.values())

    # Prepare the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Farm Report</title>
        <style>
            body { font-family: 'Helvetica', 'Arial', sans-serif; margin: 20px; background: #f9f9f9; color: #333; }
            header, footer { text-align: center; margin-bottom: 20px; }
            h1 { color: #007BFF; }
            h2 { color: #28a745; }
            .info, .data { border-bottom: 2px solid #dee2e6; margin-bottom: 20px; }
            p { line-height: 1.5; }
            footer p { font-size: 0.9rem; color: #6c757d; }
        </style>
    </head>
    <body>
        <header>
            <h1>Farm Report</h1>
        </header>
        <section class="info">
    """
    
    for i in range(len(keys)-1):
        html_content += f"<h2>{keys[i]}</h2><p>{values[i+1]}</p>"
    
    html_content += f"<h2>{keys[-1]}</h2><p>{'Completed!'}</p>"  # For the last key, provide a default value
    
    html_content += """
        </section>
        <footer>
            <p>Report generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>
        </footer>
    </body>
    </html>
    """

    # Write the HTML content to a PDF file
    HTML(string=html_content).write_pdf(file_name)
    print(f"Generated PDF: {file_name}")
