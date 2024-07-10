import heapq
import random
import pygame
import sys

# Configuración de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
GRIS = (192, 192, 192)
AMARILLO = (255, 255, 0)

# Dimensiones de la ventana y el grid
DIMENSION_CELDA = 50
MARGEN = 5

# Cargar imágenes
IMAGEN_INICIO = pygame.image.load('RUTAS_PYTHON/inicio.jpg')
IMAGEN_OBJETIVO = pygame.image.load('RUTAS_PYTHON/fin.jpg')
IMAGEN_OBSTACULO_1 = pygame.image.load('RUTAS_PYTHON/agua.jpg')
IMAGEN_OBSTACULO_2 = pygame.image.load('RUTAS_PYTHON/bosque2-e1539893598295.jpg')
IMAGEN_OBSTACULO_3 = pygame.image.load('RUTAS_PYTHON/muro.jpg')
IMAGEN_RUTA_OPTIMA = pygame.image.load('RUTAS_PYTHON/rutaoptima.jpg')  # Añadir la imagen de la ruta óptima

# Redimensionar imágenes
IMAGEN_INICIO = pygame.transform.scale(IMAGEN_INICIO, (DIMENSION_CELDA, DIMENSION_CELDA))
IMAGEN_OBJETIVO = pygame.transform.scale(IMAGEN_OBJETIVO, (DIMENSION_CELDA, DIMENSION_CELDA))
IMAGEN_OBSTACULO_1 = pygame.transform.scale(IMAGEN_OBSTACULO_1, (DIMENSION_CELDA, DIMENSION_CELDA))
IMAGEN_OBSTACULO_2 = pygame.transform.scale(IMAGEN_OBSTACULO_2, (DIMENSION_CELDA, DIMENSION_CELDA))
IMAGEN_OBSTACULO_3 = pygame.transform.scale(IMAGEN_OBSTACULO_3, (DIMENSION_CELDA, DIMENSION_CELDA))
IMAGEN_RUTA_OPTIMA = pygame.transform.scale(IMAGEN_RUTA_OPTIMA, (DIMENSION_CELDA, DIMENSION_CELDA))  # Redimensionar la imagen de la ruta óptima

class Mapa:
    def __init__(self, tamano=10):
        self.tamano = tamano
        self.mapa = [[0] * tamano for _ in range(tamano)]

    def agregar_obstaculos(self, obstaculos):
        for r, c, tipo in obstaculos:
            if 0 <= r < len(self.mapa) and 0 <= c < len(self.mapa[0]):
                self.mapa[r][c] = tipo

    def agregar_obstaculos_aleatorios(self, num_obstaculos, inicio, objetivo):
        for _ in range(num_obstaculos):
            while True:
                r, c = random.randint(0, len(self.mapa) - 1), random.randint(0, len(self.mapa[0]) - 1)
                tipo = random.choice([1, 2, 3])
                if (r, c) not in {inicio, objetivo} and self.mapa[r][c] == 0:
                    self.mapa[r][c] = tipo
                    break

class AStar:
    def __init__(self, mapa):
        self.mapa = mapa.mapa
        self.costo_terreno = {0: 1, 1: 5, 2: 10, 3: 15}  # Cambiar los costos de movimiento

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def encontrar_ruta(self, inicio, objetivo):
        filas, columnas = len(self.mapa), len(self.mapa[0])
        prioridad = [(0, inicio)]
        came_from = {inicio: None}
        costo_hasta_ahora = {inicio: 0}

        while prioridad:
            _, actual = heapq.heappop(prioridad)

            if actual == objetivo:
                break

            for delta_f, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vecino = (actual[0] + delta_f, actual[1] + delta_c)

                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                    nuevo_costo = costo_hasta_ahora[actual] + self.costo_terreno[self.mapa[vecino[0]][vecino[1]]]
                    if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:
                        costo_hasta_ahora[vecino] = nuevo_costo
                        heapq.heappush(prioridad, (nuevo_costo + self.heuristica(objetivo, vecino), vecino))
                        came_from[vecino] = actual

        actual, ruta = objetivo, []
        while actual:
            ruta.append(actual)
            actual = came_from.get(actual)
        return ruta[::-1]

