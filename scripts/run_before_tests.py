import os, datetime


date_before, date_now, date_tomorrow = (datetime.datetime.now() - datetime.timedelta(days=1)).date(), datetime.datetime.now().date(), (datetime.datetime.now() + datetime.timedelta(days=1)).date()
date_before, date_now, date_tomorrow = f"{date_before.day}.{date_before.month}.{date_before.year}", f"{date_now.day}.{date_now.month}.{date_now.year}", f"{date_tomorrow.day}.{date_tomorrow.month}.{date_tomorrow.year}"

with open(os.path.join("examples", "forbidding_file_example.txt"), "r", encoding="utf-8") as file:
    content = file.read().format(date_before, date_now, date_tomorrow)

with open(os.path.join("examples", "forbidding_file.txt"), "w", encoding="utf-8") as file:
    file.write(content)
