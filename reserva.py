"""Clase Reserva: integra cliente, servicio, duración y estado."""
from cliente import Cliente
from entidades import Entidad
from excepciones import (
    ErrorSistema,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from registro import log
from servicios import Servicio

PENDIENTE, CONFIRMADA, CANCELADA, FALLIDA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "FALLIDA"


class Reserva(Entidad):
    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio,
                 horas: float, **extra):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un cliente y un servicio válidos.")
        self.cliente, self.servicio = cliente, servicio
        self.horas, self.extra = horas, extra
        self.estado = PENDIENTE
        self.costo = None

    def confirmar(self) -> None:
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        if self.estado != PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"'{self.servicio.nombre}' no está disponible.")
        self.estado = CONFIRMADA

    def cancelar(self) -> None:
        """Cancela la reserva (no se permite cancelar dos veces)."""
        if self.estado == CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")
        self.estado = CANCELADA

    def procesar(self) -> float:
        """Valida, calcula el costo y confirma. Usa try/except/else/finally y
        encadenamiento de excepciones (raise ... from ...)."""
        try:
            self.servicio.validar_parametros(self.horas, **self.extra)
            costo = self.servicio.calcular_costo(self.horas, impuesto=0.19, **self.extra)
            self.confirmar()
        except ErrorSistema as error:
            self.estado = FALLIDA
            log.error("Reserva %s falló: %s", self.identificador, error)
            # Encadenamiento: conserva el error original como causa
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva {self.identificador}"
            ) from error
        else:
            # Solo se ejecuta si NO hubo excepción
            self.costo = costo
            log.info("Reserva %s confirmada. Costo: $%s", self.identificador, f"{costo:,.2f}")
            return costo
        finally:
            # Se ejecuta siempre, haya o no error
            log.info("Fin de procesamiento de reserva %s (estado: %s)",
                     self.identificador, self.estado)

    def describir(self) -> str:
        return (f"Reserva[{self.identificador}] {self.cliente.nombre} -> "
                f"{self.servicio.nombre} {self.horas}h [{self.estado}]")
