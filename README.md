# PairCode — Real-Time Collaborative Code Editor

FastAPI WebSocket backend with browser editor, shared rooms, collaborator count, invite links, and Docker support.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://localhost:8000 in two browser windows and join the same room.

## Docker
```bash
docker compose up --build
```
Open http://localhost:8000.

## Limitations
This portfolio MVP syncs full-document snapshots with last-write-wins behavior, so concurrent edits can overwrite each other. It has no CRDT/operational-transform conflict resolution, authentication, code execution, syntax highlighting, or durable persistence. Next steps: Yjs/CRDT, Redis, PostgreSQL, and authenticated rooms.

## Resume bullet (after testing)
Built a browser-based collaborative code editor using FastAPI WebSockets and JavaScript, enabling room-based live code synchronization and collaborator presence; containerized it with Docker Compose.
