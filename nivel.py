# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 30/Noviembre/2023
import jugador
# Descripcion: Este archivo contiene la clase Nivel, la cual se encarga de crear el mapa, los sprites y la logica del juego

from sprite import *
from jugador import Jugador
from random import choice, randint
from interfaz import *
from enemigo import Enemigo
from animaciones import Animaciones
from pydub import AudioSegment

import pandas as pd


class Nivel:
    def __init__(self):

        self.pantalla = pygame.display.get_surface()
        self.juego_en_pausa = False

        self.sprites_activos = YSortCameraGroup()
        self.sprites_obstaculos = pygame.sprite.Group()

        self.ataque_en_curso = None
        self.sprites_de_ataque = pygame.sprite.Group()
        self.sprites_enemigos = pygame.sprite.Group()
        self.sonido= pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Menu9.wav'))




        # Creacion del mapa
        self.crear_mapa()

        # Creacion de la interfaz
        self.interfaz = ElementosInterfaz()

        # Creacion de las animaciones del jugador
        self.animacion_jugador = Animaciones()

        # Guardar la velocidad actual de la música
        if pygame.mixer.music.get_busy():
            self.musica_velocidad_original = pygame.mixer.music.get_pos() / 1000.0  # Convertir a segundos

            # Creacion de la camara del juego y el mapa, se crean los sprites del mapa
    def crear_mapa(self):

        # Creacion de las capas del mapa
        capas = {
            'cerca': importar_capas_csv(os.path.join(RUTA_CSV, 'new_base_cerca.csv')),
            'arbustos': importar_capas_csv(os.path.join(RUTA_CSV, 'new_base_arbustos.csv')),
            'objeto': importar_capas_csv(os.path.join(RUTA_CSV, 'new_base_colision.csv')),
            'personajes': importar_capas_csv(os.path.join(RUTA_CSV, 'u_personajes.csv')),
        }
        elementos_extra = {
            'arbustos': importar_carpeta(os.path.join(RUTA_IMAGENES, 'arbustos')),
            'elementos': importar_carpeta(os.path.join(RUTA_IMAGENES, 'elementos')),
        }

        # Creacion de los sprites del mapa
        for estilo, layout in capas.items():
            for fila_index, fila in enumerate(layout):
                for columna_index, columna in enumerate(fila):
                    if columna != '-1':
                        x = columna_index * TAMANIO_MOSAICO
                        y = fila_index * TAMANIO_MOSAICO

                        if estilo == 'cerca':
                            Mosaico((x, y), [self.sprites_obstaculos], 'invisible')

                        if estilo == 'arbustos':
                            arbusto_al_azar = choice(elementos_extra['arbustos'])
                            Mosaico(
                                (x, y),
                                [self.sprites_activos, self.sprites_obstaculos, self.sprites_enemigos],
                                'arbustos',
                                arbusto_al_azar)

                        if estilo == 'objeto':

                            indice_elemento = int(columna)
                            surf = elementos_extra['elementos'][indice_elemento]
                            Mosaico((x, y), [self.sprites_activos, self.sprites_obstaculos], 'objeto', surf)


                        if estilo == 'personajes':
                            if columna == '0':
                                self.jugador = Jugador(
                                    (x, y),
                                    [self.sprites_activos],
                                    self.sprites_obstaculos,
                                    self.crear_ataque,
                                    self.destruir_ataque)
                            else:
                                if columna == '1':
                                    nombre_enemigo = 'ojo'
                                elif columna == '2':
                                    nombre_enemigo = 'calavera'
                                elif columna == '3':
                                    nombre_enemigo = 'demonio'
                                elif columna == '4':
                                    nombre_enemigo = 'monstruo'
                                elif columna == '5':
                                    nombre_enemigo = 'flamaAzul'
                                elif columna == '6':
                                    nombre_enemigo = 'flamaRoja'
                                elif columna == '7':
                                    nombre_enemigo = 'jefeAzul'
                                elif columna == '8':
                                    nombre_enemigo = 'jefeRojo'
                                elif columna == '9':
                                    nombre_enemigo = 'jefeDemonio'
                                elif columna == '10':
                                    nombre_enemigo = 'pocion_vida'
                                elif columna == '11':
                                    nombre_enemigo = 'pocion_velocidad'
                                else:
                                    nombre_enemigo = 'pocion_ataque'

                                Enemigo(
                                    nombre_enemigo,(x, y),
                            [self.sprites_activos,self.sprites_enemigos],
                                    self.sprites_obstaculos,
                                    self.danio,
                                    self.animacion_de_muerte,
                                    self.nuevos_puntos_score,
                                    self.nuevos_enemigos_derrotados,
                                    self.vida_extra,
                                    self.velocidad_extra,
                                    self.ataque_extra

                                )


    # Creacion de los ataques del jugador
    def crear_ataque(self):
        self.ataque_en_curso = Arma(self.jugador, [self.sprites_activos, self.sprites_de_ataque])

    # Destruccion de los ataques del jugador
    def destruir_ataque(self):
        if self.ataque_en_curso:
            self.ataque_en_curso.kill()
        self.ataque_en_curso = None

    # Logica de los ataques del jugador
    def logica_ataque(self):
        if self.sprites_de_ataque:
            for sprite_ataque in self.sprites_de_ataque:
                pared_sprites_invisible_choque = pygame.sprite.spritecollide(sprite_ataque, self.sprites_enemigos,
                                                                             False)
                if pared_sprites_invisible_choque:
                    for objetivo in pared_sprites_invisible_choque:
                        if objetivo.tipo_sprite == 'arbustos':
                            posicion = objetivo.rect.center
                            offset = pygame.math.Vector2(0, 75)

                            objetivo.kill()
                        else:
                            objetivo.danio(self.jugador, sprite_ataque.tipo_sprite)

    # Logica de los ataques de los enemigos
    def danio(self, cantidad, tipo_ataque):
        if self.jugador.vulnerabilidad:
            self.jugador.vida -= cantidad
            self.jugador.vulnerabilidad = False
            self.jugador.tiempo_de_herida = pygame.time.get_ticks()
            self.animacion_jugador.crear_animacion(tipo_ataque, self.jugador.rect.center, [self.sprites_activos])

    # Logica de la muerte del enemigo
    def animacion_de_muerte(self, pocicion, tipo_animacion):
        self.animacion_jugador.crear_animacion(tipo_animacion, pocicion, self.sprites_activos)

    # Logica de los puntos score del jugador
    def nuevos_puntos_score(self, cantidad):
        self.jugador.score += cantidad

    def nuevos_enemigos_derrotados(self, cantidad):
        self.jugador.enemigos_derrotados += cantidad

    def vida_extra(self, cantidad):
        self.jugador.vida += cantidad

    def velocidad_extra(self, cantidad):
        self.jugador.velocidad += cantidad
        self.jugador.tiempo_velocidad_extra = pygame.time.get_ticks()


    def ataque_extra(self, cantidad):
        self.jugador.danio_ataque += cantidad
        self.jugador.tiempo_ataque_extra = pygame.time.get_ticks()



    def run(self):
        self.sprites_activos.panel(self.jugador)
        self.interfaz.display(self.jugador)
        self.sprites_activos.update()
        self.sprites_activos.actualizacion_enemigo(self.jugador)
        self.logica_ataque()




