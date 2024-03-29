from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

def generate_pdf(variables, fileName='official_document.pdf', documentTitle='Official Document'):
    # Create the paragraph body
    paragraph_text = f"I am {variables['owner_name']}, the owner of the farm {variables['farm_name']}, located at {variables['location']}, covering an area of {variables['farm_area']} hectares. I report that there are {variables['num_cows']} dairy cows on the farm. The farm operates under the {variables['production_system']} production system. The farm's total methane emissions are {variables['methane_emissions']} kg CO2-eq, which were calculated using {variables['methane_calculation']}. Additionally, the farm emits {variables['manure_methane_emissions']} kg CO2-eq of methane and {variables['manure_nitrous_emissions']} kg CO2-eq of nitrous oxide from manure management, calculated using {variables['manure_system']} and {variables['manure_calculation']}, respectively. The farm also emits {variables['feed_co2_emissions']} kg CO2-eq from feed production, using {variables['feed_type']} type feed with a quantity of {variables['feed_quantity']} sourced from {variables['feed_source']} and calculated using {variables['feed_calculation']}. The farm consumes {variables['electricity_consumption']} kWh of electricity and {variables['fuel_consumption']} L/m3 of {variables['fuel_type']} fuel, resulting in {variables['energy_co2_emissions']} kg CO2-eq of emissions, calculated using {variables['energy_calculation']}. The farm has undergone land use changes, with {variables['land_use_changes']} resulting in a net change of {variables['lulucf_co2']} kg CO2-eq, calculated using {variables['lulucf_calculation']}. Other emissions sources contribute {variables['other_emissions_quantity']} kg CO2-eq from {variables['other_emissions_source']}. Carbon credits from {variables['carbon_credits_source']} offset {variables['carbon_credits_quantity']} kg CO2-eq of emissions. The total emissions breakdown is: enteric fermentation {variables['enteric_fermentation_total']} kg CO2-eq, manure management {variables['manure_management_total']} kg CO2-eq, feed production {variables['feed_production_total']} kg CO2-eq, energy use {variables['energy_use_total']} kg CO2-eq, land use and land-use change {variables['lulucf_total']} kg CO2-eq, and other sources {variables['other_sources_total']} kg CO2-eq. I declare that all the information reported on {variables['declaration_date']} is true. EU compliance: {variables['eu_compliance']}."

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
    paragraph.wrap(430, 800)  # Wrap the paragraph within a width of 400 pixels
    paragraph_height = paragraph.height  # Get the height of the paragraph
    paragraph.drawOn(pdf, 100, 680 - paragraph_height)  # Draw the paragraph

    # Add "Signed by John Doe" below the paragraph
    pdf.setFont("Times-Roman", 12)
    signed_by_text = f"Signed by {variables['owner_name']}"
    signed_by_width = pdf.stringWidth(signed_by_text, "Times-Roman")
    signed_by_position_x = 100 + (430 - signed_by_width) / 2  # Centered horizontally
    signed_by_position_y = 580 - paragraph_height  # Adjusted position below the paragraph
    pdf.drawString(signed_by_position_x, signed_by_position_y, signed_by_text)

    pdf.save()

# Example usage:
variables = {
    'farm_name': 'Example Farm',
    'owner_name': 'John Doe',
    'location': '123 Farm Road, Farmville, Country X',
    'farm_area': '100',
    'num_cows': '50',
    'production_system': 'Grazing',
    'methane_emissions': '1000',
    'methane_calculation': 'Method A',
    'manure_methane_emissions': '500',
    'manure_nitrous_emissions': '200',
    'manure_system': 'System B',
    'manure_calculation': 'Method C',
    'feed_co2_emissions': '300',
    'feed_type': 'Type X',
    'feed_quantity': '200',
    'feed_source': 'Own production',
    'feed_calculation': 'Method D',
    'electricity_consumption': '10000',
    'fuel_consumption': '5000',
    'fuel_type': 'Diesel',
    'energy_co2_emissions': '1500',
    'energy_calculation': 'Method E',
    'land_use_changes': 'Conversion of forest to pasture',
    'lulucf_co2': '-500',
    'land_use_description': 'Increase in pasture area',
    'lulucf_calculation': 'Method F',
    'other_emissions_source': 'Source A',
    'other_emissions_quantity': '200',
    'carbon_credits_source': 'Source B',
    'carbon_credits_quantity': '100',
    'enteric_fermentation_total': '1000',
    'manure_management_total': '700',
    'feed_production_total': '300',
    'energy_use_total': '1500',
    'lulucf_total': '-500',
    'other_sources_total': '100',
    'declaration_date': 'February 18, 2024',
    'eu_compliance': 'Yes'
}

generate_pdf(variables)
