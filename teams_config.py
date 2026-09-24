# teams_config.py
import logging
import re

logger = logging.getLogger(__name__)

# Единая база данных по командам
# Заполните user_id числовыми ID пользователей (например: 123456789)
TEAMS_DATA = {
    "Florida State": {
        "emoji_id": "5253603158948617174",
        "username": "shchastye",  # Укажите Telegram username
        "team_index": 1,
    },
    "Penn State": {
        "emoji_id": "5253816640298067179",
        "username": "lespaul88",  # Укажите Telegram username
        "team_index": 6,
    },
    "Michigan": {
        "emoji_id": "5256044259445876677",
        "username": None,  # Укажите Telegram username
        "team_index": 3,
    },
    "Ohio State": {
        "emoji_id": "5256227959492091357",
        "username": None,  # Укажите Telegram username
        "team_index": 4,
    },
    "Oregon": {
        "emoji_id": "5253827622529443919",
        "username": None,  # Укажите Telegram username
        "team_index": 5,
    },
    "Miami": {
        "emoji_id": "5253641302553176938",
        "username": None,  # Укажите Telegram username
        "team_index": 2,
    },
    "Texas Tech": {
        "emoji_id": "5254010111394884083",
        "username": None,  # Укажите Telegram username
        "team_index": 7,
    },
    "USC": {
        "emoji_id": "5253771886738841520",
        "username": None,  # Укажите Telegram username
        "team_index": 8,
    },
    "Alabama": {
        "emoji_id": "5255994781422623446",
        "username": None,  # Укажите Telegram username
        "team_index": 9,
    },
    "Florida": {
        "emoji_id": "5253910137441132450",
        "username": None,  # Укажите Telegram username
        "team_index": 10,
    },
    "LSU": {
        "emoji_id": "5253669314329879481",
        "username": "StasVII",
        "team_index": 11,
    },
    "Oklahoma": {
        "emoji_id": "5256203508243278219",
        "username": None,
        "team_index": 12,
    },
    "Ole Miss": {
        "emoji_id": "5253588233937262567",
        "username": "mahomes15",
        "team_index": 13,
    },
    "South Carolina": {
        "emoji_id": "5253669584912821528",
        "username": None,
        "team_index": 14,
    },
    "Texas": {
        "emoji_id": "5253554514149026853",
        "username": None,
        "team_index": 15,
    },
}

teams_number = len(TEAMS_DATA)







