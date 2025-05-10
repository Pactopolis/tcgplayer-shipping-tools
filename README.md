# TCGplayer Shipping Label Generator

This tool helps TCGplayer sellers generate shipping labels and address labels from TCGplayer order exports. It creates both a PirateShip-compatible CSV file and printable address labels in PDF format.

## Features

- Generates PirateShip-compatible CSV files from TCGplayer order exports
- Creates printable address labels in PDF format
- Filters orders based on value thresholds
- Supports custom label configurations

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `config.json` file in the project directory with the following structure:

```json
{
  "start_row": 0,
  "start_col": 0,
  "font_color": [0, 0, 0],
  "default_address": {
    "name": "",
    "addr1": "",
    "addr2": "",
    "city": "",
    "state": "",
    "zipcode": ""
  },
  "repeat_default": 0
}
```

## Usage

### Using Python Directly

Run the script using Python:

```bash
python main.py <path_to_tcgplayer_export> <path_to_config> <output_path>
```

Example:

```bash
python main.py C:\Downloads\TCGplayer_ShippingExport_20240315_123.csv config.json C:\Output
```

### Using the Batch File

1. Add the project directory to your system's PATH environment variable
2. Run the batch file from anywhere:

```bash
generate_labels <path_to_tcgplayer_export> <path_to_config> <output_path>
```

## Input File Format

The script expects a TCGplayer order export CSV file with the following columns:

- FirstName
- LastName
- Address1
- Address2
- City
- State
- PostalCode
- Country
- Order #
- Value Of Products
- Shipping Fee Paid

## Output Files

1. PirateShip CSV file:

   - Named: `PirateShip_Import_YYYY-MM-DD_NUMBER.csv`
   - Contains orders with total value >= $20
   - Formatted for direct import into PirateShip

2. Address Labels PDF:
   - Named: `formatted_addresses.pdf`
   - Contains address labels for orders with total value < $20
   - Formatted for standard address label sheets

## Disclaimer

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

The user assumes all responsibility for verifying the accuracy of generated shipping labels and CSV files before use. Always double-check addresses and shipping information before sending packages.

## Notes

- Orders with total value (products + shipping) >= $20 are included in the PirateShip CSV
- Orders with total value < $20 are included in the address labels PDF
- The script automatically handles pagination and label positioning
