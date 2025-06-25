import os
import base64
import csv
import re
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API access scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_label_id(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    raise ValueError(f"Label '{label_name}' not found.")

def clean(text):
    return re.sub(r'\s+', ' ', text.replace('-', '')).strip()

def extract_sentences(text, verb):
    lines = [clean(line) for line in text.splitlines() if line.strip()]
    rows = []
    i = 0

    while i < len(lines) - 1:
        german = lines[i]
        literal = lines[i + 1] if i + 1 < len(lines) else ''
        natural = lines[i + 2] if i + 2 < len(lines) else ''

        if re.match(r'^[A-ZÄÖÜ].+[\.\?!]$', german):
            # Use natural English if it looks valid, otherwise fallback to literal
            natural_valid = re.match(r'^[A-Z].+[\.\?!]$', natural)
            english = natural.strip() if natural_valid else literal.strip()
            example = literal.strip() if literal else ''
            rows.append([german.strip(), english, verb, example])
            i += 3 if natural_valid else 2
        else:
            i += 1

    return rows

def extract_email_content(service, user_id='me'):
    label_id = get_label_id(service, 'German')
    result = service.users().messages().list(userId=user_id, labelIds=[label_id], q='from:manuel').execute()
    messages = result.get('messages', [])
    all_rows = []

    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        parts = full_msg['payload'].get('parts', [])
        html_body = ''
        for part in parts:
            if part['mimeType'] == 'text/html':
                html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break

        soup = BeautifulSoup(html_body, 'html.parser')
        text = soup.get_text(separator='\n')

        # Extract verb from text
        verb_match = re.search(r"verb\s*:\s*([a-zA-ZäöüÄÖÜß]+)", text)
        verb = verb_match.group(1).strip() if verb_match else "unknown"

        rows = extract_sentences(text, verb)
        all_rows.extend(rows)

    return all_rows

def write_to_csv(data, filename='german_phrases.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Phrase in German', 'Phrase in English', 'Verb taught', 'Example'])
        writer.writerows(data)

if __name__ == '__main__':
    service = authenticate_gmail()
    data = extract_email_content(service)
    write_to_csv(data)
    print("✅ CSV created: german_phrases.csv")

