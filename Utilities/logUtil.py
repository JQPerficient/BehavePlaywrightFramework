import logging
import os
import time


class Logger:
    """
    LOGGER
    """
    def __init__(self, file_level=logging.INFO, log_file_path=None):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        os.makedirs("Logs", exist_ok=True)

        # ✅ Si no nos pasan ruta, la creamos (fallback)
        if not log_file_path:
            run_id = time.strftime("%Y%m%d_%H%M%S")
            log_file_path = os.path.join("Logs", f"run_{run_id}.log")

        formatter = logging.Formatter(
            "%(asctime)s - [Feature: %(feature)s] - [Scenario: %(scenario)s] - "
            "%(filename)s:[%(lineno)d] - [%(levelname)s] - %(message)s"
        )

        handler = logging.FileHandler(log_file_path, mode="w")
        handler.setLevel(file_level)
        handler.setFormatter(formatter)

        # ✅ Evitar duplicación
        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            self.logger.addHandler(handler)

        # ✅ Guardamos la ruta para email
        self.log_file_path = log_file_path
