import requests
import csv
import os
from datetime import datetime

url = "https://www.shpgx.com/marketzhishu/list/3/22"

response = requests.get(url)

# 如果返回的是 json
data = response.json()

print(data)

today = datetime.now().strftime("%Y-%m-%d")

file_exists = os.path.exists("data.csv")

with open("data.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["date", "data"])

    writer.writerow([today, str(data)])

print("保存完成")
