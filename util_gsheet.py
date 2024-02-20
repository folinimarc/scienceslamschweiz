import gspread
import os
from pathlib import Path
import tempfile
from datetime import datetime

def _filter_events(events_data):
    """Events must have a name and date-DD.MM.YY that is not in the past."""
    valid = []
    for entry in events_data:
        if entry.get('name') and entry.get('date-DD.MM.YY'):
            if datetime.strptime(entry.get('date-DD.MM.YY'), '%d.%m.%y') >= datetime.now():
                valid.append(entry)
    return valid

def _filter_organisers(organisers_data):
    """Organisers must have a name."""
    valid = []
    for entry in organisers_data:
        if entry.get('name'):
            valid.append(entry)
    return valid

def read_gsheet_data():
    # Get the credentials from the environment variable
    # If env variable not set, look for a local credentials file
    google_credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    if not google_credentials_json:
        local_json = Path("./.secret.credentials.website-gspread-sa.json")
        if local_json.exists():
            google_credentials_json = local_json.read_text()
        else:
            raise ValueError('GOOGLE_CREDENTIALS_JSON is not set and no local credentials json found. Make sure this contains the credentials json content!')

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        temp_file.write(google_credentials_json)
        google_credentials_file = temp_file.name

    # Read data from google sheet
    gc = gspread.service_account(filename=google_credentials_file)
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1OM9XGCm0lfGFb_iaTPO8oddCepWUlDRlmYO9R75gwLM/edit#gid=0")
    events_data = sh.worksheet("events").get_all_records()
    events_data = _filter_events(events_data)

    organisers_data = sh.worksheet("organisers").get_all_records()
    organisers_data = _filter_organisers(organisers_data)

    Path(google_credentials_file).unlink()  # Delete the temporary file
    return events_data, organisers_data