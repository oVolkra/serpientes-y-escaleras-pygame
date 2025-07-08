import pygame
import csv
from recursos.recursos import *
from interfaz import *

def archivo_ya_existe():
    """Función que verifica la existencia o no del archivo 'score.csv'.
    No recibe parámetros.
    Devuelve un bool que determina si existe o no."""
    
    existe = False
    try:
        with open("score.csv", "r", newline="") as archivo:
            existe = bool(archivo.readline())
    except FileNotFoundError:
        existe = False
        
    return existe

def crear_archivo_score(usuario, posicion):
    """Función que crea un archivo score.csv. Una vez que ya existe, agrega los valores de las variables 'usuario' y 'posicion'.
    Recibe como parámetros 'usuario' y posicion'.
    Devuelve el archivo score.csv, actualizado con cada ejecución del juego."""
    
    nombre_columnas = not archivo_ya_existe()

    with open("score.csv", "a", newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=';')
        if nombre_columnas:
            escritor.writerow(["Usuario", "Puntaje final"])
        escritor.writerow([usuario, posicion])

def leer_puntajes_csv():
    """Función que lee el archivo 'score.csv' y guarda en una lista los datos de 'usuario' y 'posicion'.
    No recibe parámetros.
    Retorna las listas 'usuarios' y 'puntajes'."""
    
    usuarios = []
    puntajes = []
    try:
        with open("score.csv", "r", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=';')
            next(lector)
            for fila in lector:
                if len(fila) == 2:
                    usuarios.append(fila[0])
                    puntajes.append(int(fila[1]))
    except FileNotFoundError:
        pass
    
    return usuarios, puntajes

def swap_bubble_sort(listas, i, j):
    """Función que realiza el swap de un bubble sort.
    Recibe como parámetros 'listas', 'i' y 'j'.
    Devuelve los datos ordenados"""
    for lista in listas:
        aux = lista[i]
        lista[i] = lista[j]
        lista[j] = aux

def bubble_sort_puntajes_desc(usuarios, puntajes):
    """Función que realiza un bubble sort ascendente.
    Recibe como parámetros 'usuarios' y 'puntajes'."""
    
    for i in range(len(usuarios) - 1):
        for j in range(i + 1, len(usuarios)):
            if puntajes[i] > puntajes[j]:
                swap_bubble_sort([usuarios, puntajes], i, j)

def mostrar_puntajes_en_pantalla(pantalla, fuente, fondo_puntajes):
    """Función que muestra en pantalla los datos de 'score.csv' ordenados descendentemente por puntaje.
    Recibe como parámetros 'pantalla' y 'fuente'."""
    
    usuarios, puntajes = leer_puntajes_csv()
    bubble_sort_puntajes_desc(usuarios, puntajes)
    dibujar_pantalla_puntajes(pantalla, fuente, usuarios, puntajes, fondo_puntajes)
    esperando = True
    while esperando:
        eventos = pygame.event.get()
        esperando = manejar_eventos_quit(esperando, eventos, teclas_cerrar=[pygame.K_ESCAPE])

def actualizar_tablero(pantalla, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero):
    """Función que actualiza el tablero junto con el modelo del jugador, para reflejar el movimiento en el tablero.
    Recibe como parámetros 'pantalla', 'tablero_imagen', 'casillas', 'pos_jugador' y 'jugador'."""
    
    dibujar_tablero(pantalla, tablero_imagen, fondo_tablero, escala=None)
    modelo_jugador(pantalla, casillas, pos_jugador, jugador)
    pygame.display.flip()

def setear_tiempos(tiempo):
    """Función para administrar eventos de tiempo.
    Recibe como parámetro 'tiempo'."""
    
    pygame.display.flip()
    pygame.time.wait(tiempo)

def esperar_tecla(teclas_validas, teclas_cerrar=None):
    """Función que maneja los eventos de teclado.
    Recibe como parámetros 'teclas_validas' y 'teclas_cerrar'.
    Retorna 'tecla_presionada'."""
    
    tecla_presionada = None
    esperando = True
    while esperando:
        eventos = pygame.event.get()
        if not manejar_eventos_quit(True, eventos, teclas_cerrar):
            esperando = False
            tecla_presionada = None
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key in teclas_validas:
                tecla_presionada = evento.key
                esperando = False
    return tecla_presionada

