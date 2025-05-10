import unittest
import os
import tempfile
import json
from datetime import datetime
from pirateship_generator import process_tcg_export, generate_pirateship_csv

class TestPirateshipGenerator(unittest.TestCase):
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

    def test_process_tcg_export_default_threshold(self):
        # Test processing with default threshold (20)
        transformed_data, formatted_date, export_number = process_tcg_export(self.csv_path, self.config_path)
        
        # Check if only orders >= $20 are included
        self.assertEqual(len(transformed_data), 2)  # Jane and Bob's orders
        
        # Check the transformed data
        row = transformed_data.iloc[0]
        self.assertEqual(row['Name'], "Jane Smith")
        self.assertEqual(row['Address 1'], "789 Oak St")
        self.assertEqual(row['City'], "Othertown")
        self.assertEqual(row['State'], "ST")
        self.assertEqual(str(row['Zipcode']), "54321")
        self.assertEqual(row['Country'], "US")
        self.assertEqual(str(row['Order Id']), "12346")

    def test_process_tcg_export_custom_threshold(self):
        # Update config with custom threshold
        self.config['value_threshold'] = 30
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)

        # Test processing with custom threshold
        transformed_data, formatted_date, export_number = process_tcg_export(self.csv_path, self.config_path)
        
        # Check if only orders >= $30 are included
        self.assertEqual(len(transformed_data), 1)  # Only Bob's order
        
        # Check the transformed data
        row = transformed_data.iloc[0]
        self.assertEqual(row['Name'], "Bob Johnson")
        self.assertEqual(row['Address 1'], "123 Pine St")
        self.assertEqual(row['City'], "Somewhere")
        self.assertEqual(row['State'], "ST")
        self.assertEqual(str(row['Zipcode']), "12345")
        self.assertEqual(row['Country'], "US")
        self.assertEqual(str(row['Order Id']), "12347")

    def test_generate_pirateship_csv(self):
        # Test CSV generation
        output_file = generate_pirateship_csv(self.csv_path, self.test_dir, self.config_path)
        
        # Check if file was created
        self.assertTrue(os.path.exists(output_file))
        # Check if file is not empty
        self.assertGreater(os.path.getsize(output_file), 0)
        
        # Check if filename follows the expected pattern
        self.assertTrue(output_file.endswith('.csv'))
        self.assertIn('PirateShip_Import_', output_file)

    def test_invalid_filename(self):
        # Test with invalid filename
        invalid_path = os.path.join(self.test_dir, "invalid_filename.csv")
        with self.assertRaises(ValueError):
            process_tcg_export(invalid_path)

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main() 