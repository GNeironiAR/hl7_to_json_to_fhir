# HL7 to JSON Converter

This Python script converts HL7 (Health Level 7) messages to JSON format, specifically focusing on ORU (Observational Result Unsolicited) messages for laboratory results.

## Features

- Reads HL7 messages from a file
- Parses HL7 segments (MSH, PID, ORC, OBR, OBX, NTE)
- Converts HL7 data to a structured JSON format
- Handles multiple OBX and NTE segments
- Performs basic validation of HL7 message structure
- Outputs the result to both console and a JSON file

## Requirements

- Python 3.6 or higher

## Usage

1. Place your HL7 message in a file named `example.HL7` in the same directory as the script.
2. Run the script:

   ```
   python hl7_to_json_converter.py
   ```

3. The script will process the HL7 message and output the result in two ways:
   - Printed to the console
   - Saved to a file named `output.json`

## How It Works

1. **File Reading**: The script starts by reading the HL7 message from the `example.HL7` file.

2. **Message Parsing**: The HL7 message is split into segments, and each segment is processed based on its type (MSH, PID, ORC, OBR, OBX, NTE).

3. **Segment Processing**: Each segment type has its own parsing function that extracts relevant information from the segment fields.

4. **JSON Construction**: The parsed data is structured into a JSON format, with separate objects for each segment type.

5. **Validation**: The script checks for the presence of required segments (MSH, PID, ORC, OBR, OBX) and ensures each segment has the minimum required number of fields.

6. **Error Handling**: If any errors occur during processing (e.g., missing segments, insufficient fields), the script will return a JSON object with an error message.

7. **Output**: The resulting JSON is both printed to the console and saved to a file named `output.json`.

## Supported HL7 Segments

- MSH (Message Header)
- PID (Patient Identification)
- ORC (Common Order)
- OBR (Observation Request)
- OBX (Observation Result)
- NTE (Notes and Comments)

## Limitations

- This script is specifically designed for ORU messages containing laboratory results.
- It may not handle all possible variations of HL7 messages or non-standard implementations.
- The script assumes the input file uses either '\n' or '\r\n' as line separators.

## Customization

You can modify the `parse_*` functions to extract additional fields or adjust the parsing logic for specific needs. The main `hl7_to_json` function can also be updated to handle additional segment types if required.

## Error Handling

If the script encounters any errors (e.g., missing file, invalid HL7 format), it will print an error message to the console. In the case of parsing errors, it will return a JSON object with an "error" key containing the error message.