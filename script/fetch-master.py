#!/usr/bin/env python3
import json
import os
import sys
from playwright.sync_api import sync_playwright

DEST = sys.argv[1] if len(sys.argv) > 1 else "public/master_bk"
URL = "https://noro6.github.io/kc-web/#/aircalc"
TARGET = "/kc-web-data/master.json"

os.makedirs(DEST, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    try:
        page = browser.new_page()
        # 先掛監聽再 goto，避免漏掉回應
        with page.expect_response(
            lambda r: TARGET in r.url and r.ok, timeout=60_000
        ) as resp_info:
            page.goto(URL)
        text = resp_info.value.text()
    finally:
        browser.close()

json.loads(text)  # 確認是合法 JSON，不是錯誤頁

out = os.path.join(DEST, "master.json")
with open(out + ".tmp", "w", encoding="utf-8") as f:
    f.write(text)
os.replace(out + ".tmp", out)  # 驗證通過才覆蓋舊檔
print(f"saved master.json {len(text) / 1024:.0f} KB")