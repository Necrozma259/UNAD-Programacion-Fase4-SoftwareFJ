import logging
import os


def obtener_logger(nombre: str = "SoftwareFJ") -> logging.Logger:
    """Configura y retorna el logger que registra eventos y errores en archivo y consola."""
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(nombre)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)-12s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Registro persistente en archivo .log
        file_handler = logging.FileHandler("logs/sistema_fj.log", mode="a", encoding="utf-8")
        file_handler.setFormatter(formato)

        # Salida simultánea en consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger