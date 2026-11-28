from models.base import EntidadSistema
from exceptions.errores import DatosInvalidosError


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        try:
            super().__init__(id_cliente)
        except ValueError as e:
            raise DatosInvalidosError("ID de cliente inválido.") from e

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.validar()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"Formato de correo inválido: '{valor}'.")
        self.__correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self.__telefono

    def validar(self) -> bool:
        if not self.__nombre or len(self.__nombre.strip()) < 3:
            raise DatosInvalidosError(f"Nombre inválido para el cliente {self._id}.")
        if not self.__correo or "@" not in self.__correo or "." not in self.__correo.split("@")[-1]:
            raise DatosInvalidosError(f"Correo inválido ('{self.__correo}') para el cliente {self._id}.")
        if not self.__telefono or not str(self.__telefono).isdigit() or len(str(self.__telefono)) < 7:
            raise DatosInvalidosError(f"Teléfono inválido ('{self.__telefono}') para el cliente {self._id}.")
        return True

    def obtener_resumen(self) -> str:
        return f"Cliente [{self._id}] - {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"