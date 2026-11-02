import json
import gspread

def fetch_sheet_data(credentials:str, sh_id:str):
    """Забирает все данные из таблицы списком списков"""
    credentials_dict = json.loads(credentials)

    # 3. Авторизуемся в Google Sheets через gspread
    gc = gspread.service_account_from_dict(credentials_dict)


    sh = gc.open_by_key(sh_id)
    worksheet = sh.get_worksheet(1)
    # worksheet = sh.get_worksheet(0)
    raw_data = worksheet.get_all_values()
    return raw_data

