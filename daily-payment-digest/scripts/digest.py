#!/usr/bin/env python3
"""
📰 Daily Payment Tech Digest — OpenClaw Skill
Chạy qua OpenClaw, output format đẹp cho Telegram.

Usage:
    python3 digest.py                  # Tạo bản tin hôm nay
    python3 digest.py --date 2026-02-10
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

# Fix encoding cho Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ==============================================================================
# CONFIGURABLE SETTINGS — đọc từ ~/.openclaw/.env
# ==============================================================================

DIGEST_SEARCH_DELAY = float(os.environ.get("DIGEST_SEARCH_DELAY", "0.8"))
DIGEST_TIMELIMIT = os.environ.get("DIGEST_TIMELIMIT", "w")       # d=ngày, w=tuần, m=tháng
DIGEST_MAX_RESULTS = int(os.environ.get("DIGEST_MAX_RESULTS", "5"))
DIGEST_SNIPPET_LENGTH = int(os.environ.get("DIGEST_SNIPPET_LENGTH", "150"))
DIGEST_OUTPUT_DIR = os.environ.get("DIGEST_OUTPUT_DIR", str(Path.home() / "digests"))

# Expand ~ nếu có
if DIGEST_OUTPUT_DIR.startswith("~"):
    DIGEST_OUTPUT_DIR = os.path.expanduser(DIGEST_OUTPUT_DIR)

# ==============================================================================
# SEARCH CATEGORIES
# ==============================================================================

SEARCH_CATEGORIES = [
    {
        "icon": "🌐",
        "name": "Công nghệ Thanh toán",
        "queries": [
            ("payment technology innovation 2026", "wt-wt"),
            ("new payment protocol standard launch", "wt-wt"),
            ("real-time payments RTP FedNow instant", "wt-wt"),
            ("open banking PSD3 API payment fintech", "wt-wt"),
            ("ISO 20022 SWIFT payment messaging migration", "wt-wt"),
            ("embedded finance payment platform 2026", "wt-wt"),
        ],
        "top_n": 5,
        "keywords": ["payment", "fintech", "banking", "transaction", "checkout",
                     "merchant", "acquiring", "issuing", "settlement", "clearing",
                     "POS", "terminal", "wallet", "transfer", "remittance"],
    },
    {
        "icon": "🏦",
        "name": "Visa · Mastercard · Card Networks",
        "queries": [
            ("Visa payment technology launch news", "wt-wt"),
            ("Mastercard innovation payment news", "wt-wt"),
            ("Visa Mastercard tokenization network update", "wt-wt"),
            ("American Express UnionPay JCB card news", "wt-wt"),
            ("tap to pay contactless card network", "wt-wt"),
        ],
        "top_n": 5,
        "keywords": ["visa", "mastercard", "card", "payment", "network",
                     "tokenization", "amex", "unionpay", "jcb", "discover",
                     "acquiring", "issuing", "tap to pay", "contactless",
                     "cardholder", "merchant"],
    },
    {
        "icon": "⛓️",
        "name": "Blockchain · Crypto Payments",
        "queries": [
            ("blockchain payment settlement fintech 2026", "wt-wt"),
            ("x402 HTTP payment protocol blockchain", "wt-wt"),
            ("stablecoin USDC USDT payment regulation", "wt-wt"),
            ("CBDC central bank digital currency launch", "wt-wt"),
            ("crypto payment adoption merchant rails", "wt-wt"),
        ],
        "top_n": 5,
        "keywords": ["blockchain", "crypto", "stablecoin", "CBDC", "DeFi",
                     "x402", "settlement", "payment", "digital currency",
                     "token", "ripple", "USDC", "USDT", "web3", "on-chain"],
    },
    {
        "icon": "🤖",
        "name": "Agentic Commerce · AI Payments",
        "queries": [
            ("agentic commerce AI payment checkout 2026", "wt-wt"),
            ("Google UCP universal commerce protocol agentic", "wt-wt"),
            ("AI agent shopping payment automation", "wt-wt"),
            ("machine-to-machine payment M2M IoT", "wt-wt"),
            ("LLM AI commerce checkout transaction", "wt-wt"),
        ],
        "top_n": 5,
        "keywords": ["agentic", "AI", "commerce", "payment", "checkout",
                     "UCP", "agent", "shopping", "M2M", "machine",
                     "automation", "LLM", "GPT", "Gemini", "protocol"],
    },
    {
        "icon": "📅",
        "name": "Events · Hội nghị",
        "queries": [
            ("payment fintech conference summit 2026", "wt-wt"),
            ("Money 20/20 Sibos payment event 2026", "wt-wt"),
            ("sự kiện fintech thanh toán Việt Nam 2026", "vn-vi"),
            ("hội nghị công nghệ tài chính ngân hàng Việt Nam", "vn-vi"),
        ],
        "top_n": 4,
        "keywords": ["conference", "summit", "event", "forum", "expo",
                     "payment", "fintech", "banking", "hội nghị", "sự kiện",
                     "workshop", "hackathon", "award"],
    },
    {
        "icon": "🇻🇳",
        "name": "Thanh toán Việt Nam",
        "queries": [
            ("NAPAS thanh toán liên ngân hàng cập nhật", "vn-vi"),
            ("NHNN chính sách thanh toán không dùng tiền mặt", "vn-vi"),
            ("VNPay MoMo ZaloPay ví điện tử tin mới", "vn-vi"),
            ("QR code thanh toán ngân hàng Việt Nam", "vn-vi"),
            ("fintech công nghệ thanh toán Việt Nam 2026", "vn-vi"),
        ],
        "top_n": 5,
        "keywords": ["thanh toán", "ngân hàng", "payment", "NAPAS", "NHNN",
                     "VNPay", "MoMo", "ZaloPay", "QR", "ví điện tử",
                     "fintech", "chuyển tiền", "thẻ", "ATM", "tín dụng"],
    },
]

# Noise filter — loại các bài viết chắc chắn không liên quan
NOISE_KEYWORDS = [
    "nfl", "premier league", "soccer", "football", "basketball", "baseball",
    "casino", "gambling", "slots", "betting", "poker",
    "h-1b visa", "immigration visa", "travel visa",
    "real estate", "bất động sản", "mua nhà",
    "dating", "recipe", "weather forecast",
]

# ==============================================================================
# SEARCH ENGINE — Tavily > DuckDuckGo
# ==============================================================================

def search_web(query, max_results=5, region="wt-wt"):
    """Tìm kiếm web — Tavily (nếu có) → DuckDuckGo"""
    if os.environ.get("TAVILY_API_KEY"):
        results = _search_tavily(query, max_results)
        if results:
            return results
    return _search_ddg(query, max_results, region)


def _search_tavily(query, max_results=5):
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return None
    try:
        payload = json.dumps({
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "topic": "news",
            "max_results": max_results,
            "include_answer": False,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode())
        results = []
        for r in data.get("results", []):
            results.append({
                "title": r.get("title", "").strip(),
                "url": r.get("url", ""),
                "snippet": r.get("content", "").strip(),
                "source": _extract_domain(r.get("url", "")),
                "date": "",
            })
        return results
    except Exception:
        return None


def _search_ddg(query, max_results=5, region="wt-wt"):
    DDGS = None
    try:
        from ddgs import DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            return []
    results = []
    try:
        ddgs = DDGS()
        raw = list(ddgs.news(query, region=region, timelimit=DIGEST_TIMELIMIT, max_results=max_results))
        for r in raw:
            results.append({
                "title": r.get("title", "").strip(),
                "url": r.get("url", ""),
                "snippet": r.get("body", "").strip(),
                "source": r.get("source", ""),
                "date": r.get("date", ""),
            })
    except Exception:
        time.sleep(1)
        try:
            ddgs = DDGS()
            raw = list(ddgs.text(query, region=region, timelimit=DIGEST_TIMELIMIT, max_results=max_results))
            for r in raw:
                results.append({
                    "title": r.get("title", "").strip(),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "").strip(),
                    "source": _extract_domain(r.get("href", "")),
                    "date": "",
                })
        except Exception:
            pass
    return results


def _extract_domain(url):
    try:
        return url.split("/")[2].replace("www.", "")
    except Exception:
        return ""


def _format_date(date_str):
    if not date_str:
        return ""
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%d/%m")
        return date_str[:10]
    except Exception:
        return date_str[:10] if len(date_str) >= 10 else date_str


# ==============================================================================
# DIGEST BUILDER
# ==============================================================================

def build_digest(date_str=None):
    """Tạo bản tin — output format đẹp cho Telegram"""
    today = date_str or datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.strptime(today, "%Y-%m-%d").strftime("%d/%m/%Y")

    # Global dedup across all categories
    global_seen_urls = set()

    # Thu thập tin từ tất cả chuyên mục
    all_sections = []
    total_articles = 0

    for cat in SEARCH_CATEGORIES:
        print(f"🔍 Đang tìm: {cat['icon']} {cat['name']}...", file=sys.stderr)
        articles = []

        for query, region in cat["queries"]:
            effective_top_n = cat.get("top_n", DIGEST_MAX_RESULTS)
            results = search_web(query, max_results=effective_top_n + 3, region=region)
            for r in results:
                url = r.get("url", "")
                if url and url not in global_seen_urls:
                    global_seen_urls.add(url)
                    articles.append(r)
            time.sleep(DIGEST_SEARCH_DELAY)

        # Lọc bỏ bài không liên quan
        articles = _filter_articles(articles, cat.get("keywords", []))

        # Giới hạn top N
        top_n = cat.get("top_n", DIGEST_MAX_RESULTS)
        articles = articles[:top_n]
        total_articles += len(articles)

        all_sections.append({
            "icon": cat["icon"],
            "name": cat["name"],
            "articles": articles,
        })

    # Format output
    output = _format_telegram(all_sections, today_display, total_articles)
    return output


def _filter_articles(articles, relevance_keywords):
    """Lọc bài viết: loại noise, ưu tiên bài liên quan"""
    filtered = []
    for a in articles:
        title = a.get("title", "").strip()
        snippet = a.get("snippet", "").strip()
        text = f"{title} {snippet}".lower()

        # Bỏ title quá ngắn
        if len(title) < 15:
            continue

        # Bỏ noise
        is_noise = False
        for noise in NOISE_KEYWORDS:
            if noise in text:
                is_noise = True
                break
        if is_noise:
            continue

        # Tính relevance score
        score = 0
        for kw in relevance_keywords:
            if kw.lower() in text:
                score += 1

        a["_relevance"] = score
        filtered.append(a)

    # Sắp xếp theo relevance (cao → thấp)
    filtered.sort(key=lambda x: x.get("_relevance", 0), reverse=True)
    return filtered


def _format_telegram(sections, today_display, total_articles):
    """Format bản tin đẹp cho Telegram"""
    lines = []

    # ═══ HEADER ═══
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📰 𝗗𝗔𝗜𝗟𝗬 𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗧𝗘𝗖𝗛 𝗗𝗜𝗚𝗘𝗦𝗧")
    lines.append(f"📅 {today_display}  ·  NAPAS Research")
    lines.append(f"📊 {total_articles} tin nổi bật hôm nay")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    # ═══ MỤC LỤC ═══
    for sec in sections:
        count = len(sec["articles"])
        lines.append(f"  {sec['icon']} {sec['name']} ({count})")
    lines.append("")

    # ═══ TỪNG CHUYÊN MỤC ═══
    for sec in sections:
        lines.append("┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈")
        lines.append(f"{sec['icon']} 𝗧𝗜𝗡 {sec['name'].upper()}")
        lines.append("┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈")
        lines.append("")

        if not sec["articles"]:
            lines.append("  ℹ️ Không có tin mới tuần này")
            lines.append("")
            continue

        for i, article in enumerate(sec["articles"], 1):
            title = article["title"]
            url = article["url"]
            source = article["source"]
            date = _format_date(article.get("date", ""))
            snippet = article.get("snippet", "")

            # Rút gọn snippet
            if len(snippet) > DIGEST_SNIPPET_LENGTH:
                snippet = snippet[:DIGEST_SNIPPET_LENGTH - 3] + "..."

            # Số thứ tự với emoji
            num_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            num = num_emoji[i - 1] if i <= 10 else f"{i}."

            lines.append(f"{num} {title}")

            # Meta line
            meta = []
            if source:
                meta.append(f"📰 {source}")
            if date:
                meta.append(f"📅 {date}")
            if meta:
                lines.append(f"   {' · '.join(meta)}")

            # Snippet
            if snippet:
                lines.append(f"   💬 {snippet}")

            # Link
            lines.append(f"   🔗 {url}")
            lines.append("")

    # ═══ FOOTER ═══
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("💡 𝗚𝗛𝗜 𝗖𝗛𝗨́")
    lines.append("• Tin tổng hợp tự động từ nhiều nguồn quốc tế & VN")
    lines.append("• Click link để đọc chi tiết bài gốc")
    timelimit_labels = {"d": "1 ngày", "w": "7 ngày", "m": "30 ngày"}
    lines.append(f"• Dữ liệu: {timelimit_labels.get(DIGEST_TIMELIMIT, DIGEST_TIMELIMIT)} gần nhất")
    lines.append(f"• ⏰ Cập nhật lúc {datetime.now().strftime('%H:%M')} — NAPAS Research Bot")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="📰 Daily Payment Tech Digest")
    parser.add_argument("--date", help="Ngày cụ thể (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", help="Custom output path")
    args = parser.parse_args()

    # Build digest
    print("📰 Đang tạo bản tin thanh toán...", file=sys.stderr)
    print("⏳ Thời gian ước tính: 2-3 phút\n", file=sys.stderr)

    digest = build_digest(date_str=args.date)

    # Save to file
    today = args.date or datetime.now().strftime("%Y-%m-%d")
    if args.output:
        out_path = Path(args.output)
    else:
        out_dir = Path(DIGEST_OUTPUT_DIR)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"digest-{today}.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(digest)

    print(f"\n✅ Đã lưu: {out_path}", file=sys.stderr)
    print(f"📊 File size: {out_path.stat().st_size:,} bytes", file=sys.stderr)

    # Print digest to stdout (OpenClaw sẽ đọc stdout)
    print(digest)


if __name__ == "__main__":
    main()
