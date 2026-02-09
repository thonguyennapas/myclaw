#!/usr/bin/env python3
"""
Web Search Script - Bộ tìm kiếm web đa engine cho OpenClaw Deep Research
Hỗ trợ: Tavily (tốt nhất) + DuckDuckGo (miễn phí) + Google Custom Search

Engine ưu tiên:
  1. Tavily  — Tốt nhất cho AI research, tự extract nội dung, free 1000 req/tháng
  2. DuckDuckGo — Miễn phí hoàn toàn, không cần API key  
  3. Google — Tốt nhất cho tiếng Việt, free 100 req/ngày

Usage:
    python search.py "blockchain Vietnam"                          # Auto-chọn engine tốt nhất
    python search.py "chính sách blockchain" --region vn-vi        # Tiếng Việt
    python search.py "CBDC 2025" --engine tavily                   # Chỉ định Tavily
    python search.py "blockchain" --engine tavily --depth advanced  # Deep search (Tavily)
    python search.py "NHNN blockchain" --type news --region vn-vi  # Tin tức
    python search.py --batch "kw1;kw2;kw3"                         # Nhiều từ khóa
    python search.py "query" --output results.md --format md       # Lưu file
"""

import argparse
import json
import sys
import os
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

# ============================================================================
# TAVILY SEARCH (Tốt nhất cho AI Research)
# Đăng ký miễn phí: https://tavily.com — Free 1000 req/tháng
# ============================================================================

