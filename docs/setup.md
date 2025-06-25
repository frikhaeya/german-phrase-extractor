📌 Google API Setup (Detailed Instructions)
You’ll need to do this once to get credentials.json, which allows your script to access your Gmail account securely.

🔧 Step-by-Step: Enable Gmail API + Get credentials.json
1. Go to Google Cloud Console
👉 https://console.cloud.google.com/

2. Create a New Project
Click the project dropdown in the top left corner

Click “New Project”

Name it: Gmail Phrase Extractor

3. Enable Gmail API
In the top search bar, type: Gmail API

Click on it, then click "Enable"

4. Configure OAuth Consent Screen
In the left sidebar: go to "APIs & Services" → "OAuth consent screen"

Choose:

User type: External

App name: German Extractor

User support email: your Gmail

Add yourself as a test user (your Gmail)

Save and continue

5. Create OAuth Credentials
Go to "Credentials" in the left sidebar

Click "Create Credentials" → "OAuth client ID"

Choose:

Application type: Desktop app

Name: Local Script Client

Click "Create"

6. Download credentials.json
After creation, click “Download”

Save the file as credentials.json in the same directory as german_extractor.py

7. First Script Run: Authorize
bash
Copy
Edit
python3 german_extractor.py
A browser will open asking you to log in and allow access to Gmail

After granting permission, a token.json will be created — this stores your access so you don’t have to log in again

📁 Your Folder Should Look Like:
pgsql
Copy
Edit
📦 gmail_automation_script
 ┣ 📄 german_extractor.py
 ┣ 📄 credentials.json         ← from Google Cloud
 ┣ 📄 token.json               ← created after login
 ┣ 📄 german_phrases.csv
 ┣ 📄 requirements.txt
 ┗ 📄 README.md

