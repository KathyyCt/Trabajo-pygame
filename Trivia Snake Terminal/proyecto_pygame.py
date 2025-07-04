import pygame
import sys
import random
from tablero import *
from preguntas import *

pygame.init()
pygame.mixer.init()  # Inicializar el mixer para audio

# Tamaños
ANCHO_VENTANA = 1100
LARGO_VENTANA = 600
ANCHO_CASILLA = 30
ALTO_CASILLA = 80

# Colores
BLANCO = (255, 255, 255)
AZUL_OSCURO = (0, 0, 139)
AZUL = (0, 120, 215)
CELESTE = (135, 206, 250)
ROJO = (200, 0, 0)
NEGRO = (0, 0, 0)
MARGEN = 5

# Pantalla
PANTALLA = pygame.display.set_mode((ANCHO_VENTANA, LARGO_VENTANA))
pygame.display.set_caption("Trivia Snake")

fuente = pygame.font.SysFont(None, 30)

def dibujar_boton(texto, x, y, ancho, alto, color, pantalla):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    texto_render = fuente.render(texto, True, BLANCO)
    rect_texto = texto_render.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_render, rect_texto)
    return pygame.Rect(x, y, ancho, alto)

imagen_jugador = pygame.image.load("frisk.jpg")

ANCHO_IMAGEN_JUGADOR = 60
ALTO_IMAGEN_JUGADOR = 50 

imagen_jugador = pygame.transform.scale(imagen_jugador, (ANCHO_IMAGEN_JUGADOR, ALTO_IMAGEN_JUGADOR))

imagen_estado_normal = pygame.image.load("sans1.jpg")
imagen_estado_incorrecta = pygame.image.load("sans2.jpg")

ANCHO_IMAGEN_ESTADO = 150
ALTO_IMAGEN_ESTADO = 150

imagen_estado_normal = pygame.transform.scale(imagen_estado_normal, (110, ALTO_IMAGEN_ESTADO))
imagen_estado_incorrecta = pygame.transform.scale(imagen_estado_incorrecta, (ANCHO_IMAGEN_ESTADO, ALTO_IMAGEN_ESTADO))

# Imagen botones, normal
imagen_actual = imagen_estado_normal

# Estado botones y posiciones
ancho_boton = 200
alto_boton = 60
espacio_entre = 20
x_centrado = (ANCHO_VENTANA - ancho_boton) // 2
y_total = alto_boton * 2 + espacio_entre
y_centrado = (LARGO_VENTANA - y_total) // 2

pantalla_menu = True
pantalla_juego = False
flag_correr = True

posicion_jugador = 15

indice_preguntas = list(range(len(preguntas)))
mostrar_pregunta = False
respuesta_seleccionada = None
mensaje_resultado = ""
posicion_pregunta = None
botones = []
boton_salir = None
esperar_siguiente = False
tiempo_espera = 0

# Variables para estado final del juego
juego_terminado = False
mensaje_final = ""

clock = pygame.time.Clock()

try:
    pygame.mixer.music.load("sonido_fondo.mp3") 
    pygame.mixer.music.play(-1)  
    pygame.mixer.music.set_volume(0.1)
except Exception as e:
    print(f"No se pudo cargar la música: {e}")

def iniciar_pregunta():
    global posicion_pregunta, mostrar_pregunta, respuesta_seleccionada, mensaje_resultado, esperar_siguiente
    if not indice_preguntas:
        indice_preguntas.extend(range(len(preguntas)))
    posicion_pregunta = random.choice(indice_preguntas)
    indice_preguntas.remove(posicion_pregunta)
    mostrar_pregunta = True
    respuesta_seleccionada = None
    mensaje_resultado = ""
    esperar_siguiente = False

