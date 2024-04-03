from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

def generate_pdf(variables, fileName='official_document.pdf', documentTitle='Official Document'):
    # Create the paragraph body
    paragraph_text = f"I am {variables['owner_name']}, the owner of the farm {variables['farm_name']}, located at {variables['location']}, covering an area of {variables['farm_area']} hectares. I report that there are {variables['num_cows']} dairy cows on the farm. The farm's total methane emissions are {variables['methane_emissions']} kg CO2-eq, which were calculated using {variables['methane_calculation']}. The farm consumes {variables['electricity_consumption']} kWh of electricity and {variables['fuel_consumption']} L/m3 of fuel of type {variables['fuel_type']}. I declare that all the information reported on {variables['declaration_date']} is true."

    # Create a PDF document
    pdf = canvas.Canvas(fileName, pagesize=letter)
    pdf.setTitle(documentTitle)

    # Title
    pdf.setFont("Times-Bold", 22)  # Changed font to Times-Bold
    title = "CO2 Emissions Report"
    title_width = pdf.stringWidth(title, "Times-Bold")
    pdf.drawCentredString(300, 730, title)  # Adjusted vertical position

    # Paragraph
    pdf.setFont("Times-Roman", 12)  # Set font to Times-Roman
    paragraph = Paragraph(paragraph_text, style=ParagraphStyle(name='ParagraphStyle', leading=14))
    paragraph.wrap(430, 300)  # Wrap the paragraph within a width of 400 pixels
    paragraph.drawOn(pdf, 100, 600)  # Draw the paragraph starting at (100, 600)

    # Get the height of the paragraph
    paragraph_height = paragraph.height

    # Add "Signed by John Doe" below the paragraph
    pdf.setFont("Times-Roman", 12)
    signed_by_text = "Signed by John Doe"
    signed_by_width = pdf.stringWidth(signed_by_text, "Times-Roman")
    signed_by_position_x = 100 + (430 - signed_by_width) / 2  # Centered horizontally
    signed_by_position_y = 600 - paragraph_height - 20  # 20 units below the paragraph
    pdf.drawString(signed_by_position_x, signed_by_position_y, signed_by_text)

    pdf.save()

# Example usage:
if __name__ == "__main__":
    variables = {
        'farm_name': 'Example Farm',
        'owner_name': 'John Doe',
        'location': '123 Farm Road, Farmville, Country X',
        'farm_area': '100',
        'num_cows': '50',
        'methane_emissions': '1000',
        'methane_calculation': 'Method A',
        'electricity_consumption': '10000',
        'fuel_consumption': '5000',
        'fuel_type': 'Diesel',
        'declaration_date': 'February 18, 2024',
    }

    generate_pdf(variables)
