import json
import uuid
import logging
from datetime import datetime
from fhirclient import client
from fhirclient.models import diagnosticreport, patient, observation, identifier, coding, codeableconcept, quantity, reference, fhirdatetime, fhirreference, fhirdate, fhirinstant

# Set up logging
logging.basicConfig(filename='fhir_conversion.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_date(date_string):
    logging.debug(f"Attempting to parse date string: {date_string}")
    formats = [
        "%Y%m%d%H%M",  # YYYYMMDDHHmm
        "%Y%m%d%H%M%S",  # YYYYMMDDHHmmSS
        "%Y%m%d"  # YYYYMMDD
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_string, fmt)
            logging.debug(f"Successfully parsed {date_string} with format {fmt}")
            return parsed_date
        except ValueError:
            logging.debug(f"Failed to parse {date_string} with format {fmt}")
    
    raise ValueError(f"Unable to parse date string: {date_string}")

def create_fhir_diagnostic_report(json_data):
    logging.info("Creating FHIR DiagnosticReport...")
    
    diagnostic_report = diagnosticreport.DiagnosticReport()
    diagnostic_report.id = str(uuid.uuid4())
    diagnostic_report.status = "final"
    diagnostic_report.code = codeableconcept.CodeableConcept({
        "coding": [
            {
                "system": "http://loinc.org",
                "code": json_data['OBR']['UniversalServiceIdentifier'].split('^')[0],
                "display": json_data['OBR']['UniversalServiceIdentifier'].split('^')[1]
            }
        ]
    })
    
    obs_date_str = json_data['OBR']['ObservationDateTime']
    logging.info(f"Parsing ObservationDateTime: {obs_date_str}")
    try:
        obs_date = parse_date(obs_date_str)
        fhir_date_str = obs_date.strftime("%Y-%m-%d")
        logging.debug(f"Attempting to create FHIRDateTime with: {fhir_date_str}")
        diagnostic_report.effectiveDateTime = fhirdatetime.FHIRDateTime.with_json(fhir_date_str)
        logging.info(f"Successfully set effectiveDateTime to: {diagnostic_report.effectiveDateTime.as_json()}")
    except Exception as e:
        logging.error(f"Error setting effectiveDateTime: {e}")
        diagnostic_report.effectiveDateTime = None
    
    message_date_str = json_data['MSH']['DateTimeOfMessage']
    logging.info(f"Parsing DateTimeOfMessage: {message_date_str}")
    try:
        message_date = parse_date(message_date_str)
        fhir_instant_str = message_date.isoformat() + "Z"
        logging.debug(f"Attempting to create FHIRInstant with: {fhir_instant_str}")
        diagnostic_report.issued = fhirinstant.FHIRInstant.with_json(fhir_instant_str)
        logging.info(f"Successfully set issued to: {diagnostic_report.issued.as_json()}")
    except Exception as e:
        logging.error(f"Error setting issued: {e}")
        diagnostic_report.issued = None
    
    patient_reference = fhirreference.FHIRReference()
    patient_reference.reference = f"Patient/{json_data['PID']['PatientID'].split('^')[0]}"
    diagnostic_report.subject = patient_reference
    
    observations = []
    for obx in json_data['OBX']:
        obs = observation.Observation()
        obs.id = str(uuid.uuid4())
        obs.status = "final"
        obs.code = codeableconcept.CodeableConcept({
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": obx['ObservationIdentifier'].split('^')[0],
                    "display": obx['ObservationIdentifier'].split('^')[1]
                }
            ]
        })
        obs.valueQuantity = quantity.Quantity({
            "value": float(obx['ObservationValue']),
            "unit": obx['Units'],
            "system": "http://unitsofmeasure.org",
            "code": obx['Units']
        })
        obs.subject = patient_reference
        observations.append(obs)
    
    diagnostic_report.result = [fhirreference.FHIRReference({'reference': f"Observation/{obs.id}"}) for obs in observations]
    
    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "resource": diagnostic_report.as_json(),
                "request": {
                    "method": "POST",
                    "url": "DiagnosticReport"
                }
            }
        ]
    }
    
    for obs in observations:
        bundle['entry'].append({
            "resource": obs.as_json(),
            "request": {
                "method": "POST",
                "url": "Observation"
            }
        })
    
    return bundle

def main():
    logging.info("Starting FHIR conversion process")
    with open('output.json', 'r') as json_file:
        json_data = json.load(json_file)
    
    fhir_bundle = create_fhir_diagnostic_report(json_data)
    
    with open('output_fhir.json', 'w') as fhir_file:
        json.dump(fhir_bundle, fhir_file, indent=2)
    
    logging.info("FHIR resource has been created and saved to output_fhir.json")
    print("FHIR resource has been created and saved to output_fhir.json")
    print("Check fhir_conversion.log for detailed debug information")

if __name__ == "__main__":
    main()