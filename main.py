import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# ===== 配置区（你只改这里） =====
WECHAT_NAME = "工程质量检测交流"
WPS_WEBHOOK = "https://www.kdocs.cn/chatflow/api/v2/func/webhook/37Eu6NBevYdhCyrGGDMirmr8yA5"
STATE_FILE = "state.json"
# ================================

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = f"https://weixin.sogou.com/weixin?type=2&query={WECHAT_NAME}"
res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

articles = soup.select(".news-list li")

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

for a in articles[:3]:
    title = a.select_one("h3").get_text(strip=True)
    link = a.select_one("a")["href"]

    if link in history:
        continue

    payload = {
        "account": WECHAT_NAME,
        "title": title,
        "link": link,
        "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    requests.post(WPS_WEBHOOK, json=payload, timeout=10)
    history.append(link)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False)
