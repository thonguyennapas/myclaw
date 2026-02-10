#!/usr/bin/env python3
"""
Blockchain Policy Research - Automated Research Script
Thực hiện nghiên cứu tự động về blockchain & chính sách tại Việt Nam.

Usage:
    python research.py --full                    # Nghiên cứu đầy đủ tất cả phần
    python research.py --section trends          # Chỉ nghiên cứu xu hướng
    python research.py --section policy          # Chỉ nghiên cứu chính sách VN
    python research.py --section danang          # Chỉ nghiên cứu Đà Nẵng sandbox
    python research.py --section napas           # Chỉ đề xuất vai trò NAPAS
    python research.py --output ./reports        # Chỉ định thư mục output
    python research.py --format markdown         # Định dạng output (markdown/json)
"""

import argparse
import json
import os
import sys
import datetime
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, field, asdict

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Source:
    """Nguồn tham khảo với metadata kiểm chứng"""
    title: str
    url: str
    publisher: str
    date: str = ""
    reliability: str = "verified"  # verified | secondary | unverified
    
    def to_citation(self) -> str:
        status = {"verified": "✅", "secondary": "⚠️", "unverified": "❌"}
        return f"{status.get(self.reliability, '❓')} [{self.title}]({self.url}) - {self.publisher} ({self.date})"


@dataclass
class Trend:
    """Xu hướng blockchain"""
    name: str
    description: str
    maturity: str  # Emerging | Growth | Pilot | Production
    impact: str    # Thấp | Trung bình | Cao
    scope: str     # Global | Vietnam | Both
    sources: List[Source] = field(default_factory=list)


@dataclass
class PolicyDocument:
    """Văn bản chính sách"""
    name: str
    number: str  # Số/Ký hiệu
    date: str
    issuer: str  # Cơ quan ban hành
    category: str  # Chiến lược | Chương trình | Đề án | Chỉ đạo | Khung thử nghiệm
    blockchain_content: str
    distinction: str  # tech | crypto | both
    source: Source = None


@dataclass
class SandboxInfo:
    """Thông tin sandbox Đà Nẵng"""
    exists: bool
    name: str = ""
    legal_basis: str = ""
    lead_agency: str = ""
    participants: str = ""
    scope: str = ""
    timeline: str = ""
    results: str = ""
    status: str = ""  # proposed | building | approved | active
    sources: List[Source] = field(default_factory=list)
    notes: str = ""


@dataclass
class Scenario:
    """Kịch bản tham gia"""
    name: str
    risk_level: str  # low | medium | high
    description: str
    benefits: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    legal_dependencies: List[str] = field(default_factory=list)
    partners: List[str] = field(default_factory=list)
    kpis: List[str] = field(default_factory=list)
    roadmap_30d: str = ""
    roadmap_60d: str = ""
    roadmap_90d: str = ""


@dataclass
class ResearchReport:
    """Báo cáo nghiên cứu tổng hợp"""
    title: str = "Xu hướng Blockchain & Định hướng Chính sách tại Việt Nam"
    subtitle: str = "Kèm đánh giá Đà Nẵng Sandbox & Đề xuất vai trò NAPAS"
    date: str = ""
    trends: List[Trend] = field(default_factory=list)
    policies: List[PolicyDocument] = field(default_factory=list)
    sandbox: SandboxInfo = None
    scenarios: List[Scenario] = field(default_factory=list)
    roles: List[Dict] = field(default_factory=list)
    executive_summary: str = ""
    all_sources: List[Source] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.datetime.now().strftime("%d/%m/%Y")


# ============================================================================
# RESEARCH KEYWORDS & SEARCH QUERIES
# ============================================================================