class Principal:
    def __init__(self):
        pygame.init()
        self.tamano = 10
        self.ventana = pygame.display.set_mode((self.tamano * (DIMENSION_CELDA + MARGEN) + MARGEN, self.tamano * (DIMENSION_CELDA + MARGEN) + MARGEN))
        pygame.display.set_caption("Ruta más corta con A*")
        self.mapa = Mapa(self.tamano)
        self.inicio = None
        self.objetivo = None
        self.obstaculos_usuario = []
        self.tipo_obstaculo = 1  # 1: muro, 2: agua, 3: tierra
        self.mapa.agregar_obstaculos_aleatorios(10, self.inicio, self.objetivo)

    def main(self):
        seleccionando_obstaculos = True
        seleccionar_inicio = False
        seleccionar_objetivo = False

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    columna = pos[0] // (DIMENSION_CELDA + MARGEN)
                    fila = pos[1] // (DIMENSION_CELDA + MARGEN)
                    if 0 <= fila < self.tamano and 0 <= columna < self.tamano:
                        if seleccionando_obstaculos:
                            if (fila, columna) not in {self.inicio, self.objetivo}:
                                self.obstaculos_usuario.append((fila, columna, self.tipo_obstaculo))
                                self.mapa.agregar_obstaculos([(fila, columna, self.tipo_obstaculo)])
                        elif seleccionar_inicio:
                            self.inicio = (fila, columna)
                            seleccionar_inicio = False
                            seleccionar_objetivo = True
                        elif seleccionar_objetivo:
                            self.objetivo = (fila, columna)
                            seleccionar_objetivo = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.tipo_obstaculo = 1  # Muro
                    elif evento.key == pygame.K_2:
                        self.tipo_obstaculo = 2  # Agua
                    elif evento.key == pygame.K_3:
                        self.tipo_obstaculo = 3  # Tierra
                    elif evento.key == pygame.K_i:
                        seleccionando_obstaculos = False
                        seleccionar_inicio = True
                    elif evento.key == pygame.K_n:
                        seleccionar_objetivo = True

            self.ventana.fill(BLANCO)

            # Dibuja las líneas negras del grid
            for fila in range(self.tamano):
                for columna in range(self.tamano):
                    pygame.draw.rect(self.ventana, NEGRO, [(MARGEN + DIMENSION_CELDA) * columna + MARGEN, (MARGEN + DIMENSION_CELDA) * fila + MARGEN, DIMENSION_CELDA, DIMENSION_CELDA], 1)

            for r, c, tipo in self.obstaculos_usuario:
                if tipo == 1:
                    self.ventana.blit(IMAGEN_OBSTACULO_1, ((MARGEN + DIMENSION_CELDA) * c + MARGEN, (MARGEN + DIMENSION_CELDA) * r + MARGEN))
                elif tipo == 2:
                    self.ventana.blit(IMAGEN_OBSTACULO_2, ((MARGEN + DIMENSION_CELDA) * c + MARGEN, (MARGEN + DIMENSION_CELDA) * r + MARGEN))
                elif tipo == 3:
                    self.ventana.blit(IMAGEN_OBSTACULO_3, ((MARGEN + DIMENSION_CELDA) * c + MARGEN, (MARGEN + DIMENSION_CELDA) * r + MARGEN))

            if self.inicio:
                self.ventana.blit(IMAGEN_INICIO, ((MARGEN + DIMENSION_CELDA) * self.inicio[1] + MARGEN, (MARGEN + DIMENSION_CELDA) * self.inicio[0] + MARGEN))
            if self.objetivo:
                self.ventana.blit(IMAGEN_OBJETIVO, ((MARGEN + DIMENSION_CELDA) * self.objetivo[1] + MARGEN, (MARGEN + DIMENSION_CELDA) * self.objetivo[0] + MARGEN))

            if self.inicio and self.objetivo:
                a_star = AStar(self.mapa)
                ruta = a_star.encontrar_ruta(self.inicio, self.objetivo)
                for r, c in ruta:
                    self.ventana.blit(IMAGEN_RUTA_OPTIMA, ((MARGEN + DIMENSION_CELDA) * c + MARGEN, (MARGEN + DIMENSION_CELDA) * r + MARGEN))

            pygame.display.flip()

if __name__ == "__main__":
    app = Principal()
    app.main()
