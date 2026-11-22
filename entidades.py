"""Clase abstracta base para las entidades del sistema."""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Representa cualquier entidad general (cliente, servicio, reserva)."""

    def __init__(self, identificador: str):
        # Atributo "protegido": se accede mediante la propiedad de solo lectura
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        """Identificador único de la entidad (solo lectura)."""
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad concreta debe describirse a sí misma."""

    def __str__(self) -> str:
        return self.describir()
