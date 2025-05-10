import pandas as pd
import re
from datetime import datetime

def process_tcg_export(tcg_export_path):
    """
    Process the TCGplayer export file and return the transformed data for PirateShip.
    """
    file_name_match = re.search(r'TCGplayer_ShippingExport_(\d{8})_(\d+)\.csv', tcg_export_path)
    if not file_name_match:
        raise ValueError("The file name does not match the expected pattern: TCGplayer_ShippingExport_YYYYMMDD_number.csv")

    export_date = file_name_match.group(1)
    export_number = file_name_match.group(2)
    formatted_date = datetime.strptime(export_date, '%Y%m%d').strftime('%Y-%m-%d')

    tcg_export_df = pd.read_csv(tcg_export_path)
    tcg_export_df['FullCost'] = tcg_export_df['Value Of Products'] + tcg_export_df['Shipping Fee Paid']
    filtered_df = tcg_export_df[tcg_export_df['FullCost'] >= 20]

    transformed_data = pd.DataFrame({
        'Name': filtered_df['FirstName'] + ' ' + filtered_df['LastName'],
        'Address 1': filtered_df['Address1'],
        'Address 2': filtered_df['Address2'],
        'City': filtered_df['City'],
        'State': filtered_df['State'],
        'Zipcode': filtered_df['PostalCode'],
        'Country': filtered_df['Country'],
        'Order Id': filtered_df['Order #'],
        'Ounces': 3,
        'Length': 7,
        'Width': 5,
        'Height': 0.5
    })

    return transformed_data, formatted_date, export_number

def generate_pirateship_csv(tcg_export_path, output_path):
    """
    Generate a PirateShip-compatible CSV file from the TCGplayer export.
    Returns the path to the generated file.
    """
    transformed_data, formatted_date, export_number = process_tcg_export(tcg_export_path)
    
    output_file = output_path + f'\\PirateShip_Import_{formatted_date}_{export_number}.csv'
    transformed_data.to_csv(output_file, index=False)
    
    return output_file 