def manejar_eventos_quit(ejecucion, eventos, teclas_cerrar = None):
    """Función para manejar los eventos de salida de pygame.
    Recibe como parámetros 'ejecucion', 'eventos' y 'teclas_cerrar'.
    Retorna ejecucion en False si se presiona una tecla de salida."""
    
    for evento in eventos:
        if evento.type == pygame.QUIT:
            ejecucion = False
        if evento.type == pygame.KEYDOWN and teclas_cerrar:
            if evento.key in teclas_cerrar:
                ejecucion = False
    return ejecucion

def generar_casilleros(ancho_casilla, alto_casilla, margen_x, margen_y, espacio):
    """Función para generar las colisiones de los casilleros del tablero.
    Recibe como parámetros 'ancho_casilla', 'alto_casilla', 'margen_x', 'margen_y' y 'espacio'.
    Retorna las colisiones de las casillas, con su numero de casillero asignado."""
    
    casillas = []
    
    #fila 1
    for i in range(10):
        x = margen_x + i * (ancho_casilla + espacio)
        y = margen_y
        casillas.append({"rect": pygame.Rect(x, y, ancho_casilla, alto_casilla), "numero": i})
    
    #fila 2
    for i in range(10):
        x = margen_x + i * (ancho_casilla + espacio)
        y = margen_y + alto_casilla + espacio
        casillas.append({"rect": pygame.Rect(x, y, ancho_casilla, alto_casilla), "numero": i + 10})
    
    #fila 3
    for i in range(11):
        x = margen_x + i * (ancho_casilla + espacio)
        y = margen_y + 2 * (alto_casilla + espacio)
        casillas.append({"rect": pygame.Rect(x, y, ancho_casilla, alto_casilla), "numero": i + 20})
    
    return casillas


def avanzar_casillas(tablero, posicion, es_correcta, pantalla, fuente, casillas, tablero_imagen, jugador, fondo_tablero):
    """Función encargada de calcular el avance de las casillas en función de las respuestas del usuario.
    Recibe como parámetros 'tablero','posicion', 'es_correcta', 'pantalla', 'fuente', 'casillas', 'tablero_imagen', 'jugador' y 'fondo_tablero'.
    Retorna 'posicion' actualizada."""
    
    if es_correcta:
        posicion += 1
        if posicion < len(tablero) and tablero[posicion] != 0:
            mensaje = f"¡Casilla premio! Avanza {tablero[posicion]} casilla/s."
            posicion += tablero[posicion]
            if posicion > len(tablero) - 1:
                posicion = len(tablero) - 1
            mostrar_resultado(pantalla, mensaje, tablero_imagen, casillas, posicion, jugador, color=(0, 200, 0), fondo_tablero=fondo_tablero)
            setear_tiempos(2000)
    
    else:
        posicion -= 1
        if posicion >= 0 and tablero[posicion] != 0:
            mensaje = f"¡Casilla de castigo! Retrocede {tablero[posicion]} casilla/s."
            posicion -= tablero[posicion]
            if posicion < 0:
                posicion = 0
            mostrar_resultado(pantalla, mensaje, tablero_imagen, casillas, posicion, jugador, color=(200, 0, 0), fondo_tablero=fondo_tablero)
            setear_tiempos(2000)
    
    return posicion

def pedir_usuario(pantalla, fuente, teclas_cerrar):
    """Función para mostrar la pantalla donde el usuario ingresará su nombre.
    Recibe como parámetros 'pantalla', 'fuente', 'teclas_cerrar'.
    Retorna el nombre de usuario, guardado en 'ingreso' o None si se cancela."""
    
    ingreso = ""
    ingreso_rect = pygame.Rect(230, 280, 300, 40)
    recursos = cargar_recursos_pedir_usuario()
    color_rect = recursos["color_rect"]
    fondo_usuario = recursos["fondo_usuario"]

    ejecucion = True

    while ejecucion:
        eventos = pygame.event.get()
        if not manejar_eventos_quit(True, eventos, teclas_cerrar=teclas_cerrar):
            ejecucion = False
            ingreso = None

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and ingreso != "":
                    ejecucion = False
                elif evento.key == pygame.K_BACKSPACE:
                    ingreso = ingreso[:-1]
                else:
                    if ingreso is not None and len(ingreso) < 12:
                        ingreso += evento.unicode

        dibujar_pantalla_usuario(pantalla, color_rect, ingreso_rect, ingreso if ingreso else "", fuente, fondo_usuario)

    if ingreso:
        ingreso = ingreso
    else:
        ingreso = None
    
    return ingreso

def borrar_pregunta(preguntas, pregunta_respondida):
    """Función encargada de borrar una pregunta ya respondida.
    Recibe como parámetros 'preguntas' y 'pregunta_respondida'."""

    if pregunta_respondida in preguntas:
        preguntas.remove(pregunta_respondida)

