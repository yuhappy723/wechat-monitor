import requests
from bs4 import BeautifulSoup
import datetime
import json
import os

# ====== 配置区 ======
WECHAT_NAME = "这里替换成公众号名称"
FEISHU_WEBHOOK = "这里替换成飞书Webhook地址"
STATE_FILE = "state.json"
# ===================

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
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"content": "公众号新推文", "tag": "plain_text"}},
            "elements": [
                {"tag": "div", "text": {"content": f"**{title}**", "tag": "lark_md"}},
                {"tag": "action",
                 "actions": [{
                     "tag": "button",
                     "text": {"content": "查看原文", "tag": "plain_text"},
                     "url": link,
                     "type": "default"
                 }]}
            ]
        }
    }

    requests.post(FEISHU_WEBHOOK, json=payload)
    history.append(link)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False)
