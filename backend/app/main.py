from fastapi import FastAPI

app = FastAPI(title="就活サポートAPI")


@app.get("/")
def read_root():
    return {"message": "Hello, 就活サポート!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}