def manejar_timer_respuesta(segundos, timer_event, teclas_cerrar, pantalla, fuente, pregunta_actual, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero):
    """Función para asignar un tiempo límite de respuesta a una pregunta.
    Recibe como parámetros 'segundos', 'timer_event', 'teclas_cerrar', 'pantalla', 'fuente', 'pregunta_actual', 'tablero_imagen', 'casillas', 'pos_jugador', 'jugador' y 'fondo_tablero'.
    Retorna la respuesta del usuario y la cantidad de segundos restantes."""
    
    tecla = None
    esperando = True
    
    pygame.time.set_timer(timer_event, 1000)
    while esperando:
        eventos = pygame.event.get()
        for evento in eventos:
            if not manejar_eventos_quit(True, [evento], teclas_cerrar or [pygame.K_ESCAPE]):
                tecla = "salir"
                esperando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    tecla = "a"
                    esperando = False
                elif evento.key == pygame.K_b:
                    tecla = "b"
                    esperando = False
                elif evento.key == pygame.K_c:
                    tecla = "c"
                    esperando = False
            if evento.type == timer_event:
                segundos -= 1
                if segundos <= 0:
                    segundos = 0
                    esperando = False
        
        dibujar_pantalla_pregunta(pantalla, fuente, tablero_imagen, casillas, pos_jugador, jugador, pregunta_actual, segundos, fondo_tablero)
    
    pygame.time.set_timer(timer_event, 0)
    resultado = None
    if tecla == "salir":
        resultado = "salir"
    elif segundos == 0 and tecla is None:
        resultado = None
    else:
        resultado = tecla
    
    return resultado, segundos

def registrar_respuesta(teclas_cerrar, tiempo_limite, pantalla, fuente, pregunta_actual, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero):
    """Función que recibe la respuesta del usuario, dentro del tiempo límite.
    Recibe como parámetros 'teclas_cerrar', 'tiempo_limite', 'pantalla', 'fuente', 'pregunta_actual', 'tablero_imagen', 'casillas', 'pos_jugador', 'jugador' y 'fondo_tablero'.
    Retorna la respuesta del usuario en 'resultado'."""
    
    segundos = tiempo_limite
    timer_event = pygame.USEREVENT + 10
    resultado, segundos = manejar_timer_respuesta(
        segundos, timer_event, teclas_cerrar, pantalla, fuente, pregunta_actual, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)

    return resultado

def comparar_respuesta(pregunta, respuesta_usuario, pantalla, tablero, casillas, pos_jugador, jugador, fondo_tablero):
    """Función encargada de comparar el value del key 'respuesta_correcta' en la lista de diccionarios 'preguntas' con la respuesta del usuario.
    Recibe como parámetros 'pregunta', 'respuesta_usuario', 'pantalla', 'fuente', 'tablero', 'casillas', 'pos_jugador' y 'jugador'.
    Retorna True si la respuesta es correcta, o False en caso contrario."""
    
    actualizar_tablero(pantalla, tablero, casillas, pos_jugador, jugador, fondo_tablero)

    if respuesta_usuario == pregunta["respuesta_correcta"]:
        mensaje = "¡Respuesta correcta!"
        color = (0, 200, 0)
        es_correcta = True
    else:
        mensaje = "¡Respuesta incorrecta!"
        color = (200, 0, 0)
        es_correcta = False

    mostrar_resultado(pantalla, mensaje, tablero, casillas, pos_jugador, jugador, color=color, fondo_tablero=fondo_tablero)
    setear_tiempos(2000)

    return es_correcta

def victoria(pos_jugador):
    """Función para controlar la condición de victoria.
    Recibe como parámetro 'posicion'.
    Retorna True cuando 'posicion' == 30."""
    
    return pos_jugador == 30

def derrota(pos_jugador):
    """Función para controlar la condición de derrota.
    Recibe como parámetro 'posicion'.
    Retorna True cuando 'posicion' == 0."""
    
    return pos_jugador == 0

def sin_preguntas(preguntas):
    """Función para controlar la condición de derrota cuando la lista de preguntas queda vaca.
    Recibe como parámetro 'posicion'.
    Retorna True si la lista está vacía, False en caso contrario."""
    
    return not preguntas