SEARCH_QUERIES = {
    "trends": {
        "vi": [
            "xu hướng blockchain 2025 2026",
            "blockchain ứng dụng doanh nghiệp",
            "CBDC ngân hàng trung ương kỹ thuật số",
            "tokenization tài sản thực RWA",
            "blockchain thanh toán xuyên biên giới",
            "blockchain chuỗi cung ứng supply chain",
            "blockchain định danh số DID",
            "blockchain chứng từ điện tử",
            "AI blockchain tích hợp",
        ],
        "en": [
            "blockchain trends 2025 2026 enterprise",
            "CBDC global progress 2025",
            "real world asset tokenization RWA",
            "blockchain cross border payment SWIFT",
            "blockchain supply chain enterprise",
            "decentralized identity DID W3C",
            "blockchain AI integration agentic",
            "permissioned blockchain enterprise adoption",
            "ISO 22739 blockchain standard",
            "blockchain interoperability cross-chain",
        ]
    },
    "policy": {
        "vi": [
            "chính sách blockchain Việt Nam",
            "NHNN blockchain DLT văn bản",
            "Bộ Thông tin truyền thông blockchain",
            "chuyển đổi số Việt Nam blockchain",
            "Quyết định Thủ tướng blockchain",
            "tài sản số tiền mã hóa Việt Nam pháp luật",
            "sandbox fintech Việt Nam NHNN",
            "chiến lược quốc gia blockchain",
            "Nghị quyết chuyển đổi số blockchain",
            "khung pháp lý blockchain Việt Nam",
        ],
        "en": [
            "Vietnam blockchain policy regulation",
            "Vietnam CBDC digital currency SBV",
            "Vietnam fintech sandbox regulation",
            "Vietnam crypto regulation legal framework",
            "Vietnam digital transformation blockchain",
        ]
    },
    "danang": {
        "vi": [
            "Đà Nẵng sandbox blockchain thí điểm",
            "Đà Nẵng chuyển đổi số blockchain",
            "Đà Nẵng công nghệ blockchain đề án",
            "Đà Nẵng thành phố thông minh blockchain",
            "Đà Nẵng fintech sandbox",
            "UBND Đà Nẵng blockchain",
        ],
        "en": [
            "Da Nang Vietnam blockchain sandbox pilot",
            "Da Nang smart city blockchain",
        ]
    },
    "napas_role": {
        "vi": [
            "NAPAS blockchain hạ tầng thanh toán",
            "trung gian thanh toán blockchain Việt Nam",
            "thanh toán liên ngân hàng blockchain",
            "đối soát ngân hàng blockchain",
            "tokenization chứng từ thanh toán",
        ],
        "en": [
            "payment switch blockchain integration",
            "interbank blockchain settlement",
            "payment infrastructure blockchain permissioned",
            "payment network tokenization",
            "blockchain reconciliation banking",
        ]
    }
}

# ============================================================================
# KNOWN OFFICIAL SOURCES (Verified)
# ============================================================================

OFFICIAL_SOURCES = {
    "government": [
        {"name": "Cổng TTĐT Chính phủ", "url": "https://chinhphu.vn", "type": "primary"},
        {"name": "NHNN Việt Nam (SBV)", "url": "https://sbv.gov.vn", "type": "primary"},
        {"name": "Bộ TT&TT", "url": "https://mic.gov.vn", "type": "primary"},
        {"name": "Bộ KH&CN", "url": "https://most.gov.vn", "type": "primary"},
        {"name": "Bộ Tư pháp", "url": "https://moj.gov.vn", "type": "primary"},
        {"name": "Bộ Tài chính", "url": "https://mof.gov.vn", "type": "primary"},
        {"name": "UBND TP Đà Nẵng", "url": "https://danang.gov.vn", "type": "primary"},
        {"name": "Sở TT&TT Đà Nẵng", "url": "https://tttt.danang.gov.vn", "type": "primary"},
    ],
    "legal": [
        {"name": "Thư viện Pháp luật", "url": "https://thuvienphapluat.vn", "type": "secondary"},
        {"name": "Văn bản Chính phủ", "url": "https://vanban.chinhphu.vn", "type": "primary"},
    ],
    "international": [
        {"name": "World Bank", "url": "https://worldbank.org", "type": "primary"},
        {"name": "BIS (Bank for International Settlements)", "url": "https://bis.org", "type": "primary"},
        {"name": "IMF", "url": "https://imf.org", "type": "primary"},
        {"name": "World Economic Forum", "url": "https://weforum.org", "type": "primary"},
        {"name": "Gartner", "url": "https://gartner.com", "type": "secondary"},
        {"name": "McKinsey", "url": "https://mckinsey.com", "type": "secondary"},
    ]
}

# ============================================================================
# REPORT GENERATORS
# ============================================================================

