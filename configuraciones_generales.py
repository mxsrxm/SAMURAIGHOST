# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 4/Noviembre/2023

# Description:

import os
from csv import reader
from os import walk
import pygame


# Funcion para importar los archivos csv
def importar_capas_csv(ruta):
    mapa = []
    with open(ruta) as mapa_del_nivel:
        layout = reader(mapa_del_nivel, delimiter=',')
        for fila in layout:
            mapa.append(list(fila))
        return mapa


# Funcion para importar las imagenes
def importar_carpeta(ruta):
    lista = []

    for _, __, imagenes_archivos in walk(ruta):
        for imagen in imagenes_archivos:
            ruta_completa = ruta + '/' + imagen
            imagen_superficie = pygame.image.load(ruta_completa).convert_alpha()
            lista.append(imagen_superficie)
    return lista


# Obtener la ruta del directorio actual del script
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))

# Definir las rutas a los recursos
RUTA_IMAGENES = os.path.join(RUTA_ACTUAL, 'recursos', 'imagenes')
RUTA_SONIDOS = os.path.join(RUTA_ACTUAL, 'recursos', 'sonidos')
RUTA_CSV = os.path.join(RUTA_ACTUAL, 'recursos', 'csv')
RUTA_FUENTES = os.path.join(RUTA_ACTUAL, 'recursos', 'fuentes')
RUTA_CARACTERES = os.path.join(RUTA_ACTUAL, 'recursos', 'caracteres')

LARGO = 1024
ANCHO = 576
FPS = 60
TAMANIO_MOSAICO = 64

CONJUNTO_ELEMENTOS = {
    'movimiento_jugador': -26,
    'objeto': -40,
    'arbustos': -10,
    'invisible': 0
}

INDICADOR_ANCHO = 6
INDICADOR_VIDA_LARGO = 70
BLOQUE_TAMANIO = 80

FUENTE = os.path.join(RUTA_FUENTES, 'VCR_OSD_MONO_1.001.ttf')
FUENTE2 = os.path.join(RUTA_FUENTES, 'PressStart2P.ttf')
FUENTE3 = os.path.join(RUTA_FUENTES, 'VCR_OSD_MONO_1.001.ttf')

FUENTE_TAMANIO = 18
FUENTE2_TAMANIO = 24
FUENTE3_TAAMANIO = 16

COLOR_FONDO = 'white'
COLOR_BORDE = '#111111'
COLOR_TEXTO = 'black'
COLOR_VIDA = 'red'
COLOR_BORDE_PANTALLA = 'white'

ataque = {
    'katana': {'tiempo_de_espera_bloqueo': 50, 'danio': 20},
}

goblins = {
    # Pociones

    'pocion_vida': {'vida': 200, 'vivo': 0, 'puntos_score': 0, 'danio': 0, 'tipo_ataque': 'nulo',
                    'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'silencio.mp3'),
                    'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'juego', 'Magic1.wav'),
                    'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'silencio.mp3            '),
                    'velocidad': 0,
                    'resistencia': 3, 'radio_de_ataque': 0, 'radio_alerta': 0, 'vida_extra': 1600, 'velocidad_extra': 0,
                    'ataque_extra': 0},
    'pocion_velocidad': {'vida': 200, 'vivo': 5, 'puntos_score': 0, 'danio': 0, 'tipo_ataque': 'nulo',
                         'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'silencio.mp3'),
                         'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'juego', 'Jump.wav'),
                         'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'silencio.mp3'),
                         'velocidad': 0,
                         'resistencia': 3, 'radio_de_ataque': 0, 'radio_alerta': 0, 'vida_extra': 0,
                         'velocidad_extra': 5, 'ataque_extra': 0},
    'pocion_ataque': {'vida': 200, 'vivo': 10, 'puntos_score': 0, 'danio': 0, 'tipo_ataque': 'nulo',
                      'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'silencio.mp3'),
                      'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'juego', 'PowerUp1.wav'),
                      'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'silencio.mp3'),
                      'velocidad': 0,
                      'resistencia': 3, 'radio_de_ataque': 0, 'radio_alerta': 0, 'vida_extra': 0, 'velocidad_extra': 0,
                      'ataque_extra': 25},

    # Goblins

    'ojo': {'vida': 180, 'vivo': 1, 'puntos_score': 70, 'danio': 50, 'tipo_ataque': 'humo_gris',
            'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'enemigo.wav'),
            'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
            'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
            'velocidad': 2.5, 'resistencia': 30, 'radio_de_ataque': 50, 'radio_alerta': 250,
            'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'calavera': {'vida': 200, 'vivo': 1, 'puntos_score': 100, 'danio': 75, 'tipo_ataque': 'humo_gris',
                 'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'enemigo.wav'),
                 'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                 'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                 'velocidad': 3, 'resistencia': 90, 'radio_de_ataque': 50, 'radio_alerta': 280,
                 'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'demonio': {'vida': 300, 'vivo': 1, 'puntos_score': 150, 'danio': 100, 'tipo_ataque': 'humo_verde',
                'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'enemigo.wav'),
                'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                'velocidad': 4.5, 'resistencia': 1, 'radio_de_ataque': 60, 'radio_alerta': 340,
                'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'monstruo': {'vida': 300, 'vivo': 1, 'puntos_score': 200, 'danio': 100, 'tipo_ataque': 'humo_verde',
                 'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'enemigo.wav'),
                 'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                 'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                 'velocidad': 4.5, 'resistencia': 1, 'radio_de_ataque': 60, 'radio_alerta': 340,
                 'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'flamaAzul': {'vida': 90, 'vivo': 1, 'puntos_score': 25, 'danio': 50, 'tipo_ataque': 'aura',
                  'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'juego', 'fire.wav'),
                  'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                  'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                  'velocidad': 5, 'resistencia': 1, 'radio_de_ataque': 15, 'radio_alerta': 380,
                  'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'flamaRoja': {'vida': 90, 'vivo': 1, 'puntos_score': 25, 'danio': 50, 'tipo_ataque': 'aura',
                  'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'juego', 'fire.wav'),
                  'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                  'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                  'velocidad': 5, 'resistencia': 1, 'radio_de_ataque': 15, 'radio_alerta': 380,
                  'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    # Jefes
    'jefeAzul': {'vida': 800, 'vivo': 1, 'puntos_score': 400, 'danio': 120, 'tipo_ataque': 'portal',
                 'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'juego', 'Kill.wav'),
                 'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                 'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                 'velocidad': 4,
                 'resistencia': 3, 'radio_de_ataque': 120, 'radio_alerta': 250,
                 'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'jefeRojo': {'vida': 800, 'vivo': 1, 'puntos_score': 400, 'danio': 120, 'tipo_ataque': 'portal',
                 'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'juego', 'Kill.wav'),
                 'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                 'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'),
                 'velocidad': 3.5,
                 'resistencia': 3, 'radio_de_ataque': 120, 'radio_alerta': 250,
                 'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0},

    'jefeDemonio': {'vida': 2000, 'vivo': 1, 'puntos_score': 1000, 'danio': 160, 'tipo_ataque': 'portal',
                    'sonido_de_ataque': os.path.join(RUTA_SONIDOS, 'juego', 'Explosion4.wav'),
                    'sonido_de_muerte': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'muerte.wav'),
                    'sonido_de_golpe': os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'), 'velocidad': 1,
                    'resistencia': 8, 'radio_de_ataque': 180, 'radio_alerta': 100,
                    'vida_extra': 0, 'velocidad_extra': 0, 'ataque_extra': 0}
}
