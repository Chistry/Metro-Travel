import json

# Carga los requisitos de visa desde un archivo JSON
def cargar_visas(archivo_visas="visas.json"):
    try:
        with open(archivo_visas, mode='r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo de datos '{archivo_visas}' no fue encontrado.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo_visas}' no tiene un formato JSON válido.")
        exit()


# Carga las tarifas de vuelos desde un archivo JSON
def cargar_tarifas(archivo_tarifas="tarifas.json"):
    tarifas = []
    try:
        with open(archivo_tarifas, mode='r', encoding='utf-8') as f:
            datos = json.load(f)
            for vuelo in datos:
                if 'origen' in vuelo and 'destino' in vuelo and 'precio' in vuelo:
                    tarifas.append((vuelo['origen'], vuelo['destino'], float(vuelo['precio'])))
                else:
                    print(f"Advertencia: Ignorando entrada de tarifa inválida: {vuelo}")
    except FileNotFoundError:
        print(f"Error: El archivo de datos '{archivo_tarifas}' no fue encontrado.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo_tarifas}' no tiene un formato JSON válido.")
        exit()
    return tarifas