class ReportGenerator:
    """Generate Markdown reports from research data"""
    
    def __init__(self, report: ResearchReport, output_dir: str = "./reports"):
        self.report = report
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all(self):
        """Generate all report files"""
        self.generate_full_report()
        self.generate_executive_summary()
        self.generate_trend_map()
        self.generate_policy_matrix()
        self.generate_danang_sandbox()
        self.generate_napas_roadmap()
        self.generate_sources()
        print(f"\n✅ Tất cả báo cáo đã được tạo tại: {self.output_dir}")
    
    def generate_full_report(self):
        """Generate full consolidated report"""
        md = []
        md.append(f"# {self.report.title}")
        md.append(f"## {self.report.subtitle}")
        md.append(f"\n📅 Ngày: {self.report.date}")
        md.append(f"\n---\n")
        
        # Executive Summary
        if self.report.executive_summary:
            md.append("## Executive Summary\n")
            md.append(self.report.executive_summary)
            md.append("\n---\n")
        
        # Part A: Trends
        md.append("## PHẦN A: THỊ TRƯỜNG & XU HƯỚNG\n")
        md.append(self._render_trends())
        md.append("\n---\n")
        
        # Part B: Policies
        md.append("## PHẦN B: CHÍNH SÁCH VIỆT NAM\n")
        md.append(self._render_policies())
        md.append("\n---\n")
        
        # Part C: Da Nang Sandbox
        md.append("## PHẦN C: ĐÀ NẴNG SANDBOX\n")
        md.append(self._render_sandbox())
        md.append("\n---\n")
        
        # Part D: NAPAS Roles
        md.append("## PHẦN D: VAI TRÒ THAM GIA NAPAS\n")
        md.append(self._render_scenarios())
        md.append("\n---\n")
        
        # Sources
        md.append("## NGUỒN THAM KHẢO\n")
        md.append(self._render_sources())
        
        self._write_file("report.md", "\n".join(md))
    
    def generate_executive_summary(self):
        """Generate executive summary as separate file"""
        md = []
        md.append(f"# Executive Summary")
        md.append(f"## {self.report.title}")
        md.append(f"\n📅 {self.report.date}\n")
        
        if self.report.executive_summary:
            md.append(self.report.executive_summary)
        else:
            md.append("*⚠️ Executive Summary chưa được viết. Cần hoàn thành các phần nghiên cứu trước.*")
        
        self._write_file("executive-summary.md", "\n".join(md))
    
    def generate_trend_map(self):
        """Generate trend map"""
        md = []
        md.append("# Bản đồ Xu hướng Blockchain\n")
        md.append(f"📅 Cập nhật: {self.report.date}\n")
        
        if self.report.trends:
            md.append("| # | Xu hướng | Mô tả | Phạm vi | Mức trưởng thành | Tác động | Nguồn |")
            md.append("|---|---------|-------|---------|-------------------|----------|-------|")
            for i, t in enumerate(self.report.trends, 1):
                sources_str = ", ".join([s.to_citation() for s in t.sources]) if t.sources else "⚠️ Cần bổ sung"
                md.append(f"| {i} | **{t.name}** | {t.description} | {t.scope} | {t.maturity} | {t.impact} | {sources_str} |")
        else:
            md.append("*Chưa có dữ liệu xu hướng. Chạy nghiên cứu để cập nhật.*")
        
        self._write_file("trend-map.md", "\n".join(md))
    
    def generate_policy_matrix(self):
        """Generate policy matrix"""
        md = []
        md.append("# Bảng Tổng hợp Chính sách Blockchain Việt Nam\n")
        md.append(f"📅 Cập nhật: {self.report.date}\n")
        
        md.append("## Phân biệt: Blockchain Công nghệ vs Tài sản số\n")
        md.append("| Blockchain Công nghệ | Tài sản số / Crypto |")
        md.append("|---------------------|---------------------|")
        md.append("| DLT infrastructure | Tiền mã hóa |")
        md.append("| Smart contract platform | Token/NFT trading |")
        md.append("| Enterprise blockchain | Sàn giao dịch crypto |")
        md.append("| Identity management | ICO/IEO/IDO |")
        md.append("| Supply chain tracking | Mining operations |")
        md.append("| Digital document verification | Stablecoin issuance |")
        md.append("| → **Được khuyến khích phát triển** | → **Đang chờ khung pháp lý** |")
        md.append("")
        
        if self.report.policies:
            md.append("## Danh sách Văn bản\n")
            md.append("| # | Tên văn bản | Số/Ký hiệu | Ngày | Cơ quan | Phân loại | Nội dung blockchain | Phạm vi | Link |")
            md.append("|---|-----------|-------------|------|---------|-----------|---------------------|---------|------|")
            for i, p in enumerate(self.report.policies, 1):
                link = f"[Nguồn]({p.source.url})" if p.source else "⚠️"
                distinction = {"tech": "Công nghệ", "crypto": "Tài sản số", "both": "Cả hai"}.get(p.distinction, p.distinction)
                md.append(f"| {i} | {p.name} | {p.number} | {p.date} | {p.issuer} | {p.category} | {p.blockchain_content} | {distinction} | {link} |")
        else:
            md.append("*Chưa có dữ liệu chính sách. Chạy nghiên cứu để cập nhật.*")
        
        self._write_file("policy-matrix.md", "\n".join(md))
    
    def generate_danang_sandbox(self):
        """Generate Da Nang sandbox analysis"""
        md = []
        md.append("# Phân tích Đà Nẵng Blockchain Sandbox\n")
        md.append(f"📅 Cập nhật: {self.report.date}\n")
        
        if self.report.sandbox:
            sb = self.report.sandbox
            status_emoji = "✅" if sb.exists else "❌"
            md.append(f"## Kết luận: {status_emoji} {'CÓ' if sb.exists else 'CHƯA CÓ'} sandbox blockchain chính thức\n")
            
            if sb.exists:
                md.append("| Hạng mục | Chi tiết |")
                md.append("|----------|---------|")
                md.append(f"| Tên đề án/sandbox | {sb.name} |")
                md.append(f"| Cơ sở pháp lý | {sb.legal_basis} |")
                md.append(f"| Cơ quan chủ trì | {sb.lead_agency} |")
                md.append(f"| Đối tượng tham gia | {sb.participants} |")
                md.append(f"| Phạm vi thử nghiệm | {sb.scope} |")
                md.append(f"| Thời hạn | {sb.timeline} |")
                md.append(f"| Kết quả | {sb.results} |")
            else:
                md.append("### Thông tin gần nhất\n")
                if sb.notes:
                    md.append(sb.notes)
            
            if sb.sources:
                md.append("\n### Bảng chứng cứ nguồn\n")
                md.append("| # | Thông tin | Trạng thái | Nguồn | Độ tin cậy |")
                md.append("|---|-----------|------------|-------|------------|")
                for i, s in enumerate(sb.sources, 1):
                    md.append(f"| {i} | {s.title} | {sb.status} | [{s.publisher}]({s.url}) | {s.reliability} |")
        else:
            md.append("*Chưa có dữ liệu Đà Nẵng sandbox. Chạy nghiên cứu để cập nhật.*")
        
        self._write_file("danang-sandbox.md", "\n".join(md))
    
    def generate_napas_roadmap(self):
        """Generate NAPAS roadmap"""
        md = []
        md.append("# Lộ trình & Đề xuất Vai trò NAPAS trong Blockchain\n")
        md.append(f"📅 Cập nhật: {self.report.date}\n")
        
        # Roles
        if self.report.roles:
            md.append("## Vai trò Khả thi\n")
            md.append("| # | Vai trò | Mô tả | Lợi thế NAPAS | Ưu tiên |")
            md.append("|---|---------|-------|---------------|---------|")
            for i, r in enumerate(self.report.roles, 1):
                md.append(f"| {i} | **{r['name']}** | {r['description']} | {r['advantage']} | {r['priority']} |")
        
        # Scenarios
        if self.report.scenarios:
            md.append("\n## Kịch bản Tham gia\n")
            for i, sc in enumerate(self.report.scenarios, 1):
                risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(sc.risk_level, "⚪")
                risk_label = {"low": "THẤP", "medium": "TRUNG BÌNH", "high": "CAO"}.get(sc.risk_level, sc.risk_level)
                
                md.append(f"### Kịch bản {i}: {sc.name}")
                md.append(f"**Mức rủi ro**: {risk_emoji} {risk_label}\n")
                md.append(f"**Mô tả**: {sc.description}\n")
                
                if sc.benefits:
                    md.append("**Lợi ích**:")
                    for b in sc.benefits:
                        md.append(f"- {b}")
                
                if sc.risks:
                    md.append("\n**Rủi ro**:")
                    for r in sc.risks:
                        md.append(f"- {r}")
                
                if sc.legal_dependencies:
                    md.append("\n**Phụ thuộc pháp lý**:")
                    for l in sc.legal_dependencies:
                        md.append(f"- {l}")
                
                if sc.partners:
                    md.append("\n**Đối tác cần có**:")
                    for p in sc.partners:
                        md.append(f"- {p}")
                
                if sc.kpis:
                    md.append("\n**KPI đề xuất**:")
                    for k in sc.kpis:
                        md.append(f"- {k}")
                
                md.append(f"\n**Lộ trình**:")
                md.append(f"- 📅 30 ngày: {sc.roadmap_30d}")
                md.append(f"- 📅 60 ngày: {sc.roadmap_60d}")
                md.append(f"- 📅 90 ngày: {sc.roadmap_90d}")
                md.append("")
        else:
            md.append("\n*Chưa có kịch bản tham gia. Chạy nghiên cứu để cập nhật.*")
        
        self._write_file("napas-roadmap.md", "\n".join(md))
    
    def generate_sources(self):
        """Generate sources list"""
        md = []
        md.append("# Danh sách Nguồn Tham khảo\n")
        md.append(f"📅 Cập nhật: {self.report.date}\n")
        
        if self.report.all_sources:
            md.append("## Nguồn đã sử dụng\n")
            md.append("| # | Tiêu đề | Nhà xuất bản | Ngày | Độ tin cậy | Link |")
            md.append("|---|---------|-------------|------|------------|------|")
            for i, s in enumerate(self.report.all_sources, 1):
                md.append(f"| {i} | {s.title} | {s.publisher} | {s.date} | {s.reliability} | [Link]({s.url}) |")
        
        md.append("\n## Nguồn Ưu tiên Tham khảo\n")
        for category, sources in OFFICIAL_SOURCES.items():
            cat_label = {"government": "Cơ quan Nhà nước", "legal": "Pháp luật", "international": "Quốc tế"}.get(category, category)
            md.append(f"### {cat_label}\n")
            for s in sources:
                md.append(f"- [{s['name']}]({s['url']}) ({s['type']})")
            md.append("")
        
        self._write_file("sources.md", "\n".join(md))
    
    def _render_trends(self) -> str:
        if not self.report.trends:
            return "*Chưa có dữ liệu xu hướng. Cần thực hiện nghiên cứu web.*"
        lines = []
        lines.append("### Bản đồ Xu hướng\n")
        lines.append("| # | Xu hướng | Mô tả | Mức trưởng thành | Tác động |")
        lines.append("|---|---------|-------|-------------------|----------|")
        for i, t in enumerate(self.report.trends, 1):
            lines.append(f"| {i} | **{t.name}** | {t.description} | {t.maturity} | {t.impact} |")
        return "\n".join(lines)
    
    def _render_policies(self) -> str:
        if not self.report.policies:
            return "*Chưa có dữ liệu chính sách. Cần thực hiện nghiên cứu web.*"
        lines = []
        lines.append("| # | Tên | Số hiệu | Ngày | Cơ quan | Nội dung blockchain |")
        lines.append("|---|-----|---------|------|---------|---------------------|")
        for i, p in enumerate(self.report.policies, 1):
            lines.append(f"| {i} | {p.name} | {p.number} | {p.date} | {p.issuer} | {p.blockchain_content} |")
        return "\n".join(lines)
    
    def _render_sandbox(self) -> str:
        if not self.report.sandbox:
            return "*Chưa có dữ liệu Đà Nẵng sandbox. Cần thực hiện nghiên cứu web.*"
        sb = self.report.sandbox
        return f"**Kết luận**: {'CÓ' if sb.exists else 'CHƯA CÓ'} sandbox blockchain chính thức tại Đà Nẵng.\n\n{sb.notes or ''}"
    
    def _render_scenarios(self) -> str:
        if not self.report.scenarios:
            return "*Chưa có kịch bản tham gia. Cần thực hiện nghiên cứu.*"
        lines = []
        for i, sc in enumerate(self.report.scenarios, 1):
            lines.append(f"### KB{i}: {sc.name} (Rủi ro: {sc.risk_level})")
            lines.append(f"{sc.description}\n")
        return "\n".join(lines)
    
    def _render_sources(self) -> str:
        if not self.report.all_sources:
            return "*Chưa có nguồn tham khảo.*"
        lines = []
        for i, s in enumerate(self.report.all_sources, 1):
            lines.append(f"{i}. {s.to_citation()}")
        return "\n".join(lines)
    
    def _write_file(self, filename: str, content: str):
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  📄 {filepath}")


