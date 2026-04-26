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

    creds_dict = json.loads(os.environ["GOOGLE"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1le7tQxVkznMvphgOB2T0tGyzb_ByeaOHJ4R9E5piY_A")
    worksheet = sheet.worksheet(sheet_name)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = df.copy()
    df["ticker"] = df["ticker"].astype(str)

    # 🔥 Check if sheet already has data
    existing_data = worksheet.get_all_values()

    rows = []

    # ✅ Add header ONLY if sheet is empty
    if not existing_data:
        rows.append(["Stock Name", "Sentiment Score", "", "Date & Time"])

    # ✅ Add actual data
    for _, row in df.iterrows():
        rows.append([
            str(row["ticker"]),
            float(row["sentiment_score"]),
            "",
            now
        ])

    # ✅ Append without overwriting
    worksheet.append_rows(rows, value_input_option="RAW")
