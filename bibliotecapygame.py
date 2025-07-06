from preguntas import *
from interfaz import *
from recursos.recursos import *
from funcioneslogicas import *
tablero = [0, 1, 0, 0, 0 , 3, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0]
pos_jugador = 15

def iniciar_juego():
    pygame.init()

def menu_principal():
    """Función para iniciar el menu principal, donde se puede acceder a la pantalla de ingreso de usuario, salir o puntajes.
    No recibe parámetros."""
    iniciar_juego()
    recursos_menu = cargar_recursos_menu()
    recursos_puntaje = cargar_recursos_puntajes()
    fondo_menu = recursos_menu["fondo"]
    fuente = recursos_menu["fuente"]
    pantalla = recursos_menu["pantalla"]
    boton_jugar = recursos_menu["boton_si"]
    boton_salir = recursos_menu["boton_no"]
    boton_puntaje = recursos_menu["boton_puntaje"]
    fondo_puntaje = recursos_puntaje["fondo_puntaje"]

    reproducir_sonido(recursos_menu["menuBGM"], loop=True)
    
    usuario = None
    ejecucion = True

    while ejecucion:
        dibujar_menu_principal(pantalla, fondo_menu, fuente, boton_jugar, boton_salir, boton_puntaje)
        pygame.display.flip()

        eventos = pygame.event.get()
        ejecucion = manejar_eventos_quit(ejecucion, eventos, teclas_cerrar=[pygame.K_ESCAPE])

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    usuario = pedir_usuario(pantalla, fuente, teclas_cerrar=[pygame.K_ESCAPE])
                    if usuario:
                        ejecucion = False
                elif boton_salir.collidepoint(evento.pos):
                    ejecucion = False
                elif boton_puntaje.collidepoint(evento.pos):
                    mostrar_puntajes_en_pantalla(pantalla, fuente, fondo_puntaje)
    
    return usuario

def iniciar_tablero(usuario):
    """Función que ejecuta la pantalla del tablero, junto con el modelo del jugador y las preguntas para responder.
    Recibe como parámetro 'usuario'."""
    pygame.mixer.music.stop()
    reiniciar_pantalla()
    recursos = cargar_recursos_tablero()
    tablero_imagen = recursos["tablero"]
    fuente = recursos["fuente"]
    jugador = recursos["jugador"]
    tableroBGM = recursos["tableroBGM"]
    fondo_tablero = recursos["fondo_tablero"]
    pantalla_tablero = crear_pantalla(1400, 1000)
    casillas = generar_casilleros(120, 120, 20, 60, 5)
    pos_jugador = 15
    reproducir_sonido(tableroBGM, loop=True)
    ejecutar = True

    while ejecutar:
        if not preguntas:
            ejecutar = estado_juego(pos_jugador, preguntas, pantalla_tablero, fuente,tablero_imagen, casillas, jugador, usuario, fondo_tablero)
        else:
            actualizar_tablero(pantalla_tablero, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)
            setear_tiempos(300)
            pregunta_actual = escoger_pregunta_random(preguntas)
            respuesta = registrar_respuesta(teclas_cerrar=[pygame.K_ESCAPE],tiempo_limite=15,pantalla=pantalla_tablero,fuente=fuente,pregunta_actual=pregunta_actual,tablero_imagen=tablero_imagen,casillas=casillas,pos_jugador=pos_jugador,jugador=jugador,fondo_tablero=fondo_tablero)

            if respuesta == "salir":
                actualizar_tablero(pantalla_tablero, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)
                finalizar_juego(pantalla_tablero, pos_jugador, usuario)
                ejecutar = False
            else:
                if respuesta is None:
                    mostrar_resultado(pantalla_tablero, "¡Respuesta incorrecta!",tablero_imagen, casillas, pos_jugador, jugador,(200, 0, 0), fondo_tablero)
                    setear_tiempos(2000)
                    es_correcta = False
                else:
                    es_correcta = comparar_respuesta(pregunta_actual, respuesta, pantalla_tablero, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)

                borrar_pregunta(preguntas, pregunta_actual)
                pos_jugador = avanzar_casillas(tablero, pos_jugador, es_correcta, pantalla_tablero, fuente,casillas, tablero_imagen, jugador, fondo_tablero)
                actualizar_tablero(pantalla_tablero, tablero_imagen, casillas, pos_jugador, jugador, fondo_tablero)
                ejecutar = estado_juego(pos_jugador, preguntas, pantalla_tablero, fuente,tablero_imagen, casillas, jugador, usuario, fondo_tablero)

    pygame.quit()
