"""Clase Cliente con validaciones y encapsulación de datos personales."""
import re

from entidades import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError

# Expresión regular sencilla para validar correos
_PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Los datos son privados y se validan al asignarse."""

    def __init__(self, identificador: str, nombre: str, email: str, telefono: str):
        super().__init__(identificador)
        # Se asigna mediante los setters para que se ejecuten las validaciones
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3 or any(c.isdigit() for c in valor):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'.")
        self.__nombre = valor.strip().title()

    # ---- email ----
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        if not valor:
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        if not _PATRON_EMAIL.match(valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self.__email = valor.lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor:
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        if not (str(valor).isdigit() and len(str(valor)) == 10):
            raise ClienteInvalidoError(f"Teléfono inválido (deben ser 10 dígitos): '{valor}'.")
        self.__telefono = str(valor)

    def describir(self) -> str:
        return f"Cliente[{self.identificador}] {self.nombre} <{self.email}>"
