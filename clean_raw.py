import pandas as pd
from raw_connect import fetch_sheet_data
from utilities import clean_cell
from teams_config import TEAMS_DATA

data = fetch_sheet_data()



def clear_table_data(raw_data,teams_number):
    """очищаем сырые данные от посторонних списков"""

    df = pd.DataFrame(raw_data)
    df_clean_non_week = df[df[0].str.strip().str.lower().str.startswith('week', na=False)] 
    df_clean_non_week = df_clean_non_week.reset_index(drop=True)
    df_clean_non_team = df_clean_non_week.iloc[:, :teams_number + 1]
    clean_table_data = df_clean_non_team
    clean_table_data = clean_table_data.map(clean_cell)
    return clean_table_data


def make_a_schedule(df, teams_dict):
    """Создает расписание матчей по неделям"""
    # 1. Создаем словарь для сопоставления индексов столбцов
    weekly_matchups = {}
    week_col = df.columns[0]  # Первый столбец с неделями

    # 2. Проходим по каждой неделе (строке)
    for _, row in df.iterrows():
        week_name = row[week_col]
        seen_games = set()
        matches = []
        
        # Проходим по каждому столбцу из словаря команд
        for team_in_col, col_idx,  in teams_dict.items():
            col_idx = col_idx["team_index"]
            if col_idx in df.columns:
                opponent = row[col_idx]
                
                # Проверяем, что в ячейке есть соперник (не NaN и не пустота)
                if pd.notna(opponent) and str(opponent).strip() != '':
                    opponent_name = str(opponent).strip()
                    
                    # Создаем отсортированный кортеж, чтобы игра (КомандаА, КомандаБ) 
                    # и зеркальная запись не дублировались
                    game_pair = tuple(sorted([team_in_col, opponent_name]))
                    
                    if game_pair not in seen_games:
                        seen_games.add(game_pair)
                        # matches.append(f"{game_pair[0]} @ {game_pair[1]}")
                        matches.append([game_pair[0],game_pair[1]])
                        
        weekly_matchups[week_name] = matches

    return weekly_matchups


schedule = make_a_schedule(clear_table_data(data, len(TEAMS_DATA)), TEAMS_DATA)

