# HL7 to FHIR Conversion Project

This project converts HL7 (Health Level 7) messages to FHIR (Fast Healthcare Interoperability Resources) format in two steps:
1. HL7 to JSON conversion
2. JSON to FHIR conversion

The project is specifically designed to handle ORU (Observational Result Unsolicited) messages for laboratory results.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Setup

1. Clone the repository or download the project files.

2. (Optional but recommended) Create a virtual environment:
   ```
   python -m venv env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source env/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Project Structure

- `hl7_to_json.py`: Script to convert HL7 messages to JSON format
- `json_to_fhir.py`: Script to convert JSON to FHIR format
- `requirements.txt`: List of project dependencies
- `example.HL7`: Sample HL7 message file (you should replace this with your actual HL7 message)

## Usage

### Step 1: HL7 to JSON Conversion

1. Ensure your HL7 message is in a file named `example.HL7` in the project directory.

2. Run the HL7 to JSON conversion script:
   ```
   python hl7_to_json.py
   ```

3. This will generate an `output.json` file containing the JSON representation of the HL7 message.

### Step 2: JSON to FHIR Conversion

1. Ensure the `output.json` file from Step 1 is in the project directory.

2. Run the JSON to FHIR conversion script:
   ```
   python json_to_fhir.py
   ```

3. This will generate an `output_fhir.json` file containing the FHIR representation of the data.

4. A log file `fhir_conversion.log` will also be created with detailed information about the conversion process.

## Output Files

- `output.json`: JSON representation of the HL7 message
- `output_fhir.json`: FHIR representation of the data
- `fhir_conversion.log`: Detailed log of the JSON to FHIR conversion process

## Limitations

- This project is specifically designed for ORU messages containing laboratory results.
- It may not handle all variations of HL7 messages or non-standard implementations.
- The FHIR output is limited to DiagnosticReport and Observation resources.

## Troubleshooting

- If you encounter any issues, check the `fhir_conversion.log` file for detailed error messages and the conversion process log.
- Ensure that your input HL7 message follows the expected format for ORU messages.
- Verify that all required fields are present in your HL7 message.

## Customization

To adapt this project for other types of HL7 messages or different structures:
1. Modify the parsing functions in `hl7_to_json.py` to handle different segment types or fields.
2. Adjust the FHIR resource creation logic in `json_to_fhir.py` to create different types of FHIR resources as needed.

## Support

For issues, questions, or contributions, please contact the development team or open an issue in the project repository.