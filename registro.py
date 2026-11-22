"""Configuración del archivo de logs (único uso de archivos del sistema)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "sistema.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, creando la carpeta/archivo si hace falta."""
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # crea la carpeta logs/
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar handlers si se llama varias veces
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        logger.addHandler(manejador)
    return logger


log = obtener_logger()
