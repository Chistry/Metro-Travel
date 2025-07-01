import tkinter as tk
from tkinter import Canvas
import math
import random

class GraphVisualizer:
    """
    Clase para visualizar grafos de conexiones entre aeropuertos.
    Dibuja nodos (aeropuertos) y aristas (rutas) en una ventana Tkinter.
    """
    
    def __init__(self, parent: tk.Tk | tk.Toplevel, grafo: dict, ruta_resaltada: list = None):
        """
        Constructor del visualizador de grafos.
        
        Args:
            parent (tk.Tk | tk.Toplevel): Ventana padre de Tkinter
            grafo (dict): Diccionario con estructura {aeropuerto: [(destino, precio), ...]}
                         Ejemplo: {'CCS': [('AUA', 40), ('CUR', 35)], ...}
            ruta_resaltada (list, optional): Lista de aeropuertos que forman la ruta óptima
                                           Ejemplo: ['CCS', 'AUA', 'SXM', 'SBH']
        """
        # Crear ventana secundaria (Toplevel) que depende de la ventana padre
        self.window = tk.Toplevel(parent)
        self.window.title("Visualización del Grafo de Vuelos")
        self.window.geometry("800x600")  # Tamaño: 800 píxeles ancho x 600 alto
        
        # Canvas: lienzo donde se dibujarán todos los elementos gráficos
        # width/height: dimensiones del área de dibujo
        # bg: color de fondo (blanco)
        self.canvas = Canvas(self.window, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Expandir para llenar toda la ventana
        
        # Almacenar datos del grafo
        self.grafo = grafo  # dict: estructura de nodos y conexiones
        self.ruta_resaltada = ruta_resaltada if ruta_resaltada else []  # list: ruta a destacar
        self.posiciones = {}  # dict: almacenará {nodo: (x, y)} las coordenadas de cada aeropuerto
        
        # Botón para cerrar la ventana
        tk.Button(self.window, text="Cerrar", command=self.window.destroy).pack(pady=5)
        
        # Proceso de dibujado: calcular posiciones y luego dibujar
        self._calcular_posiciones()
        self._dibujar_grafo()
    
    def _calcular_posiciones(self) -> None:
        """
        Calcula las posiciones (x, y) de cada nodo en un layout circular.
        Distribuye los nodos uniformemente alrededor de un círculo.
        
        Returns:
            None: Modifica self.posiciones directamente
        """
        # Obtener lista de todos los nodos (aeropuertos)
        nodos = list(self.grafo.keys())  # list[str]: ['CCS', 'AUA', 'CUR', ...]
        num_nodos = len(nodos)  # int: cantidad total de nodos
        
        # Si no hay nodos, no hay nada que calcular
        if num_nodos == 0:
            return
            
        # Centro del canvas (punto central del círculo)
        centro_x, centro_y = 400, 300  # int, int: coordenadas del centro
        
        # Calcular radio del círculo basado en cantidad de nodos
        # min() asegura que no sea demasiado grande
        # Fórmula: escala el radio según el número de nodos
        radio = min(250, 300 * num_nodos / (num_nodos + 5))  # float: radio en píxeles
        
        # Distribuir nodos en círculo
        for i, nodo in enumerate(nodos):
            # Calcular ángulo para este nodo
            # 2π radianes = círculo completo, dividido entre número de nodos
            angulo = 2 * math.pi * i / num_nodos  # float: ángulo en radianes
            
            # Convertir coordenadas polares a cartesianas
            # x = centro + radio * cos(ángulo)
            # y = centro + radio * sin(ángulo)
            x = centro_x + radio * math.cos(angulo)  # float: coordenada x
            y = centro_y + radio * math.sin(angulo)  # float: coordenada y
            
            # Guardar posición calculada
            self.posiciones[nodo] = (x, y)  # tuple[float, float]
    
    def _dibujar_grafo(self) -> None:
        """
        Orquesta el proceso completo de dibujado del grafo.
        El orden es importante para las capas visuales.
        
        Returns:
            None: Dibuja directamente en el canvas
        """
        # 1. Primero dibujar todas las aristas (líneas de conexión)
        #    Se dibujan primero para que queden detrás de los nodos
        self._dibujar_aristas()
        
        # 2. Luego dibujar los nodos (círculos de aeropuertos)
        #    Se dibujan después para que queden encima de las líneas
        self._dibujar_nodos()
        
        # 3. Si hay una ruta resaltada, redibujarla encima de todo
        #    Para que sea más visible
        if self.ruta_resaltada:
            self._resaltar_ruta()
    
    def _dibujar_aristas(self) -> None:
        """
        Dibuja todas las conexiones (aristas) entre aeropuertos.
        Evita dibujar la misma conexión dos veces (A->B y B->A son la misma).
        
        Returns:
            None: Dibuja líneas y precios en el canvas
        """
        # Set para rastrear conexiones ya dibujadas y evitar duplicados
        conexiones_dibujadas = set()  # set[tuple[str, str]]
        
        # Iterar sobre cada aeropuerto y sus conexiones
        for origen, destinos in self.grafo.items():
            # origen: str (ej: 'CCS')
            # destinos: list[tuple[str, float]] (ej: [('AUA', 40), ('CUR', 35)])
            
            # Verificar que el origen tenga posición calculada
            if origen not in self.posiciones:
                continue
                
            # Obtener coordenadas del aeropuerto origen
            x1, y1 = self.posiciones[origen]  # float, float
            
            # Iterar sobre cada destino conectado
            for destino, precio in destinos:
                # destino: str (ej: 'AUA')
                # precio: float (ej: 40.0)
                
                # Verificar que el destino tenga posición
                if destino not in self.posiciones:
                    continue
                    
                # Crear identificador único para la conexión
                # sorted() asegura que (A,B) y (B,A) generen el mismo ID
                conexion = tuple(sorted([origen, destino]))  # tuple[str, str]
                
                # Si ya dibujamos esta conexión, saltar
                if conexion in conexiones_dibujadas:
                    continue
                    
                # Marcar conexión como dibujada
                conexiones_dibujadas.add(conexion)
                
                # Obtener coordenadas del destino
                x2, y2 = self.posiciones[destino]  # float, float
                
                # Dibujar línea entre origen y destino
                # create_line(x1, y1, x2, y2, opciones...)
                self.canvas.create_line(x1, y1, x2, y2, 
                                       fill="gray",     # color: gris
                                       width=1,         # grosor: 1 píxel
                                       tags="arista")   # etiqueta para agrupar
                
                # Calcular punto medio de la línea para colocar el precio
                mid_x = (x1 + x2) / 2  # float: coordenada x del punto medio
                mid_y = (y1 + y2) / 2  # float: coordenada y del punto medio
                
                # Pequeño desplazamiento para evitar que el texto tape la línea
                offset_x = 10   # int: desplazamiento horizontal en píxeles
                offset_y = -10  # int: desplazamiento vertical en píxeles
                
                # Mostrar precio de la ruta
                self.canvas.create_text(mid_x + offset_x, mid_y + offset_y,
                                      text=f"${precio:.0f}",  # formato: $40
                                      font=("Arial", 8),      # fuente y tamaño
                                      fill="darkgreen",       # color del texto
                                      tags="precio")          # etiqueta
    
    def _dibujar_nodos(self) -> None:
        """
        Dibuja los nodos (aeropuertos) como círculos coloreados.
        Los nodos en la ruta resaltada se dibujan en rojo.
        
        Returns:
            None: Dibuja círculos y etiquetas en el canvas
        """
        # Iterar sobre cada nodo y su posición
        for nodo, (x, y) in self.posiciones.items():
            # nodo: str (ej: 'CCS')
            # x, y: float, float (coordenadas del centro del nodo)
            
            # Determinar colores según si el nodo está en la ruta resaltada
            if nodo in self.ruta_resaltada:
                # Colores para nodos en la ruta óptima
                color = "red"              # str: color de relleno
                outline_color = "darkred"  # str: color del borde
                text_color = "white"       # str: color del texto
            else:
                # Colores para nodos normales
                color = "lightblue"        # str: color de relleno
                outline_color = "darkblue" # str: color del borde
                text_color = "black"       # str: color del texto
            
            # Radio del círculo en píxeles
            radio = 25  # int: tamaño fijo para todos los nodos
            
            # Dibujar círculo (óvalo con mismo ancho y alto)
            # create_oval(x1, y1, x2, y2) donde (x1,y1) es esquina sup-izq
            # y (x2,y2) es esquina inf-der del rectángulo que contiene el óvalo
            self.canvas.create_oval(x - radio, y - radio,   # esquina superior izquierda
                                   x + radio, y + radio,     # esquina inferior derecha
                                   fill=color,               # color de relleno
                                   outline=outline_color,    # color del borde
                                   width=2,                  # grosor del borde
                                   tags="nodo")              # etiqueta
            
            # Dibujar etiqueta del aeropuerto (código IATA)
            self.canvas.create_text(x, y,              # posición central
                                   text=nodo,           # texto: código del aeropuerto
                                   font=("Arial", 10, "bold"),  # fuente, tamaño, estilo
                                   fill=text_color,     # color del texto
                                   tags="etiqueta")     # etiqueta
    
    def _resaltar_ruta(self) -> None:
        """
        Resalta la ruta óptima encontrada dibujando líneas rojas con flechas.
        Numera cada paso de la ruta para mostrar el orden.
        
        Returns:
            None: Dibuja la ruta resaltada sobre el grafo existente
        """
        # Verificar que haya al menos 2 nodos en la ruta (origen y destino)
        if len(self.ruta_resaltada) < 2:
            return
            
        # Dibujar las aristas de la ruta en orden
        for i in range(len(self.ruta_resaltada) - 1):
            # i: int (índice del paso actual)
            
            # Obtener nodos consecutivos en la ruta
            origen = self.ruta_resaltada[i]      # str: aeropuerto actual
            destino = self.ruta_resaltada[i + 1] # str: siguiente aeropuerto
            
            # Verificar que ambos nodos tengan posiciones
            if origen in self.posiciones and destino in self.posiciones:
                # Obtener coordenadas
                x1, y1 = self.posiciones[origen]  # float, float
                x2, y2 = self.posiciones[destino] # float, float
                
                # Dibujar flecha roja para indicar dirección
                self.canvas.create_line(x1, y1, x2, y2, 
                                       fill="red",           # color: rojo
                                       width=3,              # grosor: 3 píxeles
                                       arrow=tk.LAST,        # flecha al final
                                       arrowshape=(16, 20, 6),  # forma de la flecha
                                       tags="ruta_resaltada")   # etiqueta
                
                # Calcular punto medio para número de paso
                mid_x = (x1 + x2) / 2  # float
                mid_y = (y1 + y2) / 2  # float
                
                # Mostrar número de paso en la ruta
                self.canvas.create_text(mid_x - 15, mid_y + 15,  # posición con offset
                                      text=f"Paso {i+1}",         # texto: "Paso 1", "Paso 2", etc.
                                      font=("Arial", 9, "bold"),  # fuente
                                      fill="red",                 # color
                                      tags="paso_ruta")           # etiqueta 