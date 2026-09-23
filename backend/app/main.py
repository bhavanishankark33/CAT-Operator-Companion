from fastapi import FastAPI

app = FastAPI(title="CAT Operator Companion")

@app.get("/health")
def health():
    return {"status": "ok"}
