import pygame
import os

RUTA_BASE = os.path.dirname(__file__)

def cargar_fuente(tamaño=30, fuente="PixelatedElegance.ttf", negrita=True):
    """Función para cargar una fuente de letra.
    Recibe como parámetros el tamaño de fuente y la fuente."""
    
    fuente_ruta = os.path.join(RUTA_BASE, fuente)
    font = pygame.font.Font(fuente_ruta, tamaño)
    font.set_bold(negrita)

    return font

def escribir_texto(pantalla, texto, fuente, posicion, color=(255, 255, 255), borde=2, color_borde=(0,0,0)):
    """Función para escribir texto y fundirlo en la pantalla.
    Recibe como parámetros 'pantalla', 'texto', 'fuente', 'posicion', 'color' = (0, 0, 0)."""
    
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(topleft=posicion)
    if borde > 0:
        borde_superficie = fuente.render(texto, True, color_borde)
        for dx in [-borde, 0, borde]:
            for dy in [-borde, 0, borde]:
                if dx != 0 or dy != 0:
                    pantalla.blit(borde_superficie, (rect.x + dx, rect.y + dy))
    
    pantalla.blit(superficie, rect)

def nombres_ventanas(texto):
    pygame.display.set_caption(texto)

def dibujar_rect(pantalla, color, rect, grosor = 0):
    """Función para dibujar rects en la pantalla.
    Recibe como parámetros 'pantalla', 'color', 'rect' y 'grosor'."""
    
    pygame.draw.rect(pantalla, color, rect, grosor)

def dibujar_tablero(pantalla, tablero, fondo=None, escala=None):
    """Función para dibujar el tablero y su fondo.
    Recibe como parámetros 'pantalla', 'tablero' y 'escala'."""
    
    if fondo is not None:
        mostrar_imagen(pantalla, fondo, posicion=(0, 0), escala=escala)
    else:
        pantalla.fill((203, 179, 150))
    mostrar_imagen(pantalla, tablero, posicion=(0, 0), escala=escala)


def mostrar_imagen(pantalla, imagen, posicion, escala):
    """Función para fundir una imagen o forma en la pantalla. Permite modificar su posición y escala.
    Recibe como parámetros 'pantalla', 'imagen', 'posicion' y 'escala'."""
    
    if escala:
        imagen = pygame.transform.scale(imagen, escala)
    
    pantalla.blit(imagen, posicion)

def modelo_jugador(pantalla, casillas, pos_jugador, jugador, escala=(80, 80)):
    """Función para cargar en las casillas del tablero el modelo del jugador, centrado y escalado en la casilla correspondiente.
    Recibe como parámetros 'pantalla', 'casillas', 'pos_jugador', 'jugador' y 'escala' = (80, 80)."""
    
    casilla = casillas[pos_jugador]
    rect = casilla["rect"]
    x = rect.x + rect.width // 2 -   escala[0] // 2
    y = rect.y + rect.height // 2 - escala[1] // 2
    mostrar_imagen(pantalla, jugador, posicion=(x, y), escala=escala)

def cargar_recursos_menu():
    """Función para cargar los recursos multimedia y botones del menu.
    No recibe parámetros.
    Retorna un diccionario con los recursos."""
    
    fondo = pygame.image.load(os.path.join(RUTA_BASE, "fondo_menu.jpg"))
    fuente = cargar_fuente()
    menuBGM = os.path.join(RUTA_BASE, "menuBGM.mp3")
    pantalla = crear_pantalla(800, 600)
    boton_si = pygame.Rect(300, 250, 120, 60)
    boton_no = pygame.Rect(300, 350, 120, 60)
    boton_puntaje = pygame.Rect(285, 450, 150, 60)
    return {"fondo": fondo, "fuente": fuente, "pantalla": pantalla, "boton_si": boton_si, "boton_no": boton_no, "boton_puntaje": boton_puntaje, "menuBGM": menuBGM}

def cargar_recursos_puntajes():
    fondo_puntaje = pygame.image.load(os.path.join(RUTA_BASE, "fondo_puntaje.png")) 
    fuente = cargar_fuente()
    return {"fondo_puntaje": fondo_puntaje, "fuente": fuente}