while flag_correr:
    PANTALLA.fill(NEGRO)
    dt = clock.tick(60)

    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if pantalla_menu:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_inicio.collidepoint(evento.pos):
                    pantalla_menu = False
                    pantalla_juego = True
                    mostrar_pregunta = False
                    juego_terminado = False
                    mensaje_final = ""
                    posicion_jugador = 15
                    indice_preguntas = list(range(len(preguntas)))
                elif boton_salir and boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        elif pantalla_juego and mostrar_pregunta and evento.type == pygame.MOUSEBUTTONDOWN and not esperar_siguiente and not juego_terminado:
            for boton, clave in botones:
                if boton.collidepoint(evento.pos):
                    respuesta_seleccionada = clave
                    correcta = "respuesta_" + preguntas[posicion_pregunta]["respuesta_correcta"]
                    cantidad = casillas[posicion_jugador]

                    if clave == correcta:
                        mensaje_resultado = "¡Correcto!"
                        nueva_pos = posicion_jugador + 1 + cantidad
                        posicion_jugador = min(nueva_pos, len(casillas) - 1)
                        imagen_actual = imagen_estado_normal  
                    else:
                        mensaje_resultado = "Incorrecto."
                        nueva_pos = posicion_jugador - 1 - cantidad
                        posicion_jugador = max(nueva_pos, 0)
                        imagen_actual = imagen_estado_incorrecta  

                    if posicion_jugador >= 30:
                        juego_terminado = True
                        mensaje_final = "¡Ganaste!"
                        mostrar_pregunta = False
                    elif posicion_jugador <= 0:
                        juego_terminado = True
                        mensaje_final = "Perdiste."
                        mostrar_pregunta = False
                    elif not indice_preguntas:
                        juego_terminado = True
                        mensaje_final = "Te quedaste sin preguntas."
                        mostrar_pregunta = False

                    esperar_siguiente = True
                    tiempo_espera = pygame.time.get_ticks()

            if boton_salir and boton_salir.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    if pantalla_menu:
        boton_inicio = dibujar_boton("Iniciar", x_centrado, y_centrado, ancho_boton, alto_boton, CELESTE, PANTALLA)
        boton_salir = dibujar_boton("Salir", x_centrado, y_centrado + alto_boton + espacio_entre, ancho_boton, alto_boton, AZUL_OSCURO, PANTALLA)

    if pantalla_juego:
        PANTALLA.fill(NEGRO)

        # Casillas
        for i in range(31):
            x = i * (ANCHO_CASILLA + MARGEN) + MARGEN
            y = 50
            rect = pygame.Rect(x, y, ANCHO_CASILLA, ALTO_CASILLA)

            if casillas[i] != 0:
                color = CELESTE
            else:
                color = BLANCO

            pygame.draw.rect(PANTALLA, color, rect)
            pygame.draw.rect(PANTALLA, AZUL_OSCURO, rect, 2)

            texto_numero = fuente.render(str(i), True, BLANCO)
            texto_rect = texto_numero.get_rect(center=(x + ANCHO_CASILLA // 2, y - 20))
            PANTALLA.blit(texto_numero, texto_rect)

            texto_valor = fuente.render(str(casillas[i]), True, BLANCO)
            rect_valor = texto_valor.get_rect(center=(x + ANCHO_CASILLA // 2, y + ALTO_CASILLA // 2))
            PANTALLA.blit(texto_valor, rect_valor)

        
        pos_x_jugador = posicion_jugador * (ANCHO_CASILLA + MARGEN) + MARGEN + (ANCHO_CASILLA - ANCHO_IMAGEN_JUGADOR) // 2
        pos_y_jugador = 50 + ALTO_CASILLA + 5
        PANTALLA.blit(imagen_jugador, (pos_x_jugador, pos_y_jugador))

        if juego_terminado:
            
            texto_final = fuente.render(mensaje_final, True, BLANCO)
            rect_final = texto_final.get_rect(center=(ANCHO_VENTANA // 2, LARGO_VENTANA // 2))
            PANTALLA.blit(texto_final, rect_final)
        else:
            
            if not mostrar_pregunta:
                iniciar_pregunta()

            if mostrar_pregunta and posicion_pregunta is not None:
                pregunta = preguntas[posicion_pregunta]
                texto_pregunta = fuente.render(pregunta["pregunta"], True, BLANCO)
                rect_pregunta = texto_pregunta.get_rect(center=(ANCHO_VENTANA // 2, 200))
                PANTALLA.blit(texto_pregunta, rect_pregunta)

                opciones = ["respuesta_a", "respuesta_b", "respuesta_c"]
                textos_opciones = [pregunta[o] for o in opciones]

                ancho_opcion = 300
                alto_opcion = 50
                espacio = 50
                total_ancho = ancho_opcion * 3 + espacio * 2
                x_inicio = (ANCHO_VENTANA - total_ancho) // 2
                y_botones = rect_pregunta.bottom + 20

                botones = []
                for i, clave in enumerate(opciones):
                    x = x_inicio + i * (ancho_opcion + espacio)
                    color = CELESTE if respuesta_seleccionada == clave else AZUL
                    boton = dibujar_boton(textos_opciones[i], x, y_botones, ancho_opcion, alto_opcion, color, PANTALLA)
                    botones.append((boton, clave))

                # Botón Salir
                boton_salir = dibujar_boton("Salir", ANCHO_VENTANA - 90, y_botones + alto_opcion + 10, 70, 30, ROJO, PANTALLA)

                # Mostrar imagen debajo solo si no terminó el juego
                pos_x_imagen_estado = (ANCHO_VENTANA - ANCHO_IMAGEN_ESTADO) // 2
                pos_y_imagen_estado = y_botones + alto_opcion + 50
                PANTALLA.blit(imagen_actual, (pos_x_imagen_estado, pos_y_imagen_estado))

                if mensaje_resultado:
                    resultado_render = fuente.render(mensaje_resultado, True, BLANCO)
                    rect_res = resultado_render.get_rect(center=(ANCHO_VENTANA // 2, pos_y_imagen_estado + ALTO_IMAGEN_ESTADO + 20))
                    PANTALLA.blit(resultado_render, rect_res)

        if esperar_siguiente:
            if pygame.time.get_ticks() - tiempo_espera > 1500:
                mostrar_pregunta = False
                esperar_siguiente = False
                respuesta_seleccionada = None
                mensaje_resultado = ""

    pygame.display.update()
