from teams_config import format_team
# from alca_teams import format_team


def format_data_value(value) -> str:
    """Форматирует значения из расписания"""
    if isinstance(value, str):
        return value

    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                team1 = format_team(item[0])
                team2 = format_team(item[1])
                lines.append(f"• {team1} <b>🆚</b> {team2}")
            else:
                lines.append(f"• {item}")
        return "\n".join(lines)

    return str(value)