def cargar_recursos_pedir_usuario():
    """Función para cargar los recursos de la pantalla de ingreso de usuario.
    No recibe parámetros.
    Retorna un diccionario con los recursos."""
    
    fondo_usuario = pygame.image.load(os.path.join(RUTA_BASE, "fondo_usuario.png"))
    color_rect = (251, 252, 252)
    fuente = cargar_fuente()

    return {"fondo_usuario": fondo_usuario, "color_rect": color_rect, "fuente": fuente}

def cargar_recursos_tablero():
    """Función para cargar los recursos de la pantalla del tablero.
    No recibe parámetros.
    Retorna un diccionario con los recursos."""
    
    tablero = pygame.image.load(os.path.join(RUTA_BASE, "tablero.png"))
    fuente = cargar_fuente()
    jugador = pygame.image.load(os.path.join(RUTA_BASE, "jugador.png"))
    fondo_tablero = pygame.image.load(os.path.join(RUTA_BASE, "fondo_tablero.png"))
    tableroBGM = os.path.join(RUTA_BASE, "tableroBGM.mp3")
    return {"tablero": tablero, "fuente": fuente, "jugador": jugador, "tableroBGM": tableroBGM, "fondo_tablero": fondo_tablero}

def cargar_recursos_derrota():
    """Función para cargar los recursos del escenario de derrota.
    No recibe parámetros.
    Retorna un diccionario con los recursos."""
    
    perdisteimagen = pygame.image.load(os.path.join(RUTA_BASE, "perdisteimagen.jpg"))
    perdistesonido = os.path.join(RUTA_BASE, "perdistesonido.mp3")
    return {"img": perdisteimagen, "snd": perdistesonido}

def cargar_recursos_victoria():
    """Función para cargar los recursos del escenario de victoria.
    No recibe parámetros.
    Retorna un diccionario con los recursos."""
    
    ganasteimagen = pygame.image.load(os.path.join(RUTA_BASE, "ganasteimagen.png"))
    ganastesonido = os.path.join(RUTA_BASE, "ganastesonido.mp3")
    return {"img": ganasteimagen, "snd": ganastesonido}

def mostrar_mensaje_multimedia(pantalla, recurso, posicion_img=(550, 650), escala_img=(300, 300)):
    """Función para cargar una imagen y sonido en conjunto, utilizado para la victoria y derrota.
    Recibe como parámetros 'pantalla', 'recurso', 'posicion_img' = (550, 650) y 'escala_img' = (300, 300)."""
    
    mostrar_imagen(pantalla, recurso["img"], posicion=posicion_img, escala=escala_img)
    pygame.display.flip()
    reproducir_sonido(recurso["snd"])

def multimedia_derrota(pantalla):
    """Función para mostrar en pantalla los recursos multimedia del escenario de derrota.
    Recibe como parámetro 'pantalla'."""
    
    recursos_derrota = cargar_recursos_derrota()
    mostrar_mensaje_multimedia(pantalla, recursos_derrota)

def multimedia_victoria(pantalla):
    """Función para mostrar en pantalla los recursos multimedia del escenario de victoria.
    Recibe como parámetro 'pantalla'."""
    
    recursos_victoria = cargar_recursos_victoria()
    mostrar_mensaje_multimedia(pantalla, recursos_victoria)

def crear_pantalla(ancho, alto):
    """Función para crear una ventana de dimensiones personalizadas.
    Recibe como parámetros 'ancho' y 'alto'."""
    
    return pygame.display.set_mode((ancho, alto))

def reproducir_sonido(archivo, tiempo_ms=None, loop=False):
    """Función para reproducir archivos mp3.
    Recibe como parámetros 'archivo', 'tiempo_ms' = None y 'loop' = False."""
    
    pygame.mixer.init()
    pygame.mixer.music.load(archivo)
    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()
    if tiempo_ms:
        pygame.time.delay(tiempo_ms)
        pygame.mixer.music.stop()