def preguntar_seguir_jugando(pantalla, fuente):
    """Función para preguntarle al usuario si desea seguir jugando. Se muestra luego de responder.
    Recibe como parámetros 'pantalla' y 'fuente'.
    Retorna True si el usuario presiona 's', False si presiona 'n' o 'ESC'."""
    
    escribir_texto(pantalla, "¿Queres seguir jugando? (S/N)", fuente, (350, 650))
    pygame.display.flip()
    tecla = esperar_tecla([pygame.K_s, pygame.K_n], teclas_cerrar=[pygame.K_ESCAPE])
    
    return tecla == pygame.K_s

def printear_mensajes(pos_jugador, preguntas, pantalla):
    """Función encargada de printear los mensajes de victoria o derrota.
    Recibe como parámetros 'pos_jugador', 'preguntas' y 'pantalla'."""
    
    fuente_grande = cargar_fuente(tamaño=70)
    if victoria(pos_jugador):
        multimedia_victoria(pantalla)
        escribir_texto(pantalla, "¡GANASTE! :D", fuente_grande, (400, 550), color = (0, 255, 0))
    
    elif derrota(pos_jugador):
        multimedia_derrota(pantalla)
        escribir_texto(pantalla, "¡PERDISTE! D:", fuente_grande, (400, 550), color = (255, 0, 0))
        
   
    elif sin_preguntas(preguntas):
        multimedia_derrota(pantalla)
        escribir_texto(pantalla, "¡TE QUEDASTE SIN PREGUNTAS!", fuente_grande, (0, 550), color = (255, 0, 0))
        
def mostrar_puntajes_en_pantalla_final(pantalla, fuente, fondo_puntajes):
    """Función que crea una ventana de puntajes sin interacción del usuario.
    Recibe como parámetros 'pantalla', 'fuente' y 'fondo_puntajes'."""
    
    usuarios, puntajes = leer_puntajes_csv()
    bubble_sort_puntajes_desc(usuarios, puntajes)
    dibujar_pantalla_puntajes(pantalla, fuente, usuarios, puntajes, fondo_puntajes)
    pygame.display.flip()

def mostrar_puntajes_final():
    """Función que muestra pantalla de puntajes al finalizar la ejecución del juego.
    No recibe parámetros."""
    
    reiniciar_pantalla()
    pantalla_puntajes = pygame.display.set_mode((800, 600))
    recursos_puntaje = cargar_recursos_puntajes()
    fondo_puntaje = recursos_puntaje["fondo_puntaje"]
    fuente_puntaje = recursos_puntaje["fuente"]
    mostrar_puntajes_en_pantalla_final(pantalla_puntajes, fuente_puntaje, fondo_puntaje)
    setear_tiempos(3000)
    pygame.quit()
    exit()

def finalizar_juego(pantalla, fuente, pos_jugador, usuario, mensaje="¡Fin del juego!", color=(0,0,0)):
    """Función para ejecutar en bloque las funciones que se ejecutan al final de la ejecución.
    Recibe como parámetros 'pantalla', 'fuente', 'pos_jugador', 'usuario', 'mensaje' = "¡Fin del juego!", 'color' = (0,0,0,) y 'tiempo' = 2000."""
    
    mostrar_fin_del_juego(pantalla)
    pygame.display.flip()
    crear_archivo_score(usuario, pos_jugador)
    setear_tiempos(2000)

    mostrar_puntajes_final()

def estado_juego(pos_jugador, preguntas, pantalla, fuente, tablero_imagen, casillas, jugador, usuario, fondo_tablero):
    """Función que evalúa el estado del juego, en caso de llegar a la victoria o derrota.
    Recibe como parámetros 'pos_jugador', 'preguntas', 'pantalla', 'fuente', 'tablero_imagen', 'casillas', 'jugador' y 'usuario'."""
    
    hay_victoria = victoria(pos_jugador)
    hay_derrota = derrota(pos_jugador)
    no_hay_preguntas = sin_preguntas(preguntas)

    ejecucion = True

    if hay_victoria or hay_derrota or no_hay_preguntas:
        actualizar_tablero(pantalla, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)
        printear_mensajes(pos_jugador, preguntas, pantalla)
        finalizar_juego(pantalla, fuente, pos_jugador, usuario, mensaje="¡Fin del juego!", color=(0,0,0))
        ejecucion = False

    else:
        ejecucion = preguntar_seguir_jugando(pantalla, fuente)
        if not ejecucion:
            actualizar_tablero(pantalla, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)
            finalizar_juego(pantalla, fuente, pos_jugador, usuario, mensaje="¡Fin del juego!", color=(0,0,0))
            ejecucion = False

    return ejecucion

def reiniciar_pantalla():
    pygame.display.quit()
    pygame.display.init()