def search_tavily(query, max_results=10, search_depth="basic", topic="general",
                  include_answer=True, include_raw_content=False, **kwargs):
    """
    Tìm kiếm bằng Tavily - AI-native search engine
    Tốt nhất cho research vì:
    - Kết quả đã được tóm tắt, sạch
    - Tự extract nội dung trang web
    - Trả về AI-generated answer
    
    search_depth: "basic" (nhanh) hoặc "advanced" (sâu hơn, chậm hơn)
    topic: "general" hoặc "news"
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print("❌ Cần TAVILY_API_KEY")
        print("   Đăng ký miễn phí (30 giây): https://app.tavily.com/sign-in")
        print("   Free tier: 1000 requests/tháng")
        print("   → Fallback sang DuckDuckGo...")
        return None  # Signal to fallback

    results = []
    try:
        payload = json.dumps({
            "api_key": api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

        # AI-generated answer
        answer = data.get("answer", "")

        for r in data.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", ""),
                "raw_content": r.get("raw_content", ""),
                "score": r.get("score", 0),
                "source": r.get("url", "").split("/")[2] if r.get("url") else "",
                "date": "",
                "engine": "Tavily",
                "ai_answer": answer if results == [] else ""  # Chỉ gắn answer vào kq đầu
            })

    except urllib.error.HTTPError as e:
        print(f"⚠️ Tavily API error: {e.code} {e.reason}")
        if e.code == 401:
            print("   → API key không hợp lệ. Kiểm tra lại TAVILY_API_KEY")
        return None
    except Exception as e:
        print(f"⚠️ Lỗi Tavily: {e}")
        return None

    return results


# ============================================================================
# DUCKDUCKGO SEARCH (Miễn phí hoàn toàn)
# Không cần API key, không cần đăng ký
# ============================================================================

def search_duckduckgo(query, max_results=10, region="wt-wt", timelimit=None, 
                      search_type="text", **kwargs):
    """
    Tìm kiếm bằng DuckDuckGo (miễn phí, không cần API key)
    DuckDuckGo là search engine hợp pháp của Mỹ (Pennsylvania, est. 2008)
    """
    # Hỗ trợ cả package mới (ddgs) và cũ (duckduckgo_search)
    DDGS = None
    try:
        from ddgs import DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            print("❌ Chưa cài package search. Chạy: pip install ddgs")
            return []

    results = []
    try:
        ddgs = DDGS()
        if search_type == "news":
            raw = list(ddgs.news(
                keywords=query,
                region=region,
                timelimit=timelimit,
                max_results=max_results
            ))
            for r in raw:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("body", ""),
                    "source": r.get("source", ""),
                    "date": r.get("date", ""),
                    "engine": "DuckDuckGo News"
                })
        else:
            raw = list(ddgs.text(
                keywords=query,
                region=region,
                timelimit=timelimit,
                max_results=max_results
            ))
            for r in raw:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "",
                    "date": "",
                    "engine": "DuckDuckGo"
                })
    except Exception as e:
        print(f"⚠️ Lỗi DuckDuckGo: {e}")
        print("💡 Thử lại sau vài giây (rate limiting)")

    return results


# ============================================================================
# GOOGLE CUSTOM SEARCH (Tốt nhất cho tiếng Việt)
# Free: 100 queries/ngày
# Setup: https://developers.google.com/custom-search/v1/overview
# ============================================================================

def search_google(query, max_results=10, api_key=None, cx=None, **kwargs):
    """
    Tìm kiếm bằng Google Custom Search API
    Cần: GOOGLE_API_KEY + GOOGLE_CX (Search Engine ID)
    Free tier: 100 queries/ngày
    """
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    cx = cx or os.environ.get("GOOGLE_CX")

    if not api_key or not cx:
        print("❌ Cần GOOGLE_API_KEY và GOOGLE_CX")
        print("   1. Lấy API key: https://console.cloud.google.com/apis/credentials")
        print("   2. Tạo Search Engine: https://programmablesearchengine.google.com/")
        print("   3. Set env: GOOGLE_API_KEY=xxx GOOGLE_CX=yyy")
        return None

    results = []
    try:
        params = urllib.parse.urlencode({
            "key": api_key,
            "cx": cx,
            "q": query,
            "num": min(max_results, 10)
        })
        url = f"https://www.googleapis.com/customsearch/v1?{params}"

        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Research/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())

        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("displayLink", ""),
                "date": "",
                "engine": "Google"
            })
    except Exception as e:
        print(f"⚠️ Lỗi Google Search: {e}")
        return None

    return results


# ============================================================================
# CONTENT EXTRACTOR - Đọc nội dung trang web
# ============================================================================

def extract_url_content(url, max_chars=5000):
    """
    Đọc nội dung text từ một URL
    Dùng để đọc chi tiết trang web sau khi tìm kiếm
    """
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-Research/1.0)"
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        # Simple HTML to text
        import re
        # Remove scripts and styles
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove tags
        text = re.sub(r'<[^>]+>', ' ', html)
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text[:max_chars]
    except Exception as e:
        return f"[Không thể đọc: {e}]"


# ============================================================================
# AUTO ENGINE SELECTION
# ============================================================================

def auto_search(query, **kwargs):
    """
    Tự động chọn engine tốt nhất:
    1. Tavily (nếu có API key) → tốt nhất
    2. DuckDuckGo (fallback) → miễn phí
    """
    # Try Tavily first
    if os.environ.get("TAVILY_API_KEY"):
        print("🔍 Sử dụng Tavily (AI-optimized search)...")
        results = search_tavily(query, **kwargs)
        if results is not None:
            return results
        print("⚠️ Tavily thất bại, fallback sang DuckDuckGo...")

    # Fallback to DuckDuckGo
    print("🔍 Sử dụng DuckDuckGo...")
    return search_duckduckgo(query, **kwargs)


# ============================================================================
# OUTPUT FORMATTERS
# ============================================================================

def format_text(results, query):
    """Output dạng text"""
    lines = []
    lines.append(f"\n🔍 Kết quả tìm kiếm: \"{query}\"")
    lines.append(f"📊 Tìm thấy: {len(results)} kết quả")
    lines.append(f"🔧 Engine: {results[0].get('engine', 'N/A') if results else 'N/A'}")
    lines.append(f"📅 Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("=" * 70)

    # Show AI answer if available (Tavily)
    if results and results[0].get("ai_answer"):
        lines.append(f"\n🤖 AI Answer:\n{results[0]['ai_answer']}")
        lines.append("-" * 70)

    for i, r in enumerate(results, 1):
        lines.append(f"\n--- Kết quả {i} ---")
        lines.append(f"📌 {r['title']}")
        lines.append(f"🔗 {r['url']}")
        if r.get('snippet'):
            lines.append(f"📝 {r['snippet'][:300]}")
        if r.get('source'):
            lines.append(f"📰 Nguồn: {r['source']}")
        if r.get('date'):
            lines.append(f"📅 Ngày: {r['date']}")
        if r.get('score'):
            lines.append(f"⭐ Relevance: {r['score']:.2f}")

    return "\n".join(lines)


def format_markdown(results, query):
    """Output dạng Markdown"""
    lines = []
    engine = results[0].get('engine', 'N/A') if results else 'N/A'
    lines.append(f"# 🔍 Kết quả: \"{query}\"")
    lines.append(f"\n📊 {len(results)} kết quả | 🔧 {engine} | 📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # AI answer (Tavily)
    if results and results[0].get("ai_answer"):
        lines.append(f"\n## 🤖 AI Summary\n{results[0]['ai_answer']}")

    lines.append(f"\n## Kết quả Chi tiết\n")
    lines.append("| # | Tiêu đề | Nguồn | Tóm tắt |")
    lines.append("|---|---------|-------|---------|")

    for i, r in enumerate(results, 1):
        title = r['title'][:60] if r['title'] else "N/A"
        title_link = f"[{title}]({r['url']})"
        source = r.get('source') or (r['url'].split('/')[2] if r.get('url') else "")
        snippet = r.get('snippet', '')[:100].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {i} | {title_link} | {source} | {snippet} |")

    return "\n".join(lines)


def format_json(results, query):
    """Output dạng JSON"""
    return json.dumps({
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "engine": results[0].get("engine", "N/A") if results else "N/A",
        "count": len(results),
        "ai_answer": results[0].get("ai_answer", "") if results else "",
        "results": results
    }, ensure_ascii=False, indent=2)


# ============================================================================
# BATCH & MULTI-ENGINE SEARCH
# ============================================================================

def batch_search(queries_str, search_func, **kwargs):
    """Tìm kiếm nhiều từ khóa"""
    queries = [q.strip() for q in queries_str.split(";") if q.strip()]
    all_results = {}

    for i, query in enumerate(queries, 1):
        print(f"\n🔍 [{i}/{len(queries)}] Đang tìm: \"{query}\"...")
        results = search_func(query, **kwargs)
        if results is None:
            results = []
        all_results[query] = results
        print(f"   ✅ {len(results)} kết quả")

        if i < len(queries):
            time.sleep(2)  # Rate limiting

    return all_results


def multi_engine_search(query, **kwargs):
    """
    Tìm kiếm trên NHIỀU engine cùng lúc → kết quả phong phú nhất
    Dùng cho deep research
    """
    all_results = []
    
    # Tavily
    if os.environ.get("TAVILY_API_KEY"):
        print("  🔍 Tavily...")
        tavily_results = search_tavily(query, **kwargs)
        if tavily_results:
            all_results.extend(tavily_results)
    
    # DuckDuckGo
    print("  🔍 DuckDuckGo...")
    ddg_results = search_duckduckgo(query, **kwargs)
    if ddg_results:
        all_results.extend(ddg_results)
    
    # Google
    if os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_CX"):
        print("  🔍 Google...")
        google_results = search_google(query, **kwargs)
        if google_results:
            all_results.extend(google_results)
    
    # Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)
    
    print(f"  📊 Tổng: {len(unique_results)} kết quả (deduplicated từ {len(all_results)})")
    return unique_results


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🔍 Web Search đa engine cho OpenClaw Deep Research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python search.py "blockchain Vietnam"                           # Auto engine
  python search.py "chính sách blockchain" --region vn-vi         # Tiếng Việt
  python search.py "CBDC 2025" --engine tavily                    # Tavily (tốt nhất)
  python search.py "CBDC" --engine tavily --depth advanced        # Deep search
  python search.py "NHNN blockchain" --type news                  # Tin tức
  python search.py "blockchain" --engine multi                    # Tất cả engines
  python search.py --batch "kw1;kw2;kw3"                          # Nhiều từ khóa
  python search.py "query" --output results.md --format md        # Lưu file
  python search.py --extract "https://example.com"                # Đọc nội dung URL

Engines:
  auto    — Tự chọn tốt nhất (Tavily → DuckDuckGo) [mặc định]
  tavily  — AI-optimized, cần TAVILY_API_KEY (free 1000 req/tháng)
  ddg     — DuckDuckGo, miễn phí hoàn toàn
  google  — Google, cần GOOGLE_API_KEY + GOOGLE_CX
  multi   — Tìm trên TẤT CẢ engines, deduplicate kết quả
        """
    )

    parser.add_argument("query", nargs="?", help="Từ khóa tìm kiếm")
    parser.add_argument("--batch", help="Nhiều từ khóa phân cách bằng ;")
    parser.add_argument("--extract", help="Đọc nội dung từ URL")
    parser.add_argument("--type", choices=["text", "news"], default="text",
                       help="Loại tìm kiếm (default: text)")
    parser.add_argument("--region", default="wt-wt",
                       help="Vùng (vn-vi: Việt Nam, wt-wt: toàn cầu)")
    parser.add_argument("--max", type=int, default=10,
                       help="Số kết quả tối đa (default: 10)")
    parser.add_argument("--time", choices=["d", "w", "m", "y"],
                       help="Giới hạn thời gian: d=ngày, w=tuần, m=tháng, y=năm")
    parser.add_argument("--engine", choices=["auto", "tavily", "ddg", "google", "multi"],
                       default="auto", help="Search engine (default: auto)")
    parser.add_argument("--depth", choices=["basic", "advanced"], default="basic",
                       help="Độ sâu tìm kiếm Tavily (default: basic)")
    parser.add_argument("--output", help="File lưu kết quả")
    parser.add_argument("--format", choices=["text", "md", "json"], default="text",
                       help="Định dạng output (default: text)")
    parser.add_argument("--status", action="store_true",
                       help="Kiểm tra engines nào sẵn sàng")

    args = parser.parse_args()

    # Status check
    if args.status:
        print("\n🔧 Trạng thái Search Engines:\n")
        tavily_ok = bool(os.environ.get("TAVILY_API_KEY"))
        google_ok = bool(os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_CX"))
        
        print(f"  {'✅' if tavily_ok else '❌'} Tavily     {'— Sẵn sàng' if tavily_ok else '— Cần TAVILY_API_KEY'}")
        print(f"  ✅ DuckDuckGo — Luôn sẵn sàng (miễn phí)")
        print(f"  {'✅' if google_ok else '❌'} Google     {'— Sẵn sàng' if google_ok else '— Cần GOOGLE_API_KEY + GOOGLE_CX'}")
        
        try:
            import ddgs
            print(f"\n  ✅ Package ddgs: đã cài (v{ddgs.__version__})")
        except ImportError:
            try:
                import duckduckgo_search
                print(f"\n  ⚠️ Package duckduckgo-search: đã cài nhưng cũ → pip install ddgs")
            except ImportError:
                print(f"\n  ❌ Package search chưa cài → pip install ddgs")
        
        print(f"\n💡 Khuyến nghị: Đăng ký Tavily miễn phí tại https://app.tavily.com/sign-in")
        return

    # Extract URL content
    if args.extract:
        print(f"\n📖 Đọc nội dung: {args.extract}")
        content = extract_url_content(args.extract)
        print(content)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n💾 Đã lưu: {args.output}")
        return

    if not args.query and not args.batch:
        parser.print_help()
        return

    # Chọn search engine
    engine_map = {
        "auto": auto_search,
        "tavily": search_tavily,
        "ddg": search_duckduckgo,
        "google": search_google,
        "multi": multi_engine_search,
    }
    search_func = engine_map[args.engine]

    search_kwargs = {
        "max_results": args.max,
        "region": args.region,
        "timelimit": args.time,
        "search_type": args.type,
    }
    if args.engine == "tavily":
        search_kwargs["search_depth"] = args.depth
        search_kwargs["topic"] = "news" if args.type == "news" else "general"

    # Batch search
    if args.batch:
        all_results = batch_search(args.batch, search_func, **search_kwargs)
        
        output_parts = []
        for query, results in all_results.items():
            if results:
                if args.format == "md":
                    output_parts.append(format_markdown(results, query))
                elif args.format == "json":
                    output_parts.append(format_json(results, query))
                else:
                    output_parts.append(format_text(results, query))
        
        output = "\n\n---\n\n".join(output_parts)
        print(output)
        
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"\n💾 Đã lưu: {args.output}")
        return

    # Single search
    print(f"\n🔍 Tìm kiếm: \"{args.query}\" (engine: {args.engine})...")
    results = search_func(args.query, **search_kwargs)

    # Handle fallback
    if results is None:
        print("⚠️ Engine không khả dụng, fallback sang DuckDuckGo...")
        results = search_duckduckgo(args.query, **search_kwargs)

    if not results:
        print("❌ Không tìm thấy kết quả. Thử:")
        print("   - Từ khóa khác")
        print("   - Mở rộng phạm vi (bỏ --time)")
        print("   - Engine khác (--engine ddg / tavily)")
        return

    # Format output
    formatters = {"md": format_markdown, "json": format_json, "text": format_text}
    output = formatters[args.format](results, args.query)
    print(output)

    # Save to file
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        ext = Path(args.output).suffix
        if ext == ".json":
            save_content = format_json(results, args.query)
        elif ext == ".md":
            save_content = format_markdown(results, args.query)
        else:
            save_content = output
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(save_content)
        print(f"\n💾 Đã lưu: {args.output}")


if __name__ == "__main__":
    main()