class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()

        self.superficie_pantalla = pygame.display.get_surface()
        self.mitad_largo = self.superficie_pantalla.get_size()[0] // 2
        self.mitad_ancho = self.superficie_pantalla.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creacion del mapa base
        self.superficie_piso = pygame.image.load(
            os.path.join(RUTA_IMAGENES, 'mapa', 'new_base_mapa.png')).convert()
        self.superficie_cuadro = self.superficie_piso.get_rect(topleft=(0, 0))

    #
    def panel(self, jugador):

        self.offset.x = jugador.rect.centerx - self.mitad_largo
        self.offset.y = jugador.rect.centery - self.mitad_ancho

        pocicion_del_piso = self.superficie_cuadro.topleft - self.offset
        self.superficie_pantalla.blit(self.superficie_piso, pocicion_del_piso)

        # Dibujar los sprites en la pantalla
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_posicion = sprite.rect.topleft - self.offset
            self.superficie_pantalla.blit(sprite.imagen, offset_posicion)

    # Actualizacion de los enemigos en el nivel
    def actualizacion_enemigo(self, jugador):
        sprites_enemigos = [sprite for sprite in self.sprites() if
                            hasattr(sprite, 'tipo_sprite') and sprite.tipo_sprite == 'enemigo']
        for enemigo in sprites_enemigos:
            enemigo.actualizacion_enemigo(jugador)