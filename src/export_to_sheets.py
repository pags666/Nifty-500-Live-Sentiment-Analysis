import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

def push_to_sheet(df, sheet_name):
    import os, json
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from datetime import datetime

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = json.loads(os.environ["GOOGLE"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1le7tQxVkznMvphgOB2T0tGyzb_ByeaOHJ4R9E5piY_A")
    worksheet = sheet.worksheet(sheet_name)

    worksheet.clear()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = [["Stock Name", "Sentiment Score", "", "Date & Time"]]

    for _, row in df.iterrows():
        rows.append([
            row["ticker"],             # Column A
            row["sentiment_score"],   # Column B
            "",                       # Column C
            now                       # Column D
        ])

    worksheet.update(rows)
