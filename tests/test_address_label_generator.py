import unittest
import os
import tempfile
import json
from datetime import datetime
from address_label_generator import process_shipping_list, generate_address_pdf

class TestAddressLabelGenerator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test CSV file with today's date
        today = datetime.now().strftime('%Y%m%d')
        self.csv_filename = f"TCGplayer_ShippingExport_{today}_123.csv"
        self.csv_path = os.path.join(self.test_dir, self.csv_filename)
        
        # Sample CSV content
        csv_content = """FirstName,LastName,Address1,Address2,City,State,PostalCode,Country,Order #,Value Of Products,Shipping Fee Paid
John,Doe,456 Main St,Apt 789,Anytown,ST,67890,US,12345,15.00,2.00
Jane,Smith,789 Oak St,,Othertown,ST,54321,US,12346,25.00,3.00
Bob,Johnson,123 Pine St,,Somewhere,ST,12345,US,12347,30.00,4.00"""
        
        with open(self.csv_path, 'w') as f:
            f.write(csv_content)

        # Create test config file
        self.config_path = os.path.join(self.test_dir, 'config.json')
        self.config = {
            "start_row": 0,
            "start_col": 0,
            "font_color": [0, 0, 0],
            "value_threshold": 20,
            "default_address": {
                "name": "Test Business",
                "addr1": "Test Address",
                "addr2": "",
                "city": "Test City",
                "state": "TS",
                "zipcode": "12345"
            },
            "repeat_default": 0
        }
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)

    def test_process_shipping_list_default_threshold(self):
        # Test processing with default threshold (20)
        addresses = process_shipping_list(self.csv_path, self.config_path)
        
        # Check if only orders < $20 are included
        self.assertEqual(len(addresses), 1)  # Only John's order
        
        # Check the address data
        address = addresses[0]
        self.assertEqual(address['name'], "John Doe")
        self.assertEqual(address['addr1'], "456 Main St")
        self.assertEqual(address['addr2'], "Apt 789")
        self.assertEqual(address['city'], "Anytown")
        self.assertEqual(address['state'], "ST")
        self.assertEqual(str(address['zipcode']), "67890")  # Convert to string for comparison

    def test_process_shipping_list_custom_threshold(self):
        # Update config with custom threshold
        self.config['value_threshold'] = 30
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)

        # Test processing with custom threshold
        addresses = process_shipping_list(self.csv_path, self.config_path)
        
        # Check if only orders < $30 are included
        self.assertEqual(len(addresses), 2)  # John and Jane's orders
        
        # Check the first address
        address = addresses[0]
        self.assertEqual(address['name'], "John Doe")
        self.assertEqual(address['addr1'], "456 Main St")
        self.assertEqual(address['addr2'], "Apt 789")
        self.assertEqual(address['city'], "Anytown")
        self.assertEqual(address['state'], "ST")
        self.assertEqual(str(address['zipcode']), "67890")  # Convert to string for comparison

        # Check the second address
        address = addresses[1]
        self.assertEqual(address['name'], "Jane Smith")
        self.assertEqual(address['addr1'], "789 Oak St")
        self.assertEqual(address['addr2'], "")
        self.assertEqual(address['city'], "Othertown")
        self.assertEqual(address['state'], "ST")
        self.assertEqual(str(address['zipcode']), "54321")  # Convert to string for comparison

    def test_generate_address_pdf(self):
        # Test PDF generation
        addresses = process_shipping_list(self.csv_path, self.config_path)
        output_pdf = os.path.join(self.test_dir, 'test_addresses.pdf')
        
        # Generate PDF
        generate_address_pdf(output_pdf, addresses, self.config)
        
        # Check if file was created
        self.assertTrue(os.path.exists(output_pdf))
        # Check if file is not empty
        self.assertGreater(os.path.getsize(output_pdf), 0)

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main() 