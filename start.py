import uvicorn

# uvicorn app.main:app --port=8081
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, headers=[("Server", "AppServer")])