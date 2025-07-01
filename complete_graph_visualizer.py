import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
import math
import json

class CompleteGraphVisualizer:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Vista Completa de Todas las Rutas")
        self.window.geometry("1200x800")  # Ventana más grande
        
        # Frame principal
        main_frame = Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para información
        info_frame = Frame(main_frame, bg="lightgray", height=100)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Canvas para dibujar con scrollbars
        canvas_frame = Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = Scrollbar(canvas_frame, orient="vertical")
        h_scrollbar = Scrollbar(canvas_frame, orient="horizontal")
        
        # Canvas
        self.canvas = Canvas(canvas_frame, width=1100, height=650, bg="white",  # Canvas más grande
                           yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Cargar todas las tarifas directamente
        self.tarifas = self._cargar_tarifas_completas()
        self.grafo_completo = self._construir_grafo_completo()
        self.posiciones = {}
        
        # Estadísticas
        self.stats_label = tk.Label(info_frame, text="", justify=tk.LEFT, 
                                   font=("Arial", 10), bg="lightgray")
        self.stats_label.pack(padx=10, pady=5)
        
        # Botón para cerrar
        tk.Button(info_frame, text="Cerrar", command=self.window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # Calcular y mostrar estadísticas
        self._calcular_estadisticas()
        
        # Dibujar el grafo
        self._calcular_posiciones()
        self._dibujar_grafo_completo()
        
        # Configurar área de scroll
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def _cargar_tarifas_completas(self):
        """Carga directamente el archivo tarifas.json"""
        try:
            with open("tarifas.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _construir_grafo_completo(self):
        """Construye el grafo con TODAS las conexiones del archivo"""
        grafo = {}
        
        # Primero, identificar todos los aeropuertos
        aeropuertos = set()
        for tarifa in self.tarifas:
            aeropuertos.add(tarifa['origen'])
            aeropuertos.add(tarifa['destino'])
        
        # Inicializar el grafo
        for aeropuerto in aeropuertos:
            grafo[aeropuerto] = []
        
        # Agregar todas las conexiones (bidireccionales)
        for tarifa in self.tarifas:
            origen = tarifa['origen']
            destino = tarifa['destino']
            precio = tarifa['precio']
            
            # Agregar conexión de ida
            grafo[origen].append((destino, precio))
            # Agregar conexión de vuelta
            grafo[destino].append((origen, precio))
        
        return grafo
    
    def _calcular_estadisticas(self):
        """Calcula y muestra estadísticas del grafo"""
        num_aeropuertos = len(self.grafo_completo)
        num_rutas = len(self.tarifas)
        
        # Calcular conexiones por aeropuerto
        conexiones_por_aeropuerto = {}
        for aeropuerto, conexiones in self.grafo_completo.items():
            # Dividir por 2 porque cada ruta se cuenta dos veces (ida y vuelta)
            conexiones_directas = len(set(destino for destino, _ in conexiones))
            conexiones_por_aeropuerto[aeropuerto] = conexiones_directas
        
        # Aeropuerto con más conexiones
        max_conexiones = max(conexiones_por_aeropuerto.items(), key=lambda x: x[1])
        min_conexiones = min(conexiones_por_aeropuerto.items(), key=lambda x: x[1])
        
        stats_text = f"""Estadísticas del Grafo Completo:
• Total de aeropuertos: {num_aeropuertos}
• Total de rutas directas: {num_rutas}
• Aeropuerto con más conexiones: {max_conexiones[0]} ({max_conexiones[1]} conexiones)
• Aeropuerto con menos conexiones: {min_conexiones[0]} ({min_conexiones[1]} conexiones)"""
        
        self.stats_label.config(text=stats_text)
        
        # Guardar para mostrar en los nodos
        self.conexiones_por_aeropuerto = conexiones_por_aeropuerto
    
    def _calcular_posiciones(self):
        """Calcula las posiciones usando un layout mejorado"""
        nodos = list(self.grafo_completo.keys())
        num_nodos = len(nodos)
        
        if num_nodos == 0:
            return
        
        # Ordenar nodos por número de conexiones (los más conectados en el centro)
        nodos_ordenados = sorted(nodos, 
                                key=lambda x: self.conexiones_por_aeropuerto[x], 
                                reverse=True)
        
        # Layout en espiral para mejor distribución con MÁS ESPACIO
        centro_x, centro_y = 600, 400  # Centro ajustado para canvas más grande
        angulo = 0
        radio_base = 100  # Radio inicial más grande
        incremento_radio = 80  # Mayor incremento entre niveles
        
        for i, nodo in enumerate(nodos_ordenados):
            if i == 0:
                # El más conectado en el centro
                self.posiciones[nodo] = (centro_x, centro_y)
            else:
                # Los demás en espiral con más separación
                nivel = int((i - 1) / 6) + 1
                radio = radio_base + (nivel * incremento_radio)
                # Más separación angular
                angulo = (2 * math.pi * (i - 1)) / min(6 * nivel, num_nodos - 1)
                
                x = centro_x + radio * math.cos(angulo)
                y = centro_y + radio * math.sin(angulo)
                self.posiciones[nodo] = (x, y)
    
    def _dibujar_grafo_completo(self):
        """Dibuja el grafo completo con todas las rutas"""
        # Primero dibujar todas las aristas
        self._dibujar_todas_las_aristas()
        
        # Luego dibujar los nodos con información adicional
        self._dibujar_nodos_con_info()
        
        # Leyenda
        self._dibujar_leyenda()
    
    def _dibujar_todas_las_aristas(self):
        """Dibuja TODAS las conexiones del archivo"""
        conexiones_dibujadas = set()
        
        for tarifa in self.tarifas:
            origen = tarifa['origen']
            destino = tarifa['destino']
            precio = tarifa['precio']
            
            if origen not in self.posiciones or destino not in self.posiciones:
                continue
            
            # Crear identificador único para la conexión
            conexion_id = tuple(sorted([origen, destino]))
            if conexion_id not in conexiones_dibujadas:
                conexiones_dibujadas.add(conexion_id)
                
                x1, y1 = self.posiciones[origen]
                x2, y2 = self.posiciones[destino]
                
                # Color según el precio
                if precio < 50:
                    color = "green"
                    width = 2
                elif precio < 100:
                    color = "orange"
                    width = 1.5
                else:
                    color = "red"
                    width = 1
                
                # Dibujar línea
                self.canvas.create_line(x1, y1, x2, y2, 
                                       fill=color, width=width, 
                                       tags="arista")
                
                # Precio en el medio
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Calcular un desplazamiento perpendicular a la línea para evitar superposición
                dx = x2 - x1
                dy = y2 - y1
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # Vector perpendicular normalizado
                    perp_x = -dy / length * 15  # 15 píxeles de desplazamiento
                    perp_y = dx / length * 15
                else:
                    perp_x, perp_y = 0, -15
                
                # Crear un rectángulo blanco de fondo para el texto
                text_id = self.canvas.create_text(mid_x + perp_x, mid_y + perp_y,
                                      text=f"${precio}", 
                                      font=("Arial", 8, "bold"),
                                      fill="black",
                                      tags="precio")
                
                # Obtener los límites del texto
                bbox = self.canvas.bbox(text_id)
                if bbox:
                    # Crear rectángulo blanco detrás del texto
                    rect_id = self.canvas.create_rectangle(
                        bbox[0]-2, bbox[1]-1, bbox[2]+2, bbox[3]+1,
                        fill="white", outline="white", tags="precio_bg"
                    )
                    # Mover el rectángulo detrás del texto
                    self.canvas.tag_lower(rect_id, text_id)
    
    def _dibujar_nodos_con_info(self):
        """Dibuja los nodos con información de conexiones"""
        for nodo, (x, y) in self.posiciones.items():
            num_conexiones = self.conexiones_por_aeropuerto[nodo]
            
            # Tamaño según número de conexiones
            radio_base = 25
            radio = radio_base + (num_conexiones * 2)
            radio = min(radio, 50)  # Límite máximo
            
            # Color según número de conexiones
            if num_conexiones >= 6:
                color = "darkred"
                text_color = "white"
            elif num_conexiones >= 4:
                color = "orange"
                text_color = "black"
            elif num_conexiones >= 2:
                color = "yellow"
                text_color = "black"
            else:
                color = "lightgreen"
                text_color = "black"
            
            # Dibujar círculo
            self.canvas.create_oval(x - radio, y - radio, 
                                   x + radio, y + radio,
                                   fill=color, outline="black", 
                                   width=2, tags="nodo")
            
            # Nombre del aeropuerto
            self.canvas.create_text(x, y - 5, text=nodo, 
                                   font=("Arial", 11, "bold"),
                                   fill=text_color, tags="etiqueta")
            
            # Número de conexiones
            self.canvas.create_text(x, y + 10, 
                                   text=f"({num_conexiones})", 
                                   font=("Arial", 9),
                                   fill=text_color, tags="conexiones")
    
    def _dibujar_leyenda(self):
        """Dibuja una leyenda explicativa"""
        x_leyenda = 20
        y_leyenda = 20
        
        self.canvas.create_text(x_leyenda, y_leyenda, 
                               text="Leyenda:", 
                               font=("Arial", 12, "bold"),
                               anchor="w")
        
        # Colores de líneas
        y_leyenda += 25
        self.canvas.create_line(x_leyenda, y_leyenda, x_leyenda + 30, y_leyenda,
                               fill="green", width=2)
        self.canvas.create_text(x_leyenda + 35, y_leyenda, 
                               text="< $50", anchor="w", font=("Arial", 9))
        
        y_leyenda += 20
        self.canvas.create_line(x_leyenda, y_leyenda, x_leyenda + 30, y_leyenda,
                               fill="orange", width=1.5)
        self.canvas.create_text(x_leyenda + 35, y_leyenda, 
                               text="$50-$99", anchor="w", font=("Arial", 9))
        
        y_leyenda += 20
        self.canvas.create_line(x_leyenda, y_leyenda, x_leyenda + 30, y_leyenda,
                               fill="red", width=1)
        self.canvas.create_text(x_leyenda + 35, y_leyenda, 
                               text="≥ $100", anchor="w", font=("Arial", 9))
        
        # Tamaño de nodos
        y_leyenda += 30
        self.canvas.create_text(x_leyenda, y_leyenda, 
                               text="Tamaño = # conexiones", 
                               anchor="w", font=("Arial", 9, "italic")) 