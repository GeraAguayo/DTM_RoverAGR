import serial.tools.list_ports

def listar_puertos():
    #
    puertos = serial.tools.list_ports.comports()

    if not puertos:
        print("No se encontraron puertos seriales activos.")
        return

    print(f"{'DISPOSITIVO':<20} | {'DESCRIPCION'}")
    print("-" * 50)

    for puerto in puertos:
        print(f"{puerto.device:<20} | {puerto.description}")

if __name__ == "__main__":
    listar_puertos()
