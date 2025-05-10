import sys
import json
from address_label_generator import process_shipping_list, generate_address_pdf
from pirateship_generator import generate_pirateship_csv

def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <path_to_csv> <path_to_config> <output_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    config_path = sys.argv[2]
    output_path = sys.argv[3]

    # Read config file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Generate PirateShip CSV
    pirateship_csv = generate_pirateship_csv(csv_path, output_path)
    print(f"PirateShip CSV generated: {pirateship_csv}")

    # Process shipping list and generate addresses for labels
    addresses = process_shipping_list(csv_path)

    # Generate PDF with addresses
    output_pdf = output_path + "\\formatted_addresses.pdf"
    generate_address_pdf(output_pdf, addresses, config)

    print(f"Address labels PDF generated: {output_pdf}")

if __name__ == "__main__":
    main() 