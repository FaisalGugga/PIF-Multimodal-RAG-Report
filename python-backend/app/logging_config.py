import json
import logging
import sys
from datetime import datetime
from .request_context import request_id_context

from .config import LOG_DIR, LOG_FILE
from logging.handlers import RotatingFileHandler



RESERVED_LOG_RECORD_FIELDS = {
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
    "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread", "threadName",
    "processName", "process", "message", "asctime"
}

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        
        for key, value in record.__dict__.items():
            if key not in RESERVED_LOG_RECORD_FIELDS and not key.startswith("_"):
                try:
                    json.dumps(value)
                    log_data[key] = value
                except TypeError:
                    log_data[key] = str(value)
                    
        request_id = request_id_context.get()
        
        if request_id:
            log_data["request_id"] = request_id
                    
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)
        
            
def setup_logging() -> None:
    
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    
    root_logger.handlers.clear()
    root_logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JsonFormatter())
    
    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JsonFormatter())
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
            


                    
