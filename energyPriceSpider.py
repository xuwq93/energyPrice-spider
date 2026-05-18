import requests
import csv
import os
from datetime import datetime
import time
from urllib.parse import quote

# 当前时间
time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# GBK urlencode
def gbk_quote(s):
    return quote(s.encode("gbk"))

# 当前时间戳
timestamp = int(time.time() * 1000)

# time 参数
time_param = quote(
    " where  DATE_FORMAT(END_DATE,'%Y-%m-%d') >= '-0002-11-30'"
)

# CCTD接口
cctd_url = (
    "https://www.cctd.com.cn/datasql.php?"
    f"data={gbk_quote('CCTD秦皇岛动力煤价格')}"
    f"&name={gbk_quote('CCTD秦皇岛动力煤价格')}"
    f"&time={time_param}"
    "&draw=1"
    "&start=0"
    "&length=10"
    "&search[value]="
    "&search[regex]=false"
    "&extra_search="
    f"&_={timestamp}"
)

# 配置接口
urls = [
    {
        "type": "中国LNG出厂价格（全国）",
        "url": "https://www.shpgx.com/marketzhishu/list/3/22"
    },
    {
        "type": "中国汽柴油批发价格",
        "url": "https://www.shpgx.com/marketzhishu/list2"
    },
    {
        "type": "CCTD秦皇岛动力煤价格",
        "url": cctd_url
    }
]

file_exists = os.path.exists("data.csv")

# 超过100行时清空数据，只保留header
if file_exists:
    with open("data.csv", "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if len(rows) >= 100:
        with open("data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0])  # 只保留header

with open("data.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["datetime", "type", "data"])

    for item in urls:
        try:
            response = requests.get(item["url"], timeout=30)

            print(response.url)

            response.raise_for_status()

            data = response.json()

            print(f"{item['type']} 获取成功")

            writer.writerow([
                time_str,
                item["type"],
                str(data)
            ])

        except Exception as e:
            print(f"{item['type']} 获取失败: {e}")

print("保存完成")
