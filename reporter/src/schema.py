from pydantic import BaseModel, Field
from typing import List, Optional


class NormalizedEvent(BaseModel):
    source: str
    url: str
    title: str
    published_at: str
    text: str
    language: str
    entities: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)
    accounts: List[str] = Field(default_factory=list)
    media_urls: List[str] = Field(default_factory=list)
    signal_score: Optional[float] = None
    signal_label: Optional[str] = None


class ReportItem(BaseModel):
    title: str
    url: str
    source: str
    excerpt: str
    signal_score: float
    rationale: List[str] = Field(default_factory=list)


class DailyReport(BaseModel):
    date: str
    executive_summary: List[str]
    narratives: List[dict]
    notable_items: List[ReportItem]
    network_signals: List[dict]
    recommendations: List[str]
