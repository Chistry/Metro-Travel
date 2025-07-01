# Documentación del Visualizador de Grafos - Metro Travel

## 📋 Índice

1. [Introducción](#introducción)
2. [Arquitectura General](#arquitectura-general)
3. [GraphVisualizer - Visualizador Base](#graphvisualizer)
4. [CompleteGraphVisualizer - Visualizador Completo](#completegraphvisualizer)
5. [Algoritmos y Técnicas](#algoritmos-y-técnicas)
6. [Guía de Uso](#guía-de-uso)

---

## 🎯 Introducción

El sistema de visualización de grafos de Metro Travel permite representar gráficamente las conexiones entre aeropuertos, mostrando rutas, precios y estadísticas de manera visual e interactiva.

### Características principales:

- Visualización de redes de aeropuertos
- Representación de rutas y precios
- Resaltado de rutas óptimas
- Estadísticas de conexiones
- Interfaz interactiva con Tkinter

---

## 🏗️ Arquitectura General

El sistema consta de dos visualizadores principales:

```
┌─────────────────────────────────────┐
│         main.py                     │
│  (Interfaz principal)               │
└──────────┬──────────────────────────┘
           │
           ├─────────────────┐
           │                 │
     ┌─────▼─────┐    ┌──────▼──────┐
     │ GraphVis. │    │ CompleteVis.│
     │ (Básico)  │    │ (Completo)  │
     └───────────┘    └─────────────┘
```

---

## 📊 GraphVisualizer - Visualizador Base

### Propósito

Visualiza el grafo filtrado según las restricciones de visa y resalta rutas específicas.

### Estructura de la clase

```python
class GraphVisualizer:
    def __init__(self, parent, grafo, ruta_resaltada=None):
        # parent: ventana padre de Tkinter
        # grafo: diccionario {aeropuerto: [(destino, precio), ...]}
        # ruta_resaltada: lista de aeropuertos en la ruta óptima
```

### Componentes principales:

#### 1. **Inicialización y configuración**

```python
self.window = tk.Toplevel(parent)  # Ventana secundaria
self.canvas = Canvas(...)          # Lienzo para dibujar
self.grafo = grafo                 # Estructura del grafo
self.ruta_resaltada = ruta_resaltada  # Ruta a destacar
self.posiciones = {}               # Coordenadas de cada nodo
```

#### 2. **Cálculo de posiciones (`_calcular_posiciones`)**

Distribuye los nodos en un layout circular:

```python
# Algoritmo:
1. Obtener lista de nodos
2. Calcular centro del canvas (400, 300)
3. Calcular radio según número de nodos
4. Para cada nodo:
   - Calcular ángulo = 2π * índice / total_nodos
   - x = centro_x + radio * cos(ángulo)
   - y = centro_y + radio * sin(ángulo)
```

**Visualización del algoritmo:**

```
        Nodo2
         ↑
    Nodo1 ← Centro → Nodo3
         ↓
        Nodo4
```

#### 3. **Dibujado del grafo (`_dibujar_grafo`)**

Orden de dibujado (importante para las capas):

1. Aristas (conexiones)
2. Nodos (aeropuertos)
3. Ruta resaltada (si existe)

#### 4. **Dibujado de aristas (`_dibujar_aristas`)**

```python
# Para cada conexión:
1. Evitar duplicados (A→B es igual a B→A)
2. Dibujar línea gris entre nodos
3. Mostrar precio en el punto medio
```

#### 5. **Dibujado de nodos (`_dibujar_nodos`)**

Sistema de colores:

- **Azul claro**: Nodos normales
- **Rojo**: Nodos en la ruta resaltada
- Radio fijo: 25 píxeles

#### 6. **Resaltado de ruta (`_resaltar_ruta`)**

Si hay una ruta óptima:

- Líneas rojas gruesas con flechas
- Numeración de pasos
- Dirección del viaje

---

## 🌐 CompleteGraphVisualizer - Visualizador Completo

### Propósito

Muestra TODAS las rutas del archivo `tarifas.json` sin filtros, con estadísticas y análisis visual.

### Características adicionales:

#### 1. **Carga directa de datos**

```python
def _cargar_tarifas_completas(self):
    # Lee directamente tarifas.json
    # No aplica filtros de visa
```

#### 2. **Construcción del grafo completo**

```python
def _construir_grafo_completo(self):
    # Crea grafo bidireccional
    # Incluye TODOS los aeropuertos
```

#### 3. **Layout en espiral mejorado**

```python
# Algoritmo de posicionamiento:
1. Ordenar nodos por número de conexiones (mayor a menor)
2. Nodo más conectado → centro
3. Resto en espiral:
   - Nivel 1: 6 nodos alrededor
   - Nivel 2: 12 nodos
   - Radio aumenta con cada nivel
```

**Visualización:**

```
       ○ ○ ○
     ○   ○   ○     Nivel 2
   ○   ● ● ●   ○
 ○   ● ◉ ●   ○   Nivel 1
   ○   ● ● ●   ○   Centro
     ○   ○   ○
       ○ ○ ○
```

#### 4. **Sistema de colores dinámico**

**Para nodos:**
| Conexiones | Color | Significado |
|------------|-------|-------------|
| 6+ | Rojo oscuro | Hub principal |
| 4-5 | Naranja | Hub secundario |
| 2-3 | Amarillo | Conexión media |
| 1 | Verde claro | Conexión mínima |

**Para aristas:**
| Precio | Color | Grosor |
|--------|-------|--------|
| < $50 | Verde | 2px |
| $50-99 | Naranja | 1.5px |
| ≥ $100 | Rojo | 1px |

#### 5. **Tamaño dinámico de nodos**

```python
radio = 25 + (num_conexiones * 2)  # Mínimo 25px
radio = min(radio, 50)              # Máximo 50px
```

#### 6. **Estadísticas en tiempo real**

- Total de aeropuertos
- Total de rutas directas
- Aeropuerto más/menos conectado
- Número de conexiones por nodo

---

## 🔧 Algoritmos y Técnicas

### 1. **Prevención de duplicados en aristas**

```python
conexion = tuple(sorted([origen, destino]))
if conexion not in conexiones_dibujadas:
    conexiones_dibujadas.add(conexion)
    # Dibujar...
```

### 2. **Cálculo de desplazamiento perpendicular**

Para evitar que los precios se superpongan con las líneas:

```python
# Vector de la línea
dx = x2 - x1
dy = y2 - y1
# Vector perpendicular normalizado
perp_x = -dy / length * 15
perp_y = dx / length * 15
```

### 3. **Fondo blanco para textos**

```python
# 1. Crear texto
text_id = canvas.create_text(...)
# 2. Obtener límites
bbox = canvas.bbox(text_id)
# 3. Crear rectángulo blanco
rect_id = canvas.create_rectangle(bbox...)
# 4. Enviar rectángulo atrás
canvas.tag_lower(rect_id, text_id)
```

### 4. **Scrollbars para grafos grandes**

```python
canvas = Canvas(...,
    yscrollcommand=v_scrollbar.set,
    xscrollcommand=h_scrollbar.set)
canvas.config(scrollregion=canvas.bbox("all"))
```

---

## 📖 Guía de Uso

### 1. **Uso básico desde main.py**

```python
# Visualizar grafo con restricciones
grafo = construir_grafo(tarifas, aeropuertos_permitidos)
GraphVisualizer(root, grafo)

# Visualizar con ruta resaltada
costo, escalas, ruta = encontrar_ruta_mas_barata(...)
GraphVisualizer(root, grafo, ruta)

# Visualizar grafo completo
CompleteGraphVisualizer(root)
```

### 2. **Integración con la interfaz**

**Botones disponibles:**

- 🔵 **Ver Grafo Completo**: Muestra conexiones según visa
- 🟠 **Ver Grafo con Ruta**: Activo tras buscar ruta
- 🟣 **Ver TODAS las Rutas**: Grafo completo sin filtros

### 3. **Personalización**

**Modificar colores:**

```python
# En _dibujar_nodos()
color = "lightblue"  # Cambiar color base
outline_color = "darkblue"  # Cambiar borde
```

**Modificar tamaños:**

```python
# En _calcular_posiciones()
radio_base = 100  # Radio inicial
incremento_radio = 80  # Separación entre niveles
```

**Modificar layout:**

```python
# Cambiar de circular a grid, aleatorio, etc.
# Modificar _calcular_posiciones()
```

---

## 🎨 Ejemplos de visualización

### Grafo sin visa (GraphVisualizer)

- Muestra solo aeropuertos sin requisito de visa
- Layout circular simple
- Colores básicos (azul/rojo)

### Grafo con ruta (GraphVisualizer)

- Misma vista que anterior
- Ruta óptima en rojo con flechas
- Pasos numerados

### Grafo completo (CompleteGraphVisualizer)

- Todos los aeropuertos y conexiones
- Layout en espiral por importancia
- Colores según conexiones y precios
- Estadísticas detalladas

---

## 🚀 Extensiones posibles

1. **Animaciones**: Animar el trazado de rutas
2. **Interactividad**: Click en nodos para info detallada
3. **Filtros dinámicos**: Ocultar/mostrar rutas por precio
4. **Exportación**: Guardar como imagen
5. **Zoom**: Acercar/alejar vista
6. **Layouts alternativos**: Force-directed, jerárquico, etc.

---

## 📝 Notas técnicas

- **Canvas de Tkinter**: Coordenadas (0,0) en esquina superior izquierda
- **Tags**: Permiten agrupar y manipular elementos
- **Orden Z**: Elementos dibujados después aparecen encima
- **Performance**: Para grafos muy grandes (>100 nodos), considerar optimizaciones

---

_Documentación creada para el proyecto Metro Travel - Sistema de visualización de rutas aéreas_
