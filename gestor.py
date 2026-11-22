"""Gestor del sistema: administra listas internas de clientes, servicios y reservas."""
from cliente import Cliente
from excepciones import ErrorSistema, ReservaInvalidaError
from registro import log
from reserva import Reserva
from servicios import Servicio


class GestorSistema:
    def __init__(self):
        # Listas internas: no se usa ninguna base de datos
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, *args) -> Cliente | None:
        """Intenta crear un cliente; si falla, registra el error y sigue."""
        try:
            cliente = Cliente(*args)
        except (ErrorSistema, TypeError) as error:
            log.error("Registro de cliente fallido: %s", error)
            print(f"  [X] Cliente no registrado: {error}")
            return None
        else:
            self.clientes.append(cliente)
            log.info("Cliente registrado: %s", cliente.describir())
            print(f"  [OK] {cliente}")
            return cliente

    def crear_servicio(self, clase, *args) -> Servicio | None:
        """Intenta crear un servicio de la clase indicada."""
        try:
            servicio = clase(*args)
        except (ErrorSistema, TypeError) as error:
            log.error("Creación de servicio fallida (%s): %s", clase.__name__, error)
            print(f"  [X] Servicio no creado: {error}")
            return None
        else:
            self.servicios.append(servicio)
            log.info("Servicio creado: %s", servicio.describir())
            print(f"  [OK] {servicio}")
            return servicio

    def crear_reserva(self, identificador, cliente, servicio, horas, **extra) -> Reserva | None:
        """Crea y procesa una reserva; los fallos no detienen el sistema."""
        try:
            reserva = Reserva(identificador, cliente, servicio, horas, **extra)
            self.reservas.append(reserva)
            costo = reserva.procesar()
        except ErrorSistema as error:
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            print(f"  [X] {error}{causa}")
            return None
        else:
            print(f"  [OK] {reserva} | Costo con IVA: ${costo:,.2f}")
            return reserva
