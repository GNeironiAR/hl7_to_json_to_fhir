import re
import json
from typing import Dict, List, Any

def hl7_to_json(hl7_message: str) -> str:
    try:
        # Split the message into segments
        segments = re.split(r'\r?\n', hl7_message.strip())
        
        # Initialize the JSON structure
        json_data: Dict[str, Any] = {}
        
        for segment in segments:
            # Split the segment into fields
            fields = segment.split('|')
            segment_name = fields[0]
            
            if segment_name == "MSH":
                json_data["MSH"] = parse_msh(fields)
            elif segment_name == "PID":
                json_data["PID"] = parse_pid(fields)
            elif segment_name == "ORC":
                json_data["ORC"] = parse_orc(fields)
            elif segment_name == "OBR":
                json_data["OBR"] = parse_obr(fields)
            elif segment_name == "OBX":
                if "OBX" not in json_data:
                    json_data["OBX"] = []
                json_data["OBX"].append(parse_obx(fields))
            elif segment_name == "NTE":
                if "NTE" not in json_data:
                    json_data["NTE"] = []
                json_data["NTE"].append(parse_nte(fields))
        
        # Validate the presence of required segments
        required_segments = ["MSH", "PID", "ORC", "OBR", "OBX"]
        for segment in required_segments:
            if segment not in json_data:
                raise ValueError(f"Required segment {segment} is missing")
        
        return json.dumps(json_data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def parse_msh(fields: List[str]) -> Dict[str, str]:
    if len(fields) < 12:
        raise ValueError("MSH segment does not have enough fields")
    return {
        "SendingApplication": fields[2],
        "SendingFacility": fields[3],
        "ReceivingApplication": fields[4],
        "ReceivingFacility": fields[5],
        "DateTimeOfMessage": fields[6],
        "MessageType": fields[8],
        "MessageControlID": fields[9],
        "ProcessingID": fields[10],
        "VersionID": fields[11]
    }

def parse_pid(fields: List[str]) -> Dict[str, str]:
    if len(fields) < 9:
        raise ValueError("PID segment does not have enough fields")
    return {
        "PatientID": fields[3],
        "PatientName": fields[5],
        "DateOfBirth": fields[7],
        "Sex": fields[8],
        "Address": fields[11] if len(fields) > 11 else ""
    }

def parse_orc(fields: List[str]) -> Dict[str, str]:
    if len(fields) < 6:
        raise ValueError("ORC segment does not have enough fields")
    return {
        "OrderControl": fields[1],
        "PlacerOrderNumber": fields[2],
        "FillerOrderNumber": fields[3],
        "OrderStatus": fields[5],
        "DateTimeOfTransaction": fields[9] if len(fields) > 9 else ""
    }

def parse_obr(fields: List[str]) -> Dict[str, str]:
    if len(fields) < 8:
        raise ValueError("OBR segment does not have enough fields")
    return {
        "SetID": fields[1],
        "PlacerOrderNumber": fields[2],
        "FillerOrderNumber": fields[3],
        "UniversalServiceIdentifier": fields[4],
        "ObservationDateTime": fields[7],
        "OrderingProvider": fields[16] if len(fields) > 16 else ""
    }

def parse_obx(fields: List[str]) -> Dict[str, str]:
    if len(fields) < 12:
        raise ValueError("OBX segment does not have enough fields")
    return {
        "SetID": fields[1],
        "ValueType": fields[2],
        "ObservationIdentifier": fields[3],
        "ObservationValue": fields[5],
        "Units": fields[6],
        "ReferenceRange": fields[7],
        "AbnormalFlags": fields[8],
        "ObservationResultStatus": fields[11]
    }

def parse_nte(fields: List[str]) -> Dict[str, str]:
    if len(fields) < 4:
        raise ValueError("NTE segment does not have enough fields")
    return {
        "SetID": fields[1],
        "SourceOfComment": fields[2],
        "Comment": fields[3]
    }

# Read HL7 message from file
def read_hl7_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return ""

# Main execution
if __name__ == "__main__":
    file_path = "example.HL7"
    hl7_message = read_hl7_from_file(file_path)
    
    if hl7_message:
        json_output = hl7_to_json(hl7_message)
        print(json_output)
        
        # Optionally, write the JSON output to a file
        with open("output.json", "w") as json_file:
            json_file.write(json_output)
        print("JSON output has been written to output.json")
    else:
        print("Failed to read HL7 message from file.")