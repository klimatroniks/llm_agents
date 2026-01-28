# Минимальный safety-слой, чтобы агент не делал опасных действий.
# Расширишь при необходимости.

BLOCKLIST = {
    "оплати",
    "переведи деньги",
    "купи",
    "сними деньги",
    "удали аккаунт",
}


def is_safe(task: str) -> bool:
    tasks = task.lower()
    return not any(point in tasks for point in BLOCKLIST)
