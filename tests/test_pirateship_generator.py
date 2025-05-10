import unittest
import os
import tempfile
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
Jane,Smith,789 Oak St,,Othertown,ST,54321,US,12346,25.00,3.00"""
        
        with open(self.csv_path, 'w') as f:
            f.write(csv_content)

    def test_process_tcg_export(self):
        # Test processing
        transformed_data, formatted_date, export_number = process_tcg_export(self.csv_path)
        
        # Check if only orders >= $20 are included
        self.assertEqual(len(transformed_data), 1)
        
        # Check the transformed data
        row = transformed_data.iloc[0]
        self.assertEqual(row['Name'], "Jane Smith")
        self.assertEqual(row['Address 1'], "789 Oak St")
        self.assertEqual(row['City'], "Othertown")
        self.assertEqual(row['State'], "ST")
        self.assertEqual(str(row['Zipcode']), "54321")  # Convert to string for comparison
        self.assertEqual(row['Country'], "US")
        self.assertEqual(str(row['Order Id']), "12346")  # Convert to string for comparison
        self.assertEqual(int(row['Ounces']), 3)  # Convert to int for comparison
        self.assertEqual(int(row['Length']), 7)  # Convert to int for comparison
        self.assertEqual(int(row['Width']), 5)  # Convert to int for comparison
        self.assertEqual(float(row['Height']), 0.5)  # Convert to float for comparison

    def test_generate_pirateship_csv(self):
        # Test CSV generation
        output_file = generate_pirateship_csv(self.csv_path, self.test_dir)
        
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