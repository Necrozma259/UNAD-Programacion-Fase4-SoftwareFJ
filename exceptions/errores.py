class SoftwareFJError(Exception):
    """Excepción base para todos los errores de negocio del sistema Software FJ."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos de entrada son nulos, negativos o tienen formato incorrecto."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo/stock."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando falla la creación, validación o cálculo de una reserva."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta ejecutar una transición de estado no permitida."""
    pass