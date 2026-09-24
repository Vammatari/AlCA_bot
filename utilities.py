import re

def clean_cell(val):
    """Функция для очистки ячеек от лишних символов и слов"""
    if not isinstance(val, str):
        return val
    
    # Шаблон ищет отдельные слова/буквы A, H, C и Rivalry (без учета регистра)
    pattern = r'\b(A|H|C|Rivalry)\b'
    cleaned = re.sub(pattern, '', val, flags=re.IGNORECASE)
    
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Возвращаем None, если ячейка стала пустой
    return cleaned if cleaned else None 