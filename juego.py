import pygame
import time
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
# ✅ MODIFICACIÓN: Inicia directamente en pantalla completa
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Juego tipo Mario Bros")

# Cargar el sonido del salto
salto_sonido = pygame.mixer.Sound("audios/salto.mp3")

# Cargar sonido de game over
game_over_sonido = pygame.mixer.Sound("audios/game_over.mp3")

# Cargar música de fondo
pygame.mixer.music.load("audios/fondo_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)

# Función para cargar imágenes
def cargar_imagen(nombre, ancho, alto):
    imagen = pygame.image.load(nombre).convert_alpha()
    return pygame.transform.scale(imagen, (ancho, alto))

# Cargar fondos
fondo1 = cargar_imagen("fondos/fondo1.png", ANCHO, ALTO)
fondo_2 = cargar_imagen("fondos/fondo_2.png", ANCHO, ALTO)
fondo_noche2 = cargar_imagen("fondos/fondo_noche.png", ANCHO, ALTO)
espacio = cargar_imagen("fondos/space.png", ANCHO, ALTO)
fondo = fondo1

# Crear suelo en mosaico
def crear_suelo():
    bloque = pygame.image.load("plataformas/fonfo2.png").convert_alpha()
    bloque = pygame.transform.scale(bloque, (30, 30))
    superficie = pygame.Surface((ANCHO, 30), pygame.SRCALPHA)
    for x in range(0, ANCHO, 30):
        superficie.blit(bloque, (x, 0))
    return superficie

suelo_imagen = crear_suelo()

# Imágenes del jugador
quieto = cargar_imagen("imagenes de mario/m2.png", 40, 50)
corriendo = [
    cargar_imagen("imagenes de mario/cor1.png", 40, 50),
    cargar_imagen("imagenes de mario/cor2.png", 40, 50),
    cargar_imagen("imagenes de mario/co3.png", 40, 50)
]

salto = cargar_imagen("imagenes de mario/salt.png", 40, 50)

ANCHO_PLATAFORMA = 150
ALTO_PLATAFORMA = 30

ALTURA_MAX_SALTO = 90
DISTANCIA_HORIZONTAL_MAX = 200

pinchon_img = cargar_imagen("objetos/pinchon.png", 40, 40)
hongo_img = cargar_imagen("objetos/hongo.png", 40, 40)

fuente = pygame.font.Font(None, 36)

# ==========================
# CLASES
# ==========================
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {"quieto": quieto, "correr": corriendo, "salto": salto}
        self.image = self.images["quieto"]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO - 100
        self.vel_y = 0
        self.suelo = False
        self.direccion = 1
        self.frame_index = 0
        self.contador_animacion = 0
        self.super_salto = False

    def update(self, plataformas):
        keys = pygame.key.get_pressed()
        moviendo = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direccion = -1
            moviendo = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direccion = 1
            moviendo = True

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > ANCHO - self.rect.width:
            self.rect.x = ANCHO - self.rect.width

        if keys[pygame.K_SPACE] and self.suelo:
            if self.super_salto:
                self.vel_y = -22
                self.super_salto = False
            else:
                self.vel_y = -18
            salto_sonido.play()

        self.vel_y += 1
        self.rect.y += self.vel_y

        self.suelo = False
        for plataforma in plataformas:
            if isinstance(plataforma, PlataformaDesvanecible) and plataforma.activa:
                plataforma.verificar_desvanecimiento(self)

            if (
                plataforma.activa
                and self.vel_y > 0
                and self.rect.bottom <= plataforma.rect.top + 20
                and self.rect.right > plataforma.rect.left + 10
                and self.rect.left < plataforma.rect.right - 10
                and self.rect.bottom >= plataforma.rect.top
            ):
                self.rect.bottom = plataforma.rect.top
                self.vel_y = 0
                self.suelo = True

        if not self.suelo:
            self.image = self.images["salto"]
        elif moviendo:
            self.contador_animacion += 1
            if self.contador_animacion > 5:
                self.frame_index = (self.frame_index + 1) % len(self.images["correr"])
                self.contador_animacion = 0
            self.image = self.images["correr"][self.frame_index]
        else:
            self.image = self.images["quieto"]

        if self.direccion == -1:
            self.image = pygame.transform.flip(self.image, True, False)

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, usar_imagen=False):
        super().__init__()
        if usar_imagen:
            self.image = cargar_imagen("plataformas/plata.png", ancho, alto)
        else:
            self.image = suelo_imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.activa = True

class PlataformaDesvanecible(Plataforma):
    def __init__(self, x, y, ancho, alto):
        super().__init__(x, y, ancho, alto)
        self.image = cargar_imagen("plataformas/nube2.png", ancho, alto)
        self.tiempo_activacion = None
        self.activa = True

    def verificar_desvanecimiento(self, jugador):
        if self.rect.colliderect(jugador.rect) and self.activa:
            if self.tiempo_activacion is None:
                self.tiempo_activacion = time.time()
            elif time.time() - self.tiempo_activacion >= 1:
                self.activa = False

class ObjetoCaida(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        if tipo == "pinchon":
            self.image = pinchon_img
        else:
            self.image = hongo_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = random.randint(3, 6)

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.y > ALTO:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.randint(50, ANCHO - 50)

# ==========================
# FUNCIONES
# ==========================
def mostrar_winner():
    global fondo
    pygame.mixer.music.pause()
    
    pantalla.blit(fondo, (0, 0))
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 150, 0, 180)) # Fondo verde semi-transparente
    pantalla.blit(s, (0, 0))

    texto_winner = fuente.render("¡WINNER! ¡HAS GANADO!", True, (255, 255, 0))
    pantalla.blit(texto_winner, (ANCHO // 2 - texto_winner.get_width() // 2, ALTO // 3))

    texto_puntaje_final = fuente.render(f"Puntaje Final: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto_puntaje_final, (ANCHO // 2 - texto_puntaje_final.get_width() // 2, ALTO // 2 + 60))

    # Botones
    boton_reintentar = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50)
    pygame.draw.rect(pantalla, (0, 128, 0), boton_reintentar)
    # ✅ Se utiliza "Volver a Jugar" para coincidir con la solicitud
    texto_reintentar = fuente.render("Volver a Jugar", True, (255, 255, 255)) 
    pantalla.blit(texto_reintentar, (ANCHO // 2 - texto_reintentar.get_width() // 2, ALTO // 2 + 110))

    boton_salir = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 170, 200, 50)
    pygame.draw.rect(pantalla, (128, 0, 0), boton_salir)
    texto_salir = fuente.render("Salir", True, (255, 255, 255))
    pantalla.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, ALTO // 2 + 180))
    
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reintentar.collidepoint(evento.pos):
                    esperando = False
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    exit()
    fondo = fondo1
    pygame.mixer.music.unpause()

def mostrar_game_over():
    global fondo
    pygame.mixer.music.pause()
    game_over_sonido.play()
    
    pantalla.blit(fondo, (0, 0))
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    pantalla.blit(s, (0, 0))

    texto_game_over = fuente.render("GAME OVER", True, (255, 0, 0))
    pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 3))

    texto_puntaje_final = fuente.render(f"Puntaje Final: {puntaje}", True, (255, 255, 0))
    pantalla.blit(texto_puntaje_final, (ANCHO // 2 - texto_puntaje_final.get_width() // 2, ALTO // 2 + 60))

    # Botones
    boton_reintentar = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50)
    pygame.draw.rect(pantalla, (0, 128, 0), boton_reintentar)
    texto_reintentar = fuente.render("Reintentar", True, (255, 255, 255))
    pantalla.blit(texto_reintentar, (ANCHO // 2 - texto_reintentar.get_width() // 2, ALTO // 2 + 110))

    boton_salir = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 170, 200, 50)
    pygame.draw.rect(pantalla, (128, 0, 0), boton_salir)
    texto_salir = fuente.render("Salir", True, (255, 255, 255))
    pantalla.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, ALTO // 2 + 180))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reintentar.collidepoint(evento.pos):
                    esperando = False
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    exit()
    fondo = fondo1
    pygame.mixer.music.unpause()

def reiniciar_juego():
    global jugador, plataformas, objetos, puntaje, plataforma_base
    jugador = Jugador()
    plataformas = [
        Plataforma(0, ALTO - 30, ANCHO, 30),  # Plataforma base
        Plataforma(200, 450, ANCHO_PLATAFORMA, ALTO_PLATAFORMA, usar_imagen=True),
        Plataforma(400, 350, ANCHO_PLATAFORMA, ALTO_PLATAFORMA, usar_imagen=True),
        Plataforma(600, 250, ANCHO_PLATAFORMA, ALTO_PLATAFORMA, usar_imagen=True),
        Plataforma(300, 200, ANCHO_PLATAFORMA, ALTO_PLATAFORMA, usar_imagen=True),
        Plataforma(100, 120, ANCHO_PLATAFORMA, ALTO_PLATAFORMA, usar_imagen=True),
        PlataformaDesvanecible(500, 180, ANCHO_PLATAFORMA, ALTO_PLATAFORMA) 
    ]
    plataforma_base = plataformas[0]
    objetos = pygame.sprite.Group()
    for _ in range(7):
        x = random.randint(50, ANCHO - 50)
        y = random.randint(-300, -50)
        tipo = random.choice(["pinchon", "hongo"])
        objetos.add(ObjetoCaida(x, y, tipo))
    puntaje = 0

def mostrar_instrucciones():
    global pantalla
    instrucciones = [
        "JUEGO:", # Título principal
        "Usa las flechas ← y → para moverte.",
        "Presiona ESPACIO para saltar.",
        "Evita los pinchos y no caigas al vacío.",
        "Toca los hongos para obtener un super salto.",
        "Pulsa F11 para activar pantalla completa.",
        "Pulsa ESC para volver a modo ventana.",
        "Presiona cualquier tecla para comenzar..."
    ]

    pantalla.fill((0, 0, 0))
    y_offset = 100

    for linea in instrucciones:
        texto_renderizado = fuente.render(linea, True, (255, 255, 255))
        pantalla.blit(texto_renderizado, (ANCHO // 2 - texto_renderizado.get_width() // 2, y_offset))
        y_offset += 50

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# ==========================
# INICIO DEL JUEGO
# ==========================
mostrar_instrucciones() 
reiniciar_juego()

reloj = pygame.time.Clock()
pausa = False

while True:
    reloj.tick(30)

    # 🏆 VERIFICACIÓN DE PUNTUACIÓN (WINNER)
    # El puntaje ganador es 600
    if puntaje >= 600:
        mostrar_winner()
        reiniciar_juego()
        continue # Vuelve al inicio del bucle después de Winner

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p:
                pausa = not pausa
                if pausa:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            # F11 para activar Pantalla Completa
            if evento.key == pygame.K_F11:
                pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED | pygame.FULLSCREEN)
            
            # ESC para salir de Pantalla Completa (modo ventana)
            if evento.key == pygame.K_ESCAPE:
                pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED)

    if pausa:
        pantalla.blit(fondo, (0, 0))
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        pantalla.blit(s, (0, 0))
        texto_pausa = fuente.render("PAUSA - Presiona P para continuar", True, (255, 255, 255))
        pantalla.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, ALTO//2))
        pygame.display.flip()
        continue

    jugador.update(plataformas)
    objetos.update()

    # Cambio de fondo según puntaje
    if puntaje >= 350:
        fondo = espacio
    elif puntaje >= 200:
        fondo = fondo_noche2
    elif puntaje >= 100:
        fondo = fondo_2
    else:
        fondo = fondo1

    # Detección de Game Over al caer fuera de la pantalla
    if jugador.rect.top > ALTO:
        mostrar_game_over()
        reiniciar_juego()

    if jugador.rect.y < 200:
        desplazamiento = 200 - jugador.rect.y
        jugador.rect.y = 200
        for plataforma in plataformas:
            plataforma.rect.y += desplazamiento

        distancia_vertical_min = 60
        nueva_y = plataformas[-1].rect.y - random.randint(distancia_vertical_min, ALTURA_MAX_SALTO)
        nueva_x = random.randint(100, ANCHO - ANCHO_PLATAFORMA - 100)

        while abs(nueva_x - plataformas[-1].rect.x) > DISTANCIA_HORIZONTAL_MAX:
            nueva_x = random.randint(100, ANCHO - ANCHO_PLATAFORMA - 100)

        while any(abs(p.rect.y - nueva_y) < distancia_vertical_min for p in plataformas):
            nueva_y -= random.randint(20, 40)

        if random.random() < 0.3:
            plataformas.append(PlataformaDesvanecible(nueva_x, nueva_y, ANCHO_PLATAFORMA, ALTO_PLATAFORMA))
        else:
            plataformas.append(Plataforma(nueva_x, nueva_y, ANCHO_PLATAFORMA, ALTO_PLATAFORMA, usar_imagen=True))

    for objeto in objetos:
        if jugador.rect.colliderect(objeto.rect):
            if objeto.tipo == "pinchon":
                mostrar_game_over()
                reiniciar_juego()
            elif objeto.tipo == "hongo":
                puntaje += 10
                jugador.super_salto = True
                objeto.rect.y = random.randint(-200, -50)
                objeto.rect.x = random.randint(50, ANCHO - 50)

    pantalla.blit(fondo, (0, 0))
    for plataforma in plataformas:
        if plataforma.activa:
            pantalla.blit(plataforma.image, plataforma.rect.topleft)

    pantalla.blit(jugador.image, jugador.rect.topleft)
    objetos.draw(pantalla)

    texto_puntos = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (10, 10))

    pygame.display.flip()