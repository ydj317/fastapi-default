import os
import uvicorn

# uvicorn app.main:app --port=8081
if __name__ == "__main__":
    # 실행 전 uploads 폴더 생성
    os.makedirs("uploads", exist_ok=True)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        headers=[("Server", "AppServer")],
    )
