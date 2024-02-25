from datetime import datetime, timedelta


def get_time(user_input):
    hour, minute = map(int, user_input.split(":"))
    return time(hour, minute)


start = datetime.combine((date(2023, 6, 6)), get_time(input("Начало рабочего дня: ")))
finish = datetime.combine((date(2023, 6, 6)), get_time(input("Конец рабочего дня: ")))
if timedelta(hours=8, minutes=45) > (finish - start):
    delta = timedelta(hours=8, minutes=45) - (finish - start)
    print(f"Недоработка: {delta.seconds / 60}")
else:
    delta = (finish - start) - timedelta(hours=8, minutes=45)
    print(f"Переработка: {delta.seconds / 60}")