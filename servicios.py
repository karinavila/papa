"""Servicio (clase abstracta) y tres servicios especializados."""
from abc import abstractmethod

from entidades import Entidad
from excepciones import (
    CalculoInconsistenteError,
    ErrorValidacion,
    ParametroFaltanteError,
)

IVA = 0.19  # impuesto por defecto


class Servicio(Entidad):
    """Clase abstracta: define el contrato que todo servicio debe cumplir."""

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float):
        super().__init__(identificador)
        if not nombre:
            raise ParametroFaltanteError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ErrorValidacion(f"Tarifa por hora inválida: {tarifa_hora!r}.")
        self._nombre = nombre
        self._tarifa_hora = float(tarifa_hora)
        self.disponible = True  # el gestor puede deshabilitarlo

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def validar_parametros(self, horas: float, **extra) -> None:
        """Valida los parámetros de una reserva para este servicio."""

    @abstractmethod
    def costo_base(self, horas: float, **extra) -> float:
        """Costo sin impuestos ni descuentos (cada servicio lo calcula distinto)."""

    # ---- "Sobrecarga": un mismo método con distintas variantes de parámetros ----
    def calcular_costo(self, horas: float, impuesto: float = 0.0,
                       descuento: float = 0.0, **extra) -> float:
        """Costo total. Admite llamarse solo con horas, con impuesto, con
        descuento o con ambos (parámetros opcionales)."""
        if not 0 <= descuento <= 1 or impuesto < 0:
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango.")
        base = self.costo_base(horas, **extra)
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo calculado es negativo.")
        return round(total, 2)

    def calcular_costo_con_iva(self, horas: float, **extra) -> float:
        """Variante: aplica el IVA por defecto."""
        return self.calcular_costo(horas, impuesto=IVA, **extra)


class SalaReserva(Servicio):
    """Reserva de salas de reunión."""

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float, capacidad: int):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ErrorValidacion("La capacidad debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas: float, **extra) -> None:
        personas = extra.get("personas")
        if personas is None:
            raise ParametroFaltanteError("Falta el número de personas para la sala.")
        if not 0 < horas <= 8:
            raise ErrorValidacion("La sala se reserva entre 1 y 8 horas.")
        if personas > self._capacidad:
            raise ErrorValidacion(f"Excede la capacidad ({self._capacidad}).")

    def costo_base(self, horas: float, **extra) -> float:
        return self._tarifa_hora * horas

    def describir(self) -> str:
        return f"Sala '{self.nombre}' (cap. {self._capacidad}) ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, proyectores...)."""

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float, stock: int):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(stock, int) or stock < 0:
            raise ErrorValidacion("El stock debe ser un entero no negativo.")
        self._stock = stock

    def validar_parametros(self, horas: float, **extra) -> None:
        cantidad = extra.get("cantidad", 1)
        if horas <= 0:
            raise ErrorValidacion("Las horas de alquiler deben ser positivas.")
        if cantidad <= 0 or cantidad > self._stock:
            raise ErrorValidacion(f"Cantidad no válida (stock: {self._stock}).")

    def costo_base(self, horas: float, **extra) -> float:
        return self._tarifa_hora * horas * extra.get("cantidad", 1)

    def describir(self) -> str:
        return f"Equipo '{self.nombre}' (stock {self._stock}) ${self._tarifa_hora:,.0f}/h"


class AsesoriaEspecializada(Servicio):
    """Asesorías con un recargo si el asesor es senior."""

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float, especialidad: str):
        super().__init__(identificador, nombre, tarifa_hora)
        if not especialidad:
            raise ParametroFaltanteError("La asesoría requiere una especialidad.")
        self._especialidad = especialidad

    def validar_parametros(self, horas: float, **extra) -> None:
        if not 0 < horas <= 4:
            raise ErrorValidacion("Una asesoría dura entre 1 y 4 horas.")

    def costo_base(self, horas: float, **extra) -> float:
        recargo = 1.5 if extra.get("senior") else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' en {self._especialidad} ${self._tarifa_hora:,.0f}/h"
