from datetime import datetime
import json
import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from .db import write_events, archive_path
from .rollup import build_daily_report, load_events, resolve_rollup_day
from .schema import NormalizedEvent
from .render.html import render_html
from .render.md import render_markdown
from .render.pdf import render_pdf

app = FastAPI(title="Disinfo Reporter")


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/ingest/huginn")
def ingest_huginn(payload: dict, x_huginn_secret: str = Header(default="")):
    expected = os.environ.get("HUGINN_WEBHOOK_SECRET", "")
    if expected and x_huginn_secret != expected:
        raise HTTPException(status_code=401, detail="Invalid secret")

    event_data = payload.get("event") or payload
    try:
        event = NormalizedEvent(**event_data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    out_path = write_events([event])
    return {"stored": True, "path": out_path}


@app.post("/rollup")
def rollup():
    base = archive_path()
    day = resolve_rollup_day()
    events = load_events(base, day)
    report = build_daily_report(events, day)

    day_dir = os.path.join(base, day)
    os.makedirs(day_dir, exist_ok=True)

    html = render_html(report, template_dir="/app/templates")
    md = render_markdown(report, template_dir="/app/templates")
    pdf = render_pdf(report)

    with open(os.path.join(day_dir, "report.html"), "w", encoding="utf-8") as handle:
        handle.write(html)
    with open(os.path.join(day_dir, "report.md"), "w", encoding="utf-8") as handle:
        handle.write(md)
    with open(os.path.join(day_dir, "report.json"), "w", encoding="utf-8") as handle:
        handle.write(report.model_dump_json())
    with open(os.path.join(day_dir, "report.pdf"), "wb") as handle:
        handle.write(pdf)

    return JSONResponse(content={"day": day, "items": len(report.notable_items)})


@app.get("/report/latest")
def report_latest():
    base = archive_path()
    day = resolve_rollup_day()
    path = os.path.join(base, day, "report.json")
    if not os.path.exists(path):
        return JSONResponse(content={"message": "No report yet"}, status_code=404)
    with open(path, "r", encoding="utf-8") as handle:
        data = json.loads(handle.read())
    return JSONResponse(content=data)
