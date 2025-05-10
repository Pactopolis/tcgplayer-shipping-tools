from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import pandas as pd
import json

# Function to generate PDF from addresses
def generate_address_pdf(filename, addresses, config):
    # Page settings
    page_width, page_height = letter
    top_margin = 0.5 * inch
    left_margin = 0.25 * inch
    bottom_margin = 0.42 * inch
    cell_width = 2.63 * inch
    cell_height = 1 * inch
    column_spacing = 0.125 * inch
    row_spacing = 0.05 * inch  # Adjusted spacing
    padding_left = 0.125 * inch

    # Configurations
    start_row = config.get("start_row", 0)
    start_col = config.get("start_col", 0)
    font_color = config.get("font_color", (0, 0, 0))
    default_address = config.get("default_address", {})
    repeat_default = config.get("repeat_default", 0)

    # Prepare addresses with default if needed
    if repeat_default == -1:
        repeat_default = len(addresses)
    addresses = addresses + [default_address] * repeat_default

    # Initialize canvas
    c = canvas.Canvas(filename, pagesize=letter)

    # Set starting position
    y_position = page_height - top_margin - (start_row * (cell_height + row_spacing))
    x_positions = [
        left_margin,
        left_margin + cell_width + column_spacing,
        left_margin + 2 * (cell_width + column_spacing),
    ]

    row_count = start_row
    col_count = start_col

    for i, address in enumerate(addresses):
        # Calculate the column and row
        column = col_count % 3
        if column == 0 and i != 0:
            y_position -= cell_height + row_spacing
            row_count += 1

        # Start a new page if row limit is reached
        if row_count == 10:
            c.showPage()
            y_position = page_height - top_margin
            row_count = 0

        x_position = x_positions[column]

        # Format address
        lines = [
            address.get("name", ""),
            address.get("addr1", ""),
        ]
        if address.get("addr2"):
            lines.append(address["addr2"])
        lines.append(f"{address.get('city', '')}, {address.get('state', '')} {address.get('zipcode', '')}")

        # Calculate vertical offset based on number of lines
        line_height = 0.2 * inch  # Height of each line
        total_text_height = len(lines) * line_height
        vertical_offset = (cell_height - total_text_height) / 2  # Center the text vertically

        # Write text inside the cell
        text_object = c.beginText(x_position + padding_left, y_position - vertical_offset)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColorRGB(*font_color)
        for line in lines:
            text_object.textLine(line)
        c.drawText(text_object)

        col_count += 1

    # Save the PDF
    c.save()

def process_shipping_list(csv_path, config_path='config.json'):
    data = pd.read_csv(csv_path)

    data['FullName'] = data['FirstName'] + ' ' + data['LastName']
    data['FullCost'] = data['Value Of Products'] + data['Shipping Fee Paid']

    # Get value threshold from config
    with open(config_path, 'r') as f:
        config = json.load(f)
    value_threshold = config.get('value_threshold', 20)

    filtered_data = data[data['FullCost'] < value_threshold]

    addresses = []
    for _, row in filtered_data.iterrows():
        address = {
            "name": row['FullName'],
            "addr1": row['Address1'],
            "addr2": row['Address2'] if not pd.isna(row['Address2']) else "",
            "city": row['City'],
            "state": row['State'],
            "zipcode": row['PostalCode']
        }
        addresses.append(address)

    return addresses 