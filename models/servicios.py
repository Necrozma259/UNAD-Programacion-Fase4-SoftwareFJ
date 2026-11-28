from abc import abstractmethod
from models.base import EntidadSistema
from exceptions.errores import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(EntidadSistema):
    """Clase abstracta que define el contrato polimórfico para los servicios de Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        try:
            super().__init__(id_servicio)
        except ValueError as e:
            raise DatosInvalidosError("ID de servicio inválido.") from e

        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible
        self.validar()

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    def validar(self) -> bool:
        if not self._nombre or not self._nombre.strip():
            raise DatosInvalidosError(f"El servicio {self._id} debe tener un nombre válido.")
        if self._tarifa_base <= 0:
            raise DatosInvalidosError(f"La tarifa base del servicio {self._id} debe ser mayor a 0.")
        return True

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' ({self._id}) no está disponible actualmente.")

    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        """Calcula el costo del servicio según su lógica especializada."""
        pass


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        self.capacidad = capacidad
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)

    def validar(self) -> bool:
        super().validar()
        if self.capacidad <= 0 or self.capacidad > 100:
            raise DatosInvalidosError(f"Capacidad inválida ({self.capacidad}) para la sala {self._id}.")
        return True

    def calcular_costo(self, horas: int) -> float:
        self.verificar_disponibilidad()
        if horas <= 0:
            raise DatosInvalidosError("Las horas de reserva de sala deben ser mayores a 0.")
        recargo = 1.15 if self.capacidad > 20 else 1.0
        return round(self._tarifa_base * horas * recargo, 2)

    def obtener_resumen(self) -> str:
        return f"Sala [{self._id}]: {self._nombre} (Capacidad: {self.capacidad} pers. | ${self._tarifa_base}/h)"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de hardware y equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, stock_disponible: int, cantidad_solicitada: int = 1):
        self.stock_disponible = stock_disponible
        self.cantidad_solicitada = cantidad_solicitada
        super().__init__(id_servicio, nombre, tarifa_hora, disponible=(stock_disponible > 0))

    def validar(self) -> bool:
        super().validar()
        if self.stock_disponible < 0:
            raise DatosInvalidosError(f"El stock no puede ser negativo en el equipo {self._id}.")
        if self.cantidad_solicitada <= 0:
            raise DatosInvalidosError("La cantidad de equipos a alquilar debe ser al menos 1.")
        return True

    def calcular_costo(self, horas: int) -> float:
        self.verificar_disponibilidad()
        if self.cantidad_solicitada > self.stock_disponible:
            raise ServicioNoDisponibleError(
                f"Stock insuficiente para '{self._nombre}': solicitados {self.cantidad_solicitada}, disponibles {self.stock_disponible}."
            )
        if horas <= 0:
            raise DatosInvalidosError("Las horas de alquiler deben ser mayores a 0.")
        return round(self._tarifa_base * horas * self.cantidad_solicitada, 2)

    def obtener_resumen(self) -> str:
        return f"Equipo [{self._id}]: {self._nombre} (Stock: {self.stock_disponible} | ${self._tarifa_base}/h por unidad)"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o arquitectura de software."""

    NIVELES_VALIDOS = {"JUNIOR": 1.0, "SENIOR": 1.4, "ARQUITECTO": 1.8}

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, nivel_consultor: str, disponible: bool = True):
        self.nivel_consultor = nivel_consultor.upper().strip()
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)

    def validar(self) -> bool:
        super().validar()
        if self.nivel_consultor not in self.NIVELES_VALIDOS:
            raise DatosInvalidosError(
                f"Nivel de consultor '{self.nivel_consultor}' inválido. Use: {list(self.NIVELES_VALIDOS.keys())}"
            )
        return True

    def calcular_costo(self, horas: int) -> float:
        self.verificar_disponibilidad()
        if horas < 2:
            raise DatosInvalidosError("Las asesorías especializadas requieren un mínimo de 2 horas.")
        multiplicador = self.NIVELES_VALIDOS[self.nivel_consultor]
        return round(self._tarifa_base * horas * multiplicador, 2)

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self._id}]: {self._nombre} (Nivel: {self.nivel_consultor} | Base: ${self._tarifa_base}/h)"