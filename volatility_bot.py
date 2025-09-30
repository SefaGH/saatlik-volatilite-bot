#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, time, math, requests, numpy as np

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MODE = os.environ.get("MODE", "coingecko").lower()
TOP_N = int(os.environ.get("TOP_N", "10"))
MIN_VOLUME_USD = float(os.environ.get("MIN_VOLUME_USD", "1000000"))
MIN_QUOTE_VOL_USDT = float(os.environ.get("MIN_QUOTE_VOL_USDT", "5000000"))

def send_telegram_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()

def coingecko_top_volatility():
    rows = []
    for page in [1,2]:
        url = ("https://api.coingecko.com/api/v3/coins/markets"
               "?vs_currency=usd&order=market_cap_desc&per_page=250"
               f"&page={page}&sparkline=false&price_change_percentage=1h")
        data = requests.get(url, timeout=60).json()
        for c in data:
            pc1h = c.get("price_change_percentage_1h_in_currency")
            if pc1h is None: continue
            rows.append({
                "symbol": (c.get("symbol") or "").upper(),
                "name": c.get("name"),
                "price": c.get("current_price"),
                "pct_change_1h": pc1h,
                "abs_pct": abs(pc1h),
                "volume_24h": c.get("total_volume", 0)
            })
        time.sleep(0.6)
    rows = [r for r in rows if r["volume_24h"] >= MIN_VOLUME_USD]
    rows.sort(key=lambda x: x["abs_pct"], reverse=True)
    return rows[:TOP_N]

def main():
    rows = coingecko_top_volatility()
    if not rows:
        send_telegram_message("⚠️ No data.")
        return
    msg = "📈 <b>Most Volatile Coins (1h)</b>\n"
    msg += "\n".join([f"{i+1}. <b>{r['symbol']}</b> — {r['name']} | ${r['price']:.4f} | 1h: {r['pct_change_1h']:+.2f}%" for i,r in enumerate(rows)])
    send_telegram_message(msg)

if __name__ == "__main__":
    main()
