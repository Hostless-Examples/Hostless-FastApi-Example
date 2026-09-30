import json

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from opentelemetry import trace

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/health")
def health():
    # Emit the canonical identifiers consumed by Hostless exact log correlation.
    span_context = trace.get_current_span().get_span_context()
    print(json.dumps({
        "level": "info",
        "message": "health request handled",
        "trace_id": trace.format_trace_id(span_context.trace_id),
        "span_id": trace.format_span_id(span_context.span_id),
    }), flush=True)
    return {"status": "ok", "runtime": "python"}
