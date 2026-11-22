"""Simulación de 12 operaciones (válidas e inválidas) del sistema Software FJ."""
from excepciones import ErrorSistema
from gestor import GestorSistema
from registro import log
from servicios import AlquilerEquipo, AsesoriaEspecializada, SalaReserva


def main() -> None:
    log.info("===== INICIO DE SIMULACIÓN =====")
    g = GestorSistema()

    print("\n1. Cliente válido")
    ana = g.registrar_cliente("C001", "ana gómez", "ana@correo.com", "3101234567")
    print("2. Cliente con correo inválido")
    g.registrar_cliente("C002", "Luis Pérez", "luis-correo", "3109876543")
    print("2. Cliente con correo inválido")
    g.registrar_cliente("C002", "SEBASTIAN Pérez", "correo-papas", "3109876543")
    print("3. Cliente con nombre vacío (parámetro faltante)")
    g.registrar_cliente("C003", "", "x@correo.com", "3100000000")
    print("4. Cliente con parámetros incompletos (TypeError controlado)")
    g.registrar_cliente("C004", "Sofía Ríos")
    print("5. Segundo cliente válido")
    carlos = g.registrar_cliente("C005", "Carlos Díaz", "carlos@correo.com", "3201112233")

    print("6. Servicios válidos (sala, equipo, asesoría)")
    sala = g.crear_servicio(SalaReserva, "S01", "Sala Norte", 50000, 10)
    equipo = g.crear_servicio(AlquilerEquipo, "S02", "Portátil", 12000, 5)
    asesoria = g.crear_servicio(AsesoriaEspecializada, "S03", "Asesoría Cloud", 90000, "Cloud")
    print("7. Servicio con tarifa negativa")
    g.crear_servicio(SalaReserva, "S04", "Sala Sur", -100, 8)

    print("8. Reserva exitosa de sala")
    g.crear_reserva("R001", ana, sala, 3, personas=6)
    print("9. Reserva fallida: excede la capacidad")
    g.crear_reserva("R002", ana, sala, 2, personas=40)
    print("10. Reserva fallida: servicio no disponible")
    equipo.disponible = False
    g.crear_reserva("R003", carlos, equipo, 4, cantidad=2)
    equipo.disponible = True
    print("11. Reserva de asesoría senior (con recargo)")
    g.crear_reserva("R004", carlos, asesoria, 2, senior=True)
    print("12. Cancelar dos veces (operación no permitida)")
    r = g.crear_reserva("R005", ana, equipo, 3, cantidad=1)
    try:
        r.cancelar()
        r.cancelar()
    except ErrorSistema as error:
        log.error("Cancelación inválida: %s", error)
        print(f"  [X] {error}")

    print("\nCostos (sobrecarga): sala 2h ->",
          sala.calcular_costo(2), "| con IVA ->", sala.calcular_costo_con_iva(2),
          "| IVA + 10% desc ->", sala.calcular_costo(2, impuesto=0.19, descuento=0.10))
    print(f"\nResumen: {len(g.clientes)} clientes, {len(g.servicios)} servicios, "
          f"{len(g.reservas)} reservas. El sistema siguió funcionando ante todos los errores.")
    log.info("===== FIN DE SIMULACIÓN =====")


if __name__ == "__main__":
    main()
