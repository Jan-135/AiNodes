import logging

logger = logging.getLogger("AINodes")
logger.setLevel(logging.DEBUG)

# Optional: Nur für Debug-Zwecke auf der Konsole
if not logger.handlers:
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
