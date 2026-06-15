import logging
import json
import os
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path


class JSONFormatter(logging.Formatter):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
 
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self.service_name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)


        standard_keys = {
            "name", "msg", "args", "levelname", "levelno", "pathname",
            "filename", "module", "exc_info", "exc_text", "stack_info",
            "lineno", "funcName", "created", "msecs", "relativeCreated",
            "thread", "threadName", "processName", "process", "message",
            "taskName"
        }
        for key, value in record.__dict__.items():
            if key not in standard_keys:
                log_obj[key] = value
 
        return json.dumps(log_obj, ensure_ascii=False, default=str)



def setup_logger(service_name: str, log_dir: str = "logs") -> logging.Logger:
    
    
    logger = logging.getLogger(service_name)
 
    if logger.handlers:
        return logger
 
    logger.setLevel(logging.DEBUG)
 
    formatter = JSONFormatter(service_name=service_name)
 
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
 
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
 
    file_handler = RotatingFileHandler(
        filename=log_path / f"{service_name}.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
 
    logger.propagate = False
 
    return logger
 
 
def get_logger(service_name: str) -> logging.Logger:
  
    return logging.getLogger(service_name)
 
 

def log_request(logger: logging.Logger, request_id: str, method: str,
                path: str, status_code: int, duration_ms: float,
                user_id: int = None):
  
    level = logging.INFO if status_code < 400 else logging.WARNING
    if status_code >= 500:
        level = logging.ERROR
 
    logger.log(
        level,
        f"{method} {path} → {status_code}",
        extra={
            "request_id": request_id,
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "user_id": user_id,
        }
    )