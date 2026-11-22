"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorSistema, de modo que el programa puede capturar
cualquier error propio con un solo `except ErrorSistema`.
"""


class ErrorSistema(Exception):
    """Excepción base de la aplicación."""


class ErrorValidacion(ErrorSistema):
    """Datos inválidos (formato, rango, tipo incorrecto)."""


class ClienteInvalidoError(ErrorValidacion):
    """Los datos de un cliente no cumplen las reglas."""


class ParametroFaltanteError(ErrorValidacion):
    """Falta un parámetro obligatorio."""


class ServicioNoDisponibleError(ErrorSistema):
    """El servicio solicitado no está disponible."""


class OperacionNoPermitidaError(ErrorSistema):
    """Operación no permitida para el estado actual (p. ej. cancelar dos veces)."""


class ReservaInvalidaError(ErrorSistema):
    """La reserva no pudo crearse o procesarse."""


class CalculoInconsistenteError(ErrorSistema):
    """El cálculo de un costo produjo un valor inconsistente."""
