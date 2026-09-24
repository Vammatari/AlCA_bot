import os
import json
import gspread
from dotenv import load_dotenv
load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  

CREDENTIALS_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
def fetch_sheet_data():
    """Забирает все данные из таблицы списком списков"""
    credentials_dict = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))

    # 3. Авторизуемся в Google Sheets через gspread
    gc = gspread.service_account_from_dict(credentials_dict)


    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.sheet1
    # worksheet = sh.get_worksheet(0)
    return worksheet.get_all_values()

