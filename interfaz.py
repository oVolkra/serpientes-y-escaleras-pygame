import pygame
import random
from recursos.recursos import *

def dibujar_menu_principal(pantalla, fondo_menu, fuente, boton_si, boton_no, boton_puntaje):
    """Función para cargar el texto y rects del menu principal.
    Recibe como parámetros 'pantalla', 'fondo_menu', 'fuente', 'boton_si', 'boton_no' y 'boton_puntaje'."""
    
    fuente_botones = cargar_fuente(tamaño=25)
    mostrar_imagen(pantalla, fondo_menu, posicion=(0, 0), escala = None)
    escribir_texto(pantalla, "¡BIENVENIDO A SERPIENTES Y ESCALERAS!", fuente, (10, 40))
    dibujar_rect(pantalla, (255, 255, 0), boton_si)
    dibujar_rect(pantalla, (255, 255, 0), boton_no)
    dibujar_rect(pantalla, (255, 255, 0), boton_puntaje)
    escribir_texto(pantalla, "JUGAR", fuente_botones, (boton_si.x + 12, boton_si.y + 15))
    escribir_texto(pantalla, "SALIR", fuente_botones, (boton_no.x + 12, boton_no.y + 15))
    escribir_texto(pantalla, "PUNTAJE", fuente_botones, (boton_puntaje.x + 2, boton_puntaje.y + 15))

def dibujar_pantalla_usuario(pantalla, color_rect, ingreso_rect, ingreso, fuente, fondo_usuario):
    """Función para cargar el texto y espacio de input para la pantalla de ingreso de usuario.
    Recibe como parámetros 'pantalla', 'color_rect', 'ingreso_rect', 'color_fondo', 'ingreso' y 'fuente'."""
    
    mostrar_imagen(pantalla, fondo_usuario, posicion=(0, 0), escala=None)
    dibujar_rect(pantalla, color_rect, ingreso_rect, 2)
    escribir_texto(pantalla, ingreso, fuente, (ingreso_rect.x + 5, ingreso_rect.y + 5), color=(255,255,255), borde=2, color_borde=(0,0,0))
    escribir_texto(pantalla, "Ingrese su nombre de usuario", fuente, (ingreso_rect.x - 150, ingreso_rect.y - 60), color=(255,255,255), borde=2, color_borde=(0,0,0))
    escribir_texto(pantalla, "(12 caracteres max.)", fuente, (ingreso_rect.x - 50, ingreso_rect.y - 30), color=(255,255,255), borde=2, color_borde=(0,0,0))
    pygame.display.flip()

def dibujar_pantalla_puntajes(pantalla, fuente, usuarios, puntajes, fondo_puntajes):
    """Función para cargar el texto y datos ordenados de la pantalla de puntajes.
    Recibe como parámetros 'pantalla', 'fuente', 'usuarios' y 'puntajes'"""
    
    mostrar_imagen(pantalla, fondo_puntajes, posicion=(0, 0), escala=None)
    escribir_texto(pantalla, "PUNTAJES", fuente, (300, 50), color=(255,255,255))
    y = 120
    for i in range(len(usuarios)):
        usuario = usuarios[i]
        puntaje = puntajes[i]
        escribir_texto(pantalla, f"{i+1}. {usuario}: {puntaje}", fuente, (100, y))
        y += 40
    pygame.display.flip()

def dibujar_pantalla_pregunta(pantalla, fuente, tablero, casillas, pos_jugador, jugador, pregunta_actual, segundos, fondo_tablero):
    """Función para cargar el texto, timer, tablero y modelo de jugador en la pantalla del tablero.
    Recibe como parámetros 'pantalla', 'fuente', 'tablero', 'casillas', 'pos_jugador', 'jugador', 'pregunta_actual', 'segundos' y 'fondo_tablero'."""
    
    dibujar_tablero(pantalla, tablero, fondo_tablero, escala=None)
    modelo_jugador(pantalla, casillas, pos_jugador, jugador)
    escribir_texto(pantalla, pregunta_actual["pregunta"], fuente, (50, 550))
    escribir_texto(pantalla, f"A: {pregunta_actual['respuesta_a']}", fuente, (50, 650))
    escribir_texto(pantalla, f"B: {pregunta_actual['respuesta_b']}", fuente, (50, 700))
    escribir_texto(pantalla, f"C: {pregunta_actual['respuesta_c']}", fuente, (50, 750))
    escribir_texto(pantalla, f"Tiempo restante: {segundos}s", fuente, (900, 900), color=(200,0,0))
    pygame.display.flip()

def escoger_pregunta_random(preguntas):
    """Función para escoger una pregunta aleatoria de la lista de diccionarios 'preguntas'.
    Recibe como parámetros 'preguntas'.
    Retorna una pregunta aleatoria, almacenada en 'pregunta_dicc'."""
    
    pregunta_dicc = None
    if preguntas:
        pregunta_dicc = random.choice(preguntas)
    return pregunta_dicc

def mostrar_resultado(pantalla, mensaje, tablero, casillas, pos_jugador, jugador, color, fondo_tablero):
    """Función para cargar texto en el tablero.
    Recibe como parámetros 'pantalla', 'mensaje', 'tablero', 'casillas', 'pos_jugador', 'jugador' y 'color'."""
    
    fuente_grande = cargar_fuente(tamaño=50)
    dibujar_tablero(pantalla, tablero, fondo_tablero, escala=None)
    modelo_jugador(pantalla, casillas, pos_jugador, jugador)
    escribir_texto(pantalla, mensaje, fuente_grande, (30, 700), color)

def mostrar_fin_del_juego(pantalla):
    """Función para mostrar el mensaje de fin del juego.
    Recibe como parámetro 'pantalla'."""
    
    pygame.display.flip()
    fuente_grande = cargar_fuente(tamaño=70)
    escribir_texto(pantalla, "¡Fin del juego!", fuente_grande, (380, 800), color = (255,255,255))

