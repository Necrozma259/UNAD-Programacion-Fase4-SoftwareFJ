from models.cliente import Cliente
from models.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from models.reserva import Reserva
from exceptions.errores import SoftwareFJError
from utils.logger import obtener_logger


class GestorSoftwareFJ:
    """Controlador en memoria para clientes, servicios y reservas de Software FJ."""

    def __init__(self):
        self.clientes = {}
        self.servicios = {}
        self.reservas = {}
        self.logger = obtener_logger("SoftwareFJ")

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        cliente = Cliente(id_cliente, nombre, correo, telefono)
        self.clientes[cliente.id] = cliente
        self.logger.info(f"Cliente registrado: {cliente.obtener_resumen()}")
        return cliente

    def registrar_servicio(self, servicio):
        self.servicios[servicio.id] = servicio
        self.logger.info(f"Servicio registrado: {servicio.obtener_resumen()}")
        return servicio

    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, fecha: str, horas: int):
        cliente = self.clientes.get(id_cliente)
        servicio = self.servicios.get(id_servicio)
        reserva = Reserva(id_reserva, cliente, servicio, fecha, horas)
        self.reservas[reserva.id] = reserva
        self.logger.info(f"Reserva creada: {reserva.obtener_resumen()}")
        return reserva


def ejecutar_simulaciones():
    sistema = GestorSoftwareFJ()
    print("\n" + "=" * 80)
    print("INICIANDO SIMULACIONES DEL SISTEMA INTEGRAL SOFTWARE FJ")
    print("=" * 80 + "\n")

    # 1. Registro exitoso de clientes
    try:
        sistema.registrar_cliente("CLI-001", "Laura Gómez", "laura.gomez@empresa.com", "3104567890")
        sistema.registrar_cliente("CLI-002", "Carlos Mendoza", "cmendoza@tech.co", "3209876543")
        sistema.registrar_cliente("CLI-003", "Sofía Ramírez", "sofia.r@consultora.org", "3151122334")
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 1] Error inesperado: {e}")

    # 2. Error controlado: Registro de cliente con correo y teléfono inválidos
    try:
        sistema.registrar_cliente("CLI-ERR1", "Pedro", "correo_sin_arroba", "123")
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 2 - Excepción Capturada] {type(e).__name__}: {e}")

    # 3. Registro exitoso de servicios polimórficos (Sala, Equipos y Asesoría)
    try:
        sala_juntas = ReservaSala("SRV-101", "Sala Ejecutiva Norte", 50000, capacidad=25, disponible=True)
        sala_mantenimiento = ReservaSala("SRV-102", "Sala Capacitación Sur", 40000, capacidad=15, disponible=False)
        laptops_pro = AlquilerEquipo("SRV-201", "Workstation Dell Precision", 25000, stock_disponible=5, cantidad_solicitada=3)
        asesoria_arq = AsesoriaEspecializada("SRV-301", "Arquitectura Cloud & Python", 80000, nivel_consultor="ARQUITECTO")

        sistema.registrar_servicio(sala_juntas)
        sistema.registrar_servicio(sala_mantenimiento)
        sistema.registrar_servicio(laptops_pro)
        sistema.registrar_servicio(asesoria_arq)
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 3] Error inesperado: {e}")

    # 4. Error controlado: Servicio con tarifa negativa o nivel de consultor inválido
    try:
        AsesoriaEspecializada("SRV-ERR", "Consultoría Express", -15000, nivel_consultor="MASTER")
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 4 - Excepción Capturada] {type(e).__name__}: {e}")

    # 5. Reserva exitosa de Sala con recargo por capacidad (>20 personas) y confirmación
    try:
        res1 = sistema.crear_reserva("RES-001", "CLI-001", "SRV-101", "2026-12-05", 4)
        res1.confirmar()
        sistema.logger.info(f"[Simulación 5] Estado actualizado -> {res1.obtener_resumen()}")
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 5] Error inesperado: {e}")

    # 6. Reserva exitosa de Alquiler de Equipos (3 unidades x 5 horas) y ciclo completo hasta FINALIZADA
    try:
        res2 = sistema.crear_reserva("RES-002", "CLI-002", "SRV-201", "2026-12-06", 5)
        res2.confirmar()
        res2.finalizar()
        sistema.logger.info(f"[Simulación 6] Ciclo completado -> {res2.obtener_resumen()}")
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 6] Error inesperado: {e}")

    # 7. Reserva exitosa de Asesoría Especializada (Nivel Arquitecto, 3 horas) y posterior cancelación
    try:
        res3 = sistema.crear_reserva("RES-003", "CLI-003", "SRV-301", "2026-12-07", 3)
        res3.confirmar()
        res3.cancelar()
        sistema.logger.info(f"[Simulación 7] Reserva cancelada -> {res3.obtener_resumen()}")
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 7] Error inesperado: {e}")

    # 8. Error controlado: Intentar reservar un servicio no disponible (Sala en mantenimiento)
    try:
        sistema.crear_reserva("RES-ERR1", "CLI-001", "SRV-102", "2026-12-08", 2)
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 8 - Excepción Capturada] {type(e).__name__}: {e}")

    # 9. Error controlado: Alquiler de equipos que supera el stock disponible
    try:
        equipos_sin_stock = AlquilerEquipo("SRV-202", "Servidor Rack GPU", 60000, stock_disponible=2, cantidad_solicitada=4)
        sistema.registrar_servicio(equipos_sin_stock)
        sistema.crear_reserva("RES-ERR2", "CLI-002", "SRV-202", "2026-12-09", 3)
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 9 - Excepción Capturada] {type(e).__name__}: {e}")

    # 10. Error controlado: Asesoría especializada con menos del mínimo de 2 horas
    try:
        sistema.crear_reserva("RES-ERR3", "CLI-003", "SRV-301", "2026-12-10", 1)
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 10 - Excepción Capturada] {type(e).__name__}: {e}")

    # 11. Error controlado: Fecha con formato inválido
    try:
        sistema.crear_reserva("RES-ERR4", "CLI-001", "SRV-101", "05/12/2026", 2)
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 11 - Excepción Capturada] {type(e).__name__}: {e}")

    # 12. Error controlado: Transición de estado inválida (intentar confirmar una reserva ya cancelada)
    try:
        res3.confirmar()
    except SoftwareFJError as e:
        sistema.logger.error(f"[Simulación 12 - Excepción Capturada] {type(e).__name__}: {e}")

    print("\n" + "=" * 80)
    print(f"RESUMEN FINAL: {len(sistema.clientes)} clientes | {len(sistema.servicios)} servicios | {len(sistema.reservas)} reservas válidas")
    print("Registro detallado guardado en: logs/sistema_fj.log")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    ejecutar_simulaciones()