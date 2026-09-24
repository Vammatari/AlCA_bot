TEAM_INDEXES = {
    "Florida State": 1,
    "Miami": 2,
    "Michigan": 3,
    "Ohio State": 4,
    "Oregon": 5,
    "Penn State": 6,
    "Texas Tech": 7,
    "USC": 8,
    "Alabama": 9,
    "Florida": 10,
    "LSU": 11,
    "Oklahoma": 12,
    "Ole Miss": 13,
    "South Carolina": 14,
    "Texas": 15,
}

TEAM_EMOJI_DICT = {
    "Oklahoma": "5256203508243278219", # 1
    "South Carolina":"5253669584912821528", # 2
    "Florida State":"5253669314329879481", # 3
    "Miami":"5253641302553176938", # 4
    "Michigan":"5256044259445876677", # 5
    "Ohio State":"5256227959492091357", # 6
    "Oregon":"5253827622529443919", # 7
    "Penn State":"5253816640298067179", # 8
    "Texas Tech":"5254010111394884083", # 9
    "USC":"5253771886738841520", # 10
    "Alabama":"5255994781422623446", # 11
    "Florida":"5253910137441132450", # 12
    "LSU":"5253669314329879481", # 13
    "Ole Miss":"5253588233937262567", # 14
    "Texas":"5253554514149026853", # 15
}

TEAM_USERS_DICT = {
    "Florida State": 384481813,  # Например: 123456789
    "Miami": None,
    "Michigan": None,
    "Ohio State": None,
    "Oregon": None,
    "Penn State": 85541853,
    "Texas Tech": None,
    "USC": None,
    "Alabama": None,
    "Florida": None,
    "LSU": 417871325,
    "Oklahoma": None,
    "Ole Miss": 387284914,
    "South Carolina": None,
    "Texas": None,
}
teams_number = len(TEAM_INDEXES)

def get_team_emoji(team_name: str, fallback_emoji: str = "🏈") -> str:
    """Возвращает HTML-тег кастомного эмодзи для команды"""
    emoji_id = TEAM_EMOJI_DICT.get(team_name)
    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{fallback_emoji}</tg-emoji>'
    return fallback_emoji


def get_team_link(team_name: str) -> str:
    """Оборачивает название команды в ссылку на Telegram ID (если ID заполнен в словаре)"""
    user_id = TEAM_USERS_DICT.get(team_name)
    if user_id:
        return f'<a href="tg://user?id={user_id}">{team_name}</a>'
    return team_name


def format_team(team_name: str) -> str:
    """
    Собирает готовое отображение команды:
    [Кастомный Эмодзи] + [Имя команды со ссылкой или без]
    """
    emoji_tag = get_team_emoji(team_name)
    team_link = get_team_link(team_name)
    return f"{emoji_tag} {team_link}"