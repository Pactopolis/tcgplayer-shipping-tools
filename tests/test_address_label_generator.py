import unittest
import os
import tempfile
import json
from address_label_generator import generate_address_pdf, process_shipping_list

class TestAddressLabelGenerator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Sample config
        self.config = {
            "start_row": 0,
            "start_col": 0,
            "font_color": [0, 0, 0],
            "default_address": {
                "name": "Test Business",
                "addr1": "123 Test St",
                "addr2": "",
                "city": "Test City",
                "state": "TS",
                "zipcode": "12345"
            },
            "repeat_default": 0
        }
        
        # Sample addresses
        self.test_addresses = [
            {
                "name": "John Doe",
                "addr1": "456 Main St",
                "addr2": "Apt 789",
                "city": "Anytown",
                "state": "ST",
                "zipcode": "67890"
            }
        ]

    def test_generate_address_pdf(self):
        # Test PDF generation
        output_file = os.path.join(self.test_dir, "test_labels.pdf")
        generate_address_pdf(output_file, self.test_addresses, self.config)
        
        # Check if file was created
        self.assertTrue(os.path.exists(output_file))
        # Check if file is not empty
        self.assertGreater(os.path.getsize(output_file), 0)

    def test_process_shipping_list(self):
        # Create a temporary CSV file
        csv_content = """FirstName,LastName,Address1,Address2,City,State,PostalCode,Value Of Products,Shipping Fee Paid
John,Doe,456 Main St,Apt 789,Anytown,ST,67890,15.00,2.00
Jane,Smith,789 Oak St,,Othertown,ST,54321,25.00,3.00"""
        
        csv_file = os.path.join(self.test_dir, "test_orders.csv")
        with open(csv_file, 'w') as f:
            f.write(csv_content)
        
        # Test processing
        addresses = process_shipping_list(csv_file)
        
        # Check if only orders < $20 are included
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0]["name"], "John Doe")
        self.assertEqual(addresses[0]["addr1"], "456 Main St")
        self.assertEqual(addresses[0]["addr2"], "Apt 789")
        self.assertEqual(addresses[0]["city"], "Anytown")
        self.assertEqual(addresses[0]["state"], "ST")
        self.assertEqual(str(addresses[0]["zipcode"]), "67890")  # Convert to string for comparison

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main() 