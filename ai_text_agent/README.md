# Text-only AI Agent (Python + FastAPI)

## Run locally
1. Install Python 3.11 (or 3.10+).
2. Create a virtual environment:
   - Windows: `python -m venv .venv` and `.\.venv\Scripts\activate`
   - macOS/Linux: `python -m venv .venv` and `source .venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Start server: `uvicorn app.server:app --host 0.0.0.0 --port 8080`
5. Open docs: http://localhost:8080/docs

## Test with curl
```bash
curl -X POST http://localhost:8080/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test-1","userMessage":"Help me plan a small automation"}'