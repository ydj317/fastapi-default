# app/core/logging.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 로그 디렉토리 생성 (app과 같은 위치)
log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "server.log"

# 로그 포맷
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 파일 핸들러 (10MB 이상이면 회전, 최대 10개 보관)
file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# 루트 로거 설정
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.handlers = []  # 중복 방지
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Uvicorn 관련 로거도 동일 핸들러 적용
for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
    uv_logger = logging.getLogger(name)
    uv_logger.handlers = root_logger.handlers
    uv_logger.setLevel(logging.INFO)

# 공통 logger 객체
logger = logging.getLogger("app")
