from datetime import datetime
from models.base import EntidadSistema
from models.cliente import Cliente
from models.servicios import Servicio
from exceptions.errores import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
)


class Reserva(EntidadSistema):
    """Gestiona la reserva de un servicio por parte de un cliente mediante composición y control de estados."""

    ESTADOS_VALIDOS = ("CREADA", "CONFIRMADA", "CANCELADA", "FINALIZADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, fecha_reserva: str, horas: int):
        try:
            super().__init__(id_reserva)
        except ValueError as e:
            raise ReservaInvalidaError("ID de reserva inválido.") from e

        self.__cliente = cliente
        self.__servicio = servicio
        self.__fecha_reserva = fecha_reserva
        self.__horas = horas
        self.__estado = "CREADA"
        self.__costo_total = 0.0

        self.validar()
        # Invocación polimórfica al método calcular_costo() según el tipo concreto de Servicio
        self.__costo_total = self.__servicio.calcular_costo(self.__horas)

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def fecha_reserva(self) -> str:
        return self.__fecha_reserva

    @property
    def horas(self) -> int:
        return self.__horas

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    def validar(self) -> bool:
        if not isinstance(self.__cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe estar asociada a una instancia válida de Cliente.")
        if not isinstance(self.__servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe estar asociada a una instancia válida de Servicio.")
        if not isinstance(self.__horas, int) or self.__horas <= 0:
            raise DatosInvalidosError(f"La duración de la reserva ({self.__horas}h) debe ser un entero mayor a 0.")
        try:
            datetime.strptime(self.__fecha_reserva, "%Y-%m-%d")
        except ValueError as e:
            raise DatosInvalidosError(
                f"Formato de fecha inválido ('{self.__fecha_reserva}'). Use AAAA-MM-DD."
            ) from e
        return True

    def confirmar(self):
        if self.__estado != "CREADA":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self._id} porque su estado actual es '{self.__estado}'."
            )
        self.__servicio.verificar_disponibilidad()
        self.__estado = "CONFIRMADA"

    def cancelar(self):
        if self.__estado in ("CANCELADA", "FINALIZADA"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva {self._id} porque ya se encuentra '{self.__estado}'."
            )
        self.__estado = "CANCELADA"

    def finalizar(self):
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden finalizar reservas CONFIRMADAS (estado actual de {self._id}: '{self.__estado}')."
            )
        self.__estado = "FINALIZADA"

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self._id}] | Estado: {self.__estado} | Fecha: {self.__fecha_reserva} ({self.__horas}h) | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | Total: ${self.__costo_total:,.2f}"
        )