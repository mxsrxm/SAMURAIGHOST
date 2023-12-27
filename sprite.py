# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 30/Noviembre/2023
# Descripcion: Clase que crea el ataque del jugador

from math import sin
from configuraciones_generales import *


class Arma(pygame.sprite.Sprite):
    def __init__(self, jugador, grupos):
        super().__init__(grupos)
        self.tipo_sprite = 'arma'
        direccion = jugador.status.split('_')[0]

        # Carga de imagen os.path.join(RUTA_IMAGENES,

        ruta = os.path.join(RUTA_IMAGENES, 'armas', jugador.arma, direccion + '.png')

        self.imagen = pygame.image.load(ruta).convert_alpha()

        # Animacion de ataque
        # Nota: mantener el nombre de las etiquedas, deben coincidir con las de jugador.py
        # y el nombre del archivo del arma en la carpeta imagenes/armas/*
        if direccion == 'right':
            self.rect = self.imagen.get_rect(midleft=jugador.rect.midright + pygame.math.Vector2(0, 16))
        elif direccion == 'left':
            self.rect = self.imagen.get_rect(midright=jugador.rect.midleft + pygame.math.Vector2(0, 16))
        elif direccion == 'down':
            self.rect = self.imagen.get_rect(midtop=jugador.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.imagen.get_rect(midbottom=jugador.rect.midtop + pygame.math.Vector2(-10, 0))


class Mosaico(pygame.sprite.Sprite):
    def __init__(self, posicion, grupos, tipo_sprite, superficie=pygame.Surface((TAMANIO_MOSAICO, TAMANIO_MOSAICO))):
        super().__init__(grupos)
        self.tipo_sprite = tipo_sprite
        desplazamiento_en_y = CONJUNTO_ELEMENTOS[tipo_sprite]
        self.imagen = superficie

        if tipo_sprite == 'objeto':
            self.rect = self.imagen.get_rect(topleft=(posicion[0], posicion[1] - TAMANIO_MOSAICO))
        else:
            self.rect = self.imagen.get_rect(topleft=posicion)
        self.impacto = self.rect.inflate(0, desplazamiento_en_y)


class Entidad(pygame.sprite.Sprite):
    def __init__(self, grupos):
        super().__init__(grupos)
        self.frame_index = 0
        self.animacion_velocidad = 0.10
        self.direccion = pygame.math.Vector2()

    # Funcion para actualizar la animacion
    def mover(self, velocidad):
        if self.direccion.magnitude() != 0:
            self.direccion = self.direccion.normalize()

        self.impacto.x += self.direccion.x * velocidad
        self.collision('horizontal')
        self.impacto.y += self.direccion.y * velocidad
        self.collision('vertical')
        self.rect.center = self.impacto.center

    # Funcion para detectar colisiones
    def collision(self, direccion):
        if direccion == 'horizontal':
            for sprite in self.obstaculos_sprites:
                if sprite.impacto.colliderect(self.impacto):
                    if self.direccion.x > 0:
                        self.impacto.right = sprite.impacto.left
                    if self.direccion.x < 0:
                        self.impacto.left = sprite.impacto.right

        if direccion == 'vertical':
            for sprite in self.obstaculos_sprites:
                if sprite.impacto.colliderect(self.impacto):
                    if self.direccion.y > 0:
                        self.impacto.bottom = sprite.impacto.top
                    if self.direccion.y < 0:
                        self.impacto.top = sprite.impacto.bottom

    # Funcion para actualizar la animacion
    def valor_entidad(self):
        valor = sin(pygame.time.get_ticks())
        if valor >= 0:
            return 255
        else:
            return 0



    # Funcion para actualizar la animacion
    def mover(self, velocidad):
        if self.direccion.magnitude() != 0:
            self.direccion = self.direccion.normalize()

        self.impacto.x += self.direccion.x * velocidad
        self.collision('horizontal')
        self.impacto.y += self.direccion.y * velocidad
        self.collision('vertical')
        self.rect.center = self.impacto.center

    # Funcion para detectar colisiones
    def collision(self, direccion):
        if direccion == 'horizontal':
            for sprite in self.obstaculos_sprites:
                if sprite.impacto.colliderect(self.impacto):
                    if self.direccion.x > 0:
                        self.impacto.right = sprite.impacto.left
                    if self.direccion.x < 0:
                        self.impacto.left = sprite.impacto.right

        if direccion == 'vertical':
            for sprite in self.obstaculos_sprites:
                if sprite.impacto.colliderect(self.impacto):
                    if self.direccion.y > 0:
                        self.impacto.bottom = sprite.impacto.top
                    if self.direccion.y < 0:
                        self.impacto.top = sprite.impacto.bottom

    # Funcion para actualizar la animacion
    def valor_pocion(self):
        valor = sin(pygame.time.get_ticks())
        if valor >= 0:
            return 255
        else:
            return 0
