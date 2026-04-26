import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json


def push_to_sheet(df, sheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load credentials from GitHub secret
    creds_dict = json.loads(os.environ["GOOGLE"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)

    # Open sheet
    sheet = client.open_by_key("1le7tQxVkznMvphgOB2T0tGyzb_ByeaOHJ4R9E5piY_A")
    worksheet = sheet.worksheet(sheet_name)

    # Clear old data
  #  worksheet.clear()

    # Current time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ensure correct types (🔥 important fix)
    df = df.copy()
    df["ticker"] = df["ticker"].astype(str)
   
    # Prepare rows
    rows = [["Stock Name", "Sentiment Score", "", "Date & Time"]]

    for _, row in df.iterrows():
        rows.append([
            str(row["ticker"]),             # Column A
            float(row["sentiment_score"]),  # Column B
            "",                             # Column C
            now                             # Column D
        ])

    # Update sheet
    worksheet.append_rows(rows)
