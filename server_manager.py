import threading
import uvicorn
from PyQt5.QtCore import QObject, pyqtSignal
import logging
from logging import StreamHandler, Formatter
import io
import contextlib
import time

class UvicornLogger(StreamHandler):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def emit(self, record):
        log_entry = self.format(record)
        self.signal.emit(log_entry)

class ServerManager(QObject):
    update = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.server_thread = None
        self.running = False

    def start_server(self):
        self.running = True
        self.update.emit("Starting server...")
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        # 设置日志记录器
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # 捕获所有级别的日志消息

        handler = UvicornLogger(self.update)
        handler.setLevel(logging.DEBUG)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        log_capture_string = io.StringIO()
        with contextlib.redirect_stdout(log_capture_string):
            with contextlib.redirect_stderr(log_capture_string):
                config = uvicorn.Config("api:app", host="0.0.0.0", port=23456, workers=1, log_level="debug")
                self.server = uvicorn.Server(config)

                self.update.emit("Server started")
                try:
                    while not self.server.should_exit:
                        time.sleep(0.1)
                        logs = log_capture_string.getvalue()
                        if logs:
                            self.update.emit(logs)
                            log_capture_string.truncate(0)
                            log_capture_string.seek(0)
                        self.server.run()
                except Exception as e:
                    self.update.emit(str(e))
                finally:
                    logs = log_capture_string.getvalue()
                    self.update.emit(logs)
                    log_capture_string.close()
                    logger.removeHandler(handler)

    def stop_server(self):
        if self.running:
            self.update.emit("Stopping server...")
            self.server.should_exit = True  # 通知Uvicorn服务器停止
            self.server_thread.join()  # 等待服务器线程结束
            self.update.emit("Server stopped")
            self.running = False