# ============================================================================
# TEMPLATE DATA (Pre-populated research framework)
# ============================================================================

def create_template_report() -> ResearchReport:
    """Create a template report with structured framework for research"""
    
    report = ResearchReport()
    
    # Pre-populate trend framework
    report.trends = [
        Trend(
            name="CBDC (Tiền kỹ thuật số NHTW)",
            description="Các NHTW toàn cầu nghiên cứu & thí điểm CBDC. BIS báo cáo 130+ NHTW đang exploring.",
            maturity="Pilot",
            impact="Cao",
            scope="Both",
            sources=[]
        ),
        Trend(
            name="Tokenization Tài sản (RWA)",
            description="Số hóa tài sản thực lên blockchain: trái phiếu, bất động sản, hàng hóa. BlackRock, Franklin Templeton, JP Morgan dẫn đầu.",
            maturity="Growth",
            impact="Cao",
            scope="Global",
            sources=[]
        ),
        Trend(
            name="Blockchain Thanh toán Xuyên biên giới",
            description="SWIFT, Ripple, Visa, Mastercard đang tích hợp blockchain cho cross-border payment, giảm thời gian từ 3-5 ngày xuống real-time.",
            maturity="Growth",
            impact="Cao",
            scope="Global",
            sources=[]
        ),
        Trend(
            name="Enterprise Permissioned Blockchain",
            description="Hyperledger, R3 Corda, Quorum cho enterprise use cases. Ngân hàng & tổ chức tài chính chuyển hướng permissioned.",
            maturity="Production",
            impact="Cao",
            scope="Both",
            sources=[]
        ),
        Trend(
            name="Định danh Số (DID / Verifiable Credentials)",
            description="W3C DID standard, eIDAS 2.0 EU, định danh kỹ thuật số trên blockchain. Liên kết eKYC/KYC.",
            maturity="Growth",
            impact="Trung bình",
            scope="Global",
            sources=[]
        ),
        Trend(
            name="Blockchain + AI / Agentic Workflows",
            description="Tích hợp AI agents với blockchain cho automated workflows, smart contract AI-enhanced, on-chain AI inference.",
            maturity="Emerging",
            impact="Trung bình",
            scope="Global",
            sources=[]
        ),
        Trend(
            name="Supply Chain & Traceability",
            description="Truy xuất nguồn gốc hàng hóa, logistics, phòng chống hàng giả. IBM Food Trust, Walmart, Maersk TradeLens.",
            maturity="Production",
            impact="Trung bình",
            scope="Both",
            sources=[]
        ),
        Trend(
            name="Chứng từ Điện tử / Trade Finance",
            description="Digitalize LC, B/L, invoice trên blockchain. ICC DSI, MLETR, Singapore eBL.",
            maturity="Pilot",
            impact="Cao",
            scope="Both",
            sources=[]
        ),
        Trend(
            name="Stablecoin & Deposit Token",
            description="Bank-issued stablecoin, deposit token cho thanh toán B2B. USDC institutional, JPM Coin, MAS Project Orchid.",
            maturity="Growth",
            impact="Cao",
            scope="Global",
            sources=[]
        ),
        Trend(
            name="Zero Knowledge Proof (ZKP) Privacy",
            description="ZK-rollups, zk-SNARKs cho privacy-preserving blockchain. Tuân thủ regulation mà vẫn bảo mật dữ liệu.",
            maturity="Emerging",
            impact="Trung bình",
            scope="Global",
            sources=[]
        ),
    ]
    
    # Pre-populate roles
    report.roles = [
        {
            "name": "Đầu mối hạ tầng mạng Permissioned",
            "description": "Vận hành blockchain enterprise cho hệ thống thanh toán liên ngân hàng",
            "advantage": "Có sẵn hạ tầng kết nối 50+ ngân hàng, kinh nghiệm vận hành switch",
            "priority": "🔴 Cao"
        },
        {
            "name": "Điều phối Tiêu chuẩn & Kết nối",
            "description": "Xây dựng tiêu chuẩn kỹ thuật kết nối blockchain giữa các ngân hàng thành viên",
            "advantage": "Vai trò trung gian kết nối hiện tại, trust relationship với NH",
            "priority": "🔴 Cao"
        },
        {
            "name": "Dịch vụ Đối soát Liên bên (Smart Reconciliation)",
            "description": "Smart contract tự động đối soát giao dịch liên ngân hàng trên blockchain",
            "advantage": "Core business hiện tại, hiểu sâu quy trình đối soát",
            "priority": "🔴 Cao"
        },
        {
            "name": "Dịch vụ Xác thực / Định danh (eKYC Blockchain)",
            "description": "DID / Verifiable Credentials cho xác thực giao dịch liên ngân hàng",
            "advantage": "Có dữ liệu KYC từ hệ thống ngân hàng, kết nối CCCD/VNeID",
            "priority": "🟡 TB"
        },
        {
            "name": "Tokenization Chứng từ Thanh toán",
            "description": "Số hóa chứng từ thanh toán, ủy nhiệm thu/chi trên blockchain",
            "advantage": "Xử lý hàng triệu giao dịch/ngày, hiểu quy trình chứng từ",
            "priority": "🟡 TB"
        },
    ]
    
    # Pre-populate scenarios
    report.scenarios = [
        Scenario(
            name="PoC Đối soát Liên ngân hàng trên Blockchain",
            risk_level="low",
            description="Xây dựng prototype smart contract để tự động đối soát giao dịch ATM/POS liên ngân hàng. Chạy song song (shadow) với hệ thống hiện tại, không ảnh hưởng production.",
            benefits=[
                "Giảm 50-80% thời gian đối soát (từ T+1 → near real-time)",
                "Phát hiện sai lệch tức thời thay vì cuối ngày",
                "Tích lũy expertise blockchain nội bộ",
                "Ít rủi ro: không ảnh hưởng hệ thống production"
            ],
            risks=[
                "Chi phí R&D team & infrastructure",
                "PoC không đảm bảo sẽ scale production",
                "Cần thuyết phục lãnh đạo về ROI dài hạn"
            ],
            legal_dependencies=[
                "Không yêu cầu phê duyệt pháp lý đặc biệt (internal PoC)",
                "Cần tuân thủ chính sách bảo mật dữ liệu nội bộ",
                "Dữ liệu test phải được anonymized"
            ],
            partners=[
                "Đội ngũ R&D nội bộ NAPAS",
                "1-2 đối tác blockchain technology (Hyperledger, R3...)",
                "Đội vận hành/đối soát hiện tại (domain knowledge)"
            ],
            kpis=[
                "Hoàn thành PoC đúng timeline (90 ngày)",
                "Accuracy đối soát ≥ 99.99% vs hệ thống hiện tại",
                "Thời gian đối soát giảm ≥ 50%",
                "Báo cáo ROI analysis cho phase tiếp theo"
            ],
            roadmap_30d="Khảo sát platform (Hyperledger Besu/Fabric, R3 Corda), setup team, define use case chi tiết",
            roadmap_60d="Phát triển smart contract đối soát, deploy testnet, data migration tool",
            roadmap_90d="Chạy shadow test 2 tuần với dữ liệu thực (anonymized), đánh giá kết quả, báo cáo board"
        ),
        Scenario(
            name="Pilot Tokenization Chứng từ Thanh toán Liên NH",
            risk_level="medium",
            description="Phối hợp 2-3 ngân hàng thí điểm số hóa chứng từ thanh toán (ủy nhiệm thu/chi, lệnh chuyển tiền) trên blockchain permissioned. Verify tính toàn vẹn và traceability.",
            benefits=[
                "Giảm giấy tờ, tăng tốc xử lý chứng từ",
                "Audit trail minh bạch, tamper-proof",
                "Tiền đề cho trade finance digitalization",
                "Vị thế tiên phong trong hệ sinh thái"
            ],
            risks=[
                "Cần NH đối tác sẵn sàng pilot",
                "Thay đổi quy trình nghiệp vụ",
                "Câu hỏi pháp lý về tính hợp lệ chứng từ điện tử trên blockchain",
                "Vấn đề tương thích với hệ thống core banking"
            ],
            legal_dependencies=[
                "Luật Giao dịch điện tử (sửa đổi 2023)",
                "Nghị định hướng dẫn về chứng từ điện tử",
                "Quy định NHNN về giao dịch điện tử trong ngân hàng",
                "Sandbox fintech nếu có"
            ],
            partners=[
                "2-3 ngân hàng thương mại (ưu tiên NHTM lớn đã có interest)",
                "Nhà cung cấp blockchain enterprise (Hyperledger, Polygon CDK...)",
                "Tư vấn pháp lý chuyên blockchain/fintech",
                "NHNN (tham vấn, định hướng)"
            ],
            kpis=[
                "100+ giao dịch pilot thành công",
                "Uptime ≥ 99.9%",
                "Thời gian xử lý chứng từ giảm ≥ 40%",
                "≥ 2 NH đồng ý mở rộng pilot",
                "Báo cáo compliance đầy đủ"
            ],
            roadmap_30d="MoU với NH đối tác, design solution architecture, khảo sát legal framework",
            roadmap_60d="Phát triển platform, smart contract cho chứng từ thanh toán, API integration với core banking test",
            roadmap_90d="Go-live pilot, monitor 4 tuần, đánh giá kết quả, đề xuất mở rộng"
        ),
        Scenario(
            name="Hạ tầng Mạng Blockchain Liên Ngân hàng (BankChain)",
            risk_level="high",
            description="Triển khai permissioned blockchain network kết nối toàn bộ hệ thống ngân hàng thành viên, phục vụ đa dạng use cases: đối soát, chứng từ, KYC sharing, cross-border...",
            benefits=[
                "Định vị NAPAS là hạ tầng blockchain quốc gia cho ngân hàng",
                "Revenue streams mới (node operation, API, consulting)",
                "Nền tảng cho nhiều dịch vụ blockchain trong tương lai",
                "Competitive advantage dài hạn"
            ],
            risks=[
                "Đầu tư lớn (infrastructure, team, operations)",
                "Cần đồng thuận toàn hệ thống NH",
                "Phụ thuộc khung pháp lý quốc gia",
                "Rủi ro technology obsolescence",
                "Cạnh tranh với các platform quốc tế"
            ],
            legal_dependencies=[
                "Phê duyệt NHNN (bắt buộc)",
                "Khung pháp lý cho private blockchain infrastructure",
                "Quy chuẩn kỹ thuật quốc gia cho DLT trong tài chính",
                "Tuân thủ Luật An toàn thông tin mạng",
                "Tuân thủ quy định chống rửa tiền (AML)"
            ],
            partners=[
                "NHNN (chỉ đạo, phê duyệt, giám sát)",
                "Toàn bộ NH thành viên NAPAS (50+ NH)",
                "Đối tác công nghệ cấp enterprise (IBM, Microsoft, Consensys...)",
                "Tư vấn quốc tế (McKinsey, BCG...)",
                "Đối tác bảo mật (security audit firm)"
            ],
            kpis=[
                "Kết nối ≥ 10 NH trong năm đầu",
                "≥ 1,000 giao dịch/ngày trên blockchain",
                "Uptime ≥ 99.99%",
                "Latency < 2 giây cho finality",
                "Pass security audit bởi bên thứ 3",
                "Break-even trong 3-5 năm"
            ],
            roadmap_30d="Đề xuất chiến lược lên NHNN, tham vấn NH lớn, RFI cho technology partner",
            roadmap_60d="Feasibility study, technology selection, consortium governance framework",
            roadmap_90d="Architecture design, MVP scope, pilot selection (3-5 NH), funding proposal"
        ),
    ]
    
    return report


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Blockchain Policy Research - Tự động nghiên cứu blockchain & chính sách VN",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python research.py --full                    # Tạo template báo cáo đầy đủ
  python research.py --section trends          # Template phần xu hướng
  python research.py --section policy          # Template phần chính sách  
  python research.py --output ./my-reports     # Chỉ định thư mục output
  python research.py --queries                 # Hiện danh sách search queries
  python research.py --sources                 # Hiện danh sách nguồn ưu tiên
        """
    )
    
    parser.add_argument("--full", action="store_true", help="Tạo bộ template báo cáo đầy đủ")
    parser.add_argument("--section", choices=["trends", "policy", "danang", "napas", "summary"],
                       help="Tạo template cho một phần cụ thể")
    parser.add_argument("--output", default="./reports", help="Thư mục output (default: ./reports)")
    parser.add_argument("--queries", action="store_true", help="Hiện danh sách search queries gợi ý")
    parser.add_argument("--sources", action="store_true", help="Hiện danh sách nguồn ưu tiên")
    parser.add_argument("--json", action="store_true", help="Output dạng JSON thay vì Markdown")
    
    args = parser.parse_args()
    
    if args.queries:
        print("\n📋 SEARCH QUERIES GỢI Ý CHO NGHIÊN CỨU\n")
        for category, queries in SEARCH_QUERIES.items():
            cat_label = {
                "trends": "Xu hướng Blockchain",
                "policy": "Chính sách VN", 
                "danang": "Đà Nẵng Sandbox",
                "napas_role": "Vai trò NAPAS"
            }.get(category, category)
            print(f"\n### {cat_label}")
            for lang, q_list in queries.items():
                print(f"  [{lang.upper()}]:")
                for q in q_list:
                    print(f"    - \"{q}\"")
        return
    
    if args.sources:
        print("\n📚 NGUỒN ƯU TIÊN THAM KHẢO\n")
        for category, sources in OFFICIAL_SOURCES.items():
            cat_label = {
                "government": "Cơ quan Nhà nước",
                "legal": "Pháp luật",
                "international": "Quốc tế"
            }.get(category, category)
            print(f"\n### {cat_label}")
            for s in sources:
                print(f"  [{s['type'].upper()}] {s['name']}: {s['url']}")
        return
    
    # Create template report
    report = create_template_report()
    generator = ReportGenerator(report, args.output)
    
    if args.full:
        print("\n🔬 TẠO BỘ TEMPLATE BÁO CÁO ĐẦY ĐỦ\n")
        generator.generate_all()
    elif args.section:
        section_map = {
            "trends": generator.generate_trend_map,
            "policy": generator.generate_policy_matrix,
            "danang": generator.generate_danang_sandbox,
            "napas": generator.generate_napas_roadmap,
            "summary": generator.generate_executive_summary,
        }
        print(f"\n🔬 TẠO TEMPLATE: {args.section}\n")
        section_map[args.section]()
    else:
        # Default: generate all
        print("\n🔬 TẠO BỘ TEMPLATE BÁO CÁO ĐẦY ĐỦ\n")
        print("💡 Sử dụng --help để xem tất cả options\n")
        generator.generate_all()
    
    if args.json:
        json_path = Path(args.output) / "report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(asdict(report), f, ensure_ascii=False, indent=2)
        print(f"\n  📄 JSON: {json_path}")
    
    print("\n✅ Hoàn tất! Sử dụng các báo cáo template để fill dữ liệu nghiên cứu thực tế.")
    print("💡 Chạy `--queries` để xem danh sách search queries gợi ý.")
    print("💡 Chạy `--sources` để xem danh sách nguồn ưu tiên.\n")


if __name__ == "__main__":
    main()
