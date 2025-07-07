import pygame
import sys
import random
import csv
from tablero import *
from preguntas import *

pygame.init()
pygame.mixer.init()

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

nombre = ""
mensaje_advertencia = ""

pantalla_menu = True
pantalla_juego = False
pantalla_score = False
pantalla_nombre = False

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
juego_terminado = False
mensaje_final = ""
ya_guardado = False

clock = pygame.time.Clock()

imagen_jugador = pygame.image.load("frisk.jpg").convert()
imagen_jugador.set_colorkey((0, 0, 0))
imagen_jugador = pygame.transform.scale(imagen_jugador, (60, 50))
imagen_estado_normal = pygame.image.load("sans1.jpg")
imagen_estado_incorrecta = pygame.image.load("sans2.jpg")
imagen_estado_normal = pygame.transform.scale(imagen_estado_normal, (110, 150))
imagen_estado_incorrecta = pygame.transform.scale(imagen_estado_incorrecta, (150, 150))
imagen_actual = imagen_estado_normal

try:
    pygame.mixer.music.load("sonido_fondo.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
except Exception as e:
    print(f"No se pudo cargar la música: {e}")

def dibujar_boton(texto, x, y, ancho, alto, color, pantalla):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    texto_render = fuente.render(texto, True, BLANCO)
    rect_texto = texto_render.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_render, rect_texto)
    return pygame.Rect(x, y, ancho, alto)

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

    if pantalla_menu:
        x_centrado = (ANCHO_VENTANA - 200) // 2
        y_centrado = (LARGO_VENTANA - 3 * 60 - 2 * 20) // 2
        boton_inicio = dibujar_boton("Iniciar", x_centrado, y_centrado, 200, 60, CELESTE, PANTALLA)
        boton_puntajes = dibujar_boton("Puntajes", x_centrado, y_centrado + 80, 200, 60, AZUL, PANTALLA)
        boton_salir = dibujar_boton("Salir", x_centrado, y_centrado + 160, 200, 60, AZUL_OSCURO, PANTALLA)

    elif pantalla_nombre:
        texto = fuente.render("Ingresar nombre (máx 5 letras):", True, BLANCO)
        PANTALLA.blit(texto, (ANCHO_VENTANA // 2 - texto.get_width() // 2, 200))
        pygame.draw.rect(PANTALLA, BLANCO, (ANCHO_VENTANA // 2 - 150, 250, 300, 40), 2)
        texto_input = fuente.render(nombre.upper(), True, BLANCO)
        texto_rect = texto_input.get_rect(center=(ANCHO_VENTANA // 2, 270))
        PANTALLA.blit(texto_input, texto_rect)

        boton_confirmar = dibujar_boton("Confirmar", ANCHO_VENTANA // 2 - 75, 320, 150, 40, AZUL, PANTALLA)

        if mensaje_advertencia:
            advertencia = fuente.render(mensaje_advertencia, True, ROJO)
            PANTALLA.blit(advertencia, (ANCHO_VENTANA // 2 - advertencia.get_width() // 2, 370))

    elif pantalla_score:
        titulo = fuente.render("--- PUNTAJES GUARDADOS ---", True, BLANCO)
        PANTALLA.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 30))

        try:
            with open("Score.csv", mode="r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                y = 80
                for fila in lector:
                    if len(fila) == 2:
                        texto_fila = fuente.render(f"{fila[0]} | {fila[1]}", True, BLANCO)
                        PANTALLA.blit(texto_fila, (50, y))
                        y += 30
        except FileNotFoundError:
            texto_error = fuente.render("No hay puntajes aún.", True, BLANCO)
            PANTALLA.blit(texto_error, (50, 100))

        boton_volver = dibujar_boton("Volver", 20, 20, 100, 40, ROJO, PANTALLA)

    elif pantalla_juego:
        if juego_terminado:
            if not ya_guardado:
                with open("Score.csv", mode="a", newline='') as archivo:
                    escritor = csv.writer(archivo)
                    escritor.writerow([f"Nombre: {nombre}", f"Puntaje: {posicion_jugador}"])
                ya_guardado = True

            PANTALLA.fill(NEGRO)
            texto_final = fuente.render(mensaje_final, True, BLANCO)
            rect_final = texto_final.get_rect(center=(ANCHO_VENTANA // 2, LARGO_VENTANA // 2))
            PANTALLA.blit(texto_final, rect_final)

            boton_volver = dibujar_boton("<", 20, 20, 50, 40, AZUL, PANTALLA)

        else:
            if not mostrar_pregunta:
                iniciar_pregunta()

            PANTALLA.blit(imagen_actual, ((ANCHO_VENTANA - imagen_actual.get_width()) // 2, 10))

            if mostrar_pregunta and posicion_pregunta is not None:
                pregunta = preguntas[posicion_pregunta]
                texto_pregunta = fuente.render(pregunta["pregunta"], True, BLANCO)
                rect_pregunta = texto_pregunta.get_rect(center=(ANCHO_VENTANA // 2, 180))
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

                if mensaje_resultado:
                    resultado_render = fuente.render(mensaje_resultado, True, BLANCO)
                    rect_res = resultado_render.get_rect(center=(ANCHO_VENTANA // 2, y_botones + alto_opcion + 40))
                    PANTALLA.blit(resultado_render, rect_res)

            for i in range(31):
                x = i * (ANCHO_CASILLA + MARGEN) + MARGEN
                y = 450
                rect = pygame.Rect(x, y, ANCHO_CASILLA, ALTO_CASILLA)

                color = CELESTE if casillas[i] != 0 else BLANCO
                pygame.draw.rect(PANTALLA, color, rect)
                pygame.draw.rect(PANTALLA, AZUL_OSCURO, rect, 2)

                texto_numero = fuente.render(str(i), True, BLANCO)
                texto_rect = texto_numero.get_rect(center=(x + ANCHO_CASILLA // 2, y - 20))
                PANTALLA.blit(texto_numero, texto_rect)

                texto_valor = fuente.render(str(casillas[i]), True, BLANCO)
                rect_valor = texto_valor.get_rect(center=(x + ANCHO_CASILLA // 2, y + ALTO_CASILLA // 2))
                PANTALLA.blit(texto_valor, rect_valor)

            pos_x_jugador = posicion_jugador * (ANCHO_CASILLA + MARGEN) + MARGEN + (ANCHO_CASILLA // 2) - (imagen_jugador.get_width() // 2)
            pos_y_jugador = 450 + (ALTO_CASILLA // 2) - (imagen_jugador.get_height() // 2)
            PANTALLA.blit(imagen_jugador, (pos_x_jugador, pos_y_jugador))

            boton_volver = dibujar_boton("<", 20, 20, 50, 40, AZUL, PANTALLA)
            boton_dejar = dibujar_boton("Dejar de jugar", ANCHO_VENTANA - 180, LARGO_VENTANA - 60, 160, 40, AZUL, PANTALLA)

            if esperar_siguiente:
                if pygame.time.get_ticks() - tiempo_espera > 1500:
                    mostrar_pregunta = False
                    esperar_siguiente = False
                    respuesta_seleccionada = None
                    mensaje_resultado = ""

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if pantalla_menu:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_inicio.collidepoint(evento.pos):
                    pantalla_menu = False
                    pantalla_nombre = True
                    mensaje_advertencia = ""
                    nombre = ""
                elif boton_puntajes.collidepoint(evento.pos):
                    pantalla_menu = False
                    pantalla_score = True
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        elif pantalla_nombre:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 5 and evento.unicode.isprintable():
                    nombre += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_confirmar.collidepoint(evento.pos):
                    if len(nombre) == 0:
                        mensaje_advertencia = "Debes escribir un nombre."
                    elif len(nombre) > 5:
                        mensaje_advertencia = "Nombre demasiado largo (máx 5)."
                    else:
                        pantalla_nombre = False
                        pantalla_juego = True
                        mostrar_pregunta = False
                        juego_terminado = False
                        mensaje_final = ""
                        posicion_jugador = 15
                        indice_preguntas = list(range(len(preguntas)))
                        ya_guardado = False
                        mensaje_advertencia = ""

        elif pantalla_score:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    pantalla_score = False
                    pantalla_menu = True

        elif pantalla_juego:
            if juego_terminado:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        pantalla_juego = False
                        pantalla_menu = True
                        ya_guardado = False
            else:
                if evento.type == pygame.MOUSEBUTTONDOWN and not esperar_siguiente:
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

                    if boton_volver.collidepoint(evento.pos):
                        pantalla_juego = False
                        pantalla_menu = True
                        ya_guardado = False

                    if boton_dejar.collidepoint(evento.pos):
                        with open("Score.csv", mode="a", newline='') as archivo:
                            escritor = csv.writer(archivo)
                            escritor.writerow([f"Nombre: {nombre}", f"Puntaje: {posicion_jugador}"])
                        pantalla_juego = False
                        pantalla_menu = True
                        ya_guardado = False

    pygame.display.update()
