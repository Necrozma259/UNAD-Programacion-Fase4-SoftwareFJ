from abc import ABC, abstractmethod


class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad gestionada en Software FJ."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise ValueError("El identificador de la entidad no puede estar vacío.")
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def validar(self) -> bool:
        """Valida las reglas de negocio e integridad de los atributos de la entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Devuelve una representación legible de la entidad."""
        pass