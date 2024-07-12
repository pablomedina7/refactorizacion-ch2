import heapq  # colas de prioridad
import pygame  # para escribir juegos
import sys

# Configuración de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


# Dimensiones de la ventana y el grid
DIMENSION_CELDA = 50
MARGEN = 5

# Cargar imágenes
IMAGEN_INICIO = pygame.image.load('refactorizacion-ch2/inicio.jpg')
IMAGEN_OBJETIVO = pygame.image.load('refactorizacion-ch2/fin.jpg')
IMAGEN_OBSTACULO_1 = pygame.image.load('refactorizacion-ch2/agua.jpg')
IMAGEN_OBSTACULO_2 = pygame.image.load('refactorizacion-ch2/bosque2-e1539893598295.jpg')
IMAGEN_OBSTACULO_3 = pygame.image.load('refactorizacion-ch2/muro.jpg')
IMAGEN_RUTA_OPTIMA = pygame.image.load('refactorizacion-ch2/rutaoptima.jpg')  # Añadir la imagen de la ruta óptima

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

class AStar:
    def __init__(self, mapa):
        self.mapa = mapa.mapa
        self.costo_terreno = {0: 1, 1: 5, 2: 10, 3: 15}  # Cambiar los costos de movimiento

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  #calcula la distancia de manhattan entre los puntos a y b 

    def encontrar_ruta(self, inicio, objetivo):
        filas, columnas = len(self.mapa), len(self.mapa[0]) #obtiene el numero de filas y de columnas del mapa 
        prioridad = [(0, inicio)] #inicia la cola de prioridad con los puntos de inicio 
        came_from = {inicio: None} #inicializa un diccionario para rastrear el camino recorrido 
        costo_hasta_ahora = {inicio: 0}     #inicializa un diccionario para rastrear el costo acumulado hasta cada punto 

        while prioridad:            #itera mientras la cola de prioridad no esté vacia 
            _, actual = heapq.heappop(prioridad) #-c

            if actual == objetivo:
                break

            for delta_f, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vecino = (actual[0] + delta_f, actual[1] + delta_c)         #calcula las coordenadas del vecino 

                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:    #verifica que el vecino esté dentro del mapa 
                    nuevo_costo = costo_hasta_ahora[actual] + self.costo_terreno[self.mapa[vecino[0]][vecino[1]]]   #calcula el nuevo C.A sumando el costo acumulado hasta actual 
                    if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:  #comprueba si se ha encontrado un camino mas corto hacia vec
                        costo_hasta_ahora[vecino] = nuevo_costo # actualiza el costo 
                        heapq.heappush(prioridad, (nuevo_costo + self.heuristica(objetivo, vecino), vecino)) #añadir vecino a la cola de prioridad con el nuevo C.A+heuristic to objetivo 
                        came_from[vecino] = actual
#reconstruccion de la ruta optima 
        actual, ruta = objetivo, [] #despues de encontrar el objetivo se reconstruye la ruta optima desde incio hasta objetivo 
        while actual:               
            ruta.append(actual)
            actual = came_from.get(actual)
        return ruta[::-1]

class Principal:
    def __init__(self):
        pygame.init()
        self.tamano = 10
        self.ventana = pygame.display.set_mode((self.tamano * (DIMENSION_CELDA + MARGEN) + MARGEN, self.tamano * (DIMENSION_CELDA + MARGEN) + MARGEN))
        pygame.display.set_caption("Ruta para mostrar a mi kp Marcos")
        self.mapa = Mapa(self.tamano)
        self.inicio = None
        self.objetivo = None
        self.obstaculos_usuario = []
        self.tipo_obstaculo = 1  # 1: muro, 2: agua, 3: tierra

    def main(self):
        seleccionando_obstaculos = True     #inicializa una variable para determinar si se están seleccionando obstaculos 
        seleccionar_inicio = False          #se inicia en false ya que aun no hay valores al inicio de la ejecucion 
        seleccionar_objetivo = False

        while True:
            for evento in pygame.event.get(): #se obtienen los parametros como clics y las teclas 
                if evento.type == pygame.QUIT:      #Si el usuario cierra la ventana se acaba el juego 
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN: #presion de un boton del raton 
                    pos = pygame.mouse.get_pos()    #se obtiene la posicion actual del raton en la ventana del juego 
                    columna = pos[0] // (DIMENSION_CELDA + MARGEN)      
                    fila = pos[1] // (DIMENSION_CELDA + MARGEN)
                    if 0 <= fila < self.tamano and 0 <= columna < self.tamano: #verifica que el clic esté dentro de los limites 
                        if seleccionando_obstaculos:        
                            if (fila, columna) not in {self.inicio, self.objetivo}:
                                self.obstaculos_usuario.append((fila, columna, self.tipo_obstaculo))
                                self.mapa.mapa[fila][columna] = self.tipo_obstaculo #se actualiza el mapa con la seleccion del usuario 
                        elif seleccionar_inicio:        #en el caso de que el usuario no esté seleccionando obstaculos 
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
            #blit= dibujo de la imagen 
            #se muestra el inicio y fin 
            if self.inicio:
                self.ventana.blit(IMAGEN_INICIO, ((MARGEN + DIMENSION_CELDA) * self.inicio[1] + MARGEN, (MARGEN + DIMENSION_CELDA) * self.inicio[0] + MARGEN))
            if self.objetivo:
                self.ventana.blit(IMAGEN_OBJETIVO, ((MARGEN + DIMENSION_CELDA) * self.objetivo[1] + MARGEN, (MARGEN + DIMENSION_CELDA) * self.objetivo[0] + MARGEN))

            if self.inicio and self.objetivo:
                a_star = AStar(self.mapa)
                ruta = a_star.encontrar_ruta(self.inicio, self.objetivo)    #se calcula la ruta optima utilizando el algoritmo a star 
                for r, c in ruta:       #itera sobre cada posición en la ruta optima 
                    self.ventana.blit(IMAGEN_RUTA_OPTIMA, ((MARGEN + DIMENSION_CELDA) * c + MARGEN, (MARGEN + DIMENSION_CELDA) * r + MARGEN)) #se dibuja 
                    #la ruta optima 
            pygame.display.flip() #actualiza la pantalla con todos los elementos dibujados y visibles 
#verificacion y ejecucion final del juego 
if __name__ == "__main__":
    app = Principal() #se utiliza app para encapsular toda la funcionalidad solo cuando se esté en la ventana de python 
    app.main()
