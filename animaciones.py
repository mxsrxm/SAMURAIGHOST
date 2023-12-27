# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 30/Noviembre/2023

# Description: Este archivo contiene la clase Animaciones,
# la cual se encarga de crear las animaciones de los ataques y de los arbustos

from configuraciones_generales import *


class Animaciones:
    def __init__(self):
        self.frames = {

            # Animacion de ataques del jugador
            'aura': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'aura')),
            'humo_verde': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'humo_verde')),
            'portal': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'portal')),
            'humo_gris': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'humo_gris')),
            'nulo': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'nulo')),

            # Animacion de muerte de los enemigos
            'ojo': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'estela')),
            'calavera': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'estela')),

            'demonio': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'estrella')),
            'monstruo': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'estrella')),

            'flamaAzul': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'estrella')),
            'flamaRoja': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'estrella')),

            # Animacion de los jefes
            'jefeDemonio': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'trueno')),
            'jefeAzul': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'trueno')),
            'jefeRojo': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'trueno')),




            'pocion_vida': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'pocion_vida')),
            'pocion_velocidad': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'pocion_velocidad')),
            'pocion_ataque': importar_carpeta(os.path.join(RUTA_IMAGENES, 'animaciones', 'pocion_ataque'))

        }

    # Funcion para voltear las imagenes de las animaciones
    def imagenes_espejo(self, frames):
        nuevo_frame = []

        for frame in frames:
            voltear_frame = pygame.transform.flip(frame, True, False)
            nuevo_frame.append(voltear_frame)
        return nuevo_frame

    # Funcion para crear la animacion de los ataques
    def crear_animacion(self, tipo_animacion, posicion, grupos):
        animacion_frames = self.frames[tipo_animacion]
        EfectoAnimacion(posicion, animacion_frames, grupos)


class EfectoAnimacion(pygame.sprite.Sprite):
    def __init__(self, posicion, animacion_frames, grupos):
        super().__init__(grupos)
        self.frame_index = 0
        self.animacion_velocidad = 0.15
        self.frames = animacion_frames
        self.imagen = self.frames[self.frame_index]
        self.rect = self.imagen.get_rect(center=posicion)

    def animacion(self):
        self.frame_index += self.animacion_velocidad
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.imagen = self.frames[int(self.frame_index)]

    def update(self):
        self.animacion()