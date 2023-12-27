# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 30/Noviembre/2023
# Descripcion: Clase que contiene los atributos y metodos de los enemigos
# Nota: Se importan las imagenes de la carpeta del enemigo
# mantener el nombre de las carpetas como idle, direccion y attack

import nivel
from sprite import *


class Enemigo(Entidad):
    def __init__(self,
                 nombre_enemigo,
                 posicion,
                 grupos,
                 obstaculos_sprites,
                 danio_jugador,
                 animacion_muerte,
                 puntos_nuevos,
                 enemigos_derrotados,
                 vida_extra,
                 velocidad_extra,
                 ataque_extra

                    ):

        super().__init__(grupos)
        self.nivel = nivel
        self.tipo_sprite = 'enemigo'



        # Importar imagenes del id del enemigo
        self.importar_imageness(nombre_enemigo)
        self.status = 'idle'
        self.imagen = self.animaciones[self.status][self.frame_index]

        # Posicion y colisiones
        self.rect = self.imagen.get_rect(topleft=posicion)
        self.impacto = self.rect.inflate(0, -10)
        self.obstaculos_sprites = obstaculos_sprites

        # Atributos del enemigo
        self.nombre_enemigo = nombre_enemigo
        enemigo_info = goblins[self.nombre_enemigo]
        self.vida = enemigo_info['vida']
        self.exp = enemigo_info['puntos_score']
        self.vivo = enemigo_info['vivo']
        self.vida_ext = enemigo_info['vida_extra']
        self.velocidad_ext = enemigo_info['velocidad_extra']
        self.ataque_ext = enemigo_info['ataque_extra']
        self.velocidad = enemigo_info['velocidad']
        self.danio_ataque = enemigo_info['danio']
        self.resistencia = enemigo_info['resistencia']
        self.radio_de_ataque = enemigo_info['radio_de_ataque']
        self.radio_alerta = enemigo_info['radio_alerta']
        self.tipo_ataque = enemigo_info['tipo_ataque']

        self.sonido_de_ataque = pygame.mixer.Sound(enemigo_info['sonido_de_ataque'])
        self.sonido_de_muerte = pygame.mixer.Sound(enemigo_info['sonido_de_muerte'])
        self.sonido_de_dolpe = pygame.mixer.Sound(enemigo_info['sonido_de_golpe'])

        self.sonido_de_muerte.set_volume(1)
        self.sonido_de_dolpe.set_volume(1)
        self.sonido_de_ataque.set_volume(1)

        # Ataque y bloqueo de ataque del enemigo
        self.puede_atacar = True
        self.tiempo_ataque = None
        self.tiempo_bloequeo_ataque = 400
        self.danio_al_jugador = danio_jugador
        self.animacion_muerte = animacion_muerte
        self.puntos_nuevos = puntos_nuevos
        self.enemigos_derrotados = enemigos_derrotados
        self.vida_extra = vida_extra
        self.velocidad_extra = velocidad_extra
        self.ataque_extra = ataque_extra

        # Vulnerabilidad del enemigo
        self.vulnerabilidad = True
        self.tiempo_de_golpe = None
        self.duracion = 200





    # Importar imagenes del enemigo idle, direccion y ataque
    # Nota: Se importan las imagenes de la carpeta del enemigo
    # mantener el nombre de las carpetas como idle, direccion y attack
    def importar_imageness(self, name):
        self.animaciones = {'idle': [], 'direccion': [], 'attack': []}
        ruta_principal = os.path.join(RUTA_IMAGENES, 'enemigos', name)
        for animacion in self.animaciones.keys():
            # self.animaciones[animacion] = importar_carpeta(ruta_principal + animacion)
            self.animaciones[animacion] = importar_carpeta(os.path.join(ruta_principal, animacion))

    # Direccion y distancia del jugador
    def direccion_distancia_jugador(self, jugador):
        enemigo_vec = pygame.math.Vector2(self.rect.center)
        jugador_vec = pygame.math.Vector2(jugador.rect.center)
        distancia = (jugador_vec - enemigo_vec).magnitude()

        if distancia > 0:
            direccion = (jugador_vec - enemigo_vec).normalize()
        else:
            direccion = pygame.math.Vector2()

        return (distancia, direccion)

    # Estado del enemigo
    def estado(self, jugador):
        distancia = self.direccion_distancia_jugador(jugador)[0]

        if distancia <= self.radio_de_ataque and self.puede_atacar:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distancia <= self.radio_alerta:
            self.status = 'direccion'
        else:
            self.status = 'idle'

    # Acciones del enemigo contra el jugador
    def acciones(self, jugador):
        if self.status == 'attack':
            self.tiempo_ataque = pygame.time.get_ticks()
            self.danio_al_jugador(self.danio_ataque, self.tipo_ataque)
            self.sonido_de_ataque.play()
        elif self.status == 'direccion':
            self.direccion = self.direccion_distancia_jugador(jugador)[1]
        else:
            self.direccion = pygame.math.Vector2()

    # Animacion del enemigo
    def animar(self):
        animacion = self.animaciones[self.status]

        self.frame_index += self.animacion_velocidad
        if self.frame_index >= len(animacion):
            if self.status == 'attack':
                self.puede_atacar = False
            self.frame_index = 0

        self.imagen = animacion[int(self.frame_index)]
        self.rect = self.imagen.get_rect(center=self.impacto.center)

        if not self.vulnerabilidad:
            alpha = self.valor_entidad()
            self.imagen.set_alpha(alpha)
        else:
            self.imagen.set_alpha(255)

    # Bloqueo de ataque y vulnerabilidad del enemigo
    def bloqueo(self):
        tiempo_actual = pygame.time.get_ticks()
        if not self.puede_atacar:
            if tiempo_actual - self.tiempo_ataque >= self.tiempo_bloequeo_ataque:
                self.puede_atacar = True

        if not self.vulnerabilidad:
            if tiempo_actual - self.tiempo_de_golpe >= self.duracion:
                self.vulnerabilidad = True

    # Verificar daño del enemigo ppor parte del jugador
    def danio(self, jugador, tipo_de_ataque):
        if self.vulnerabilidad:
            self.sonido_de_dolpe.play()
            self.direccion = self.direccion_distancia_jugador(jugador)[1]

            if tipo_de_ataque == 'arma':
                self.vida -= jugador.danio_total_arma()

            self.tiempo_de_golpe = pygame.time.get_ticks()
            self.vulnerabilidad = False

    # Verificar muerte del enemigo
    def verificar_muerte(self):
        if self.vida <= 0:
            if self.vivo == 5:
                self.kill()
                self.animacion_muerte(self.rect.center, self.nombre_enemigo)
                self.puntos_nuevos(self.exp)
                self.enemigos_derrotados(self.vivo)
                self.vida_extra(self.vida_ext)
                self.velocidad_extra(self.velocidad_ext)
                self.ataque_extra(self.ataque_ext)

                #reproducir bucle de sonido de muerte del enemigo durante 10 segundos
                self.sonido_de_muerte.play(loops=37)
                #volumen del sonido de muerte del enemigo
                self.sonido_de_muerte.set_volume(0.3)

            elif self.vivo == 10:
                self.kill()
                self.animacion_muerte(self.rect.center, self.nombre_enemigo)
                self.puntos_nuevos(self.exp)
                self.enemigos_derrotados(self.vivo)
                self.vida_extra(self.vida_ext)
                self.velocidad_extra(self.velocidad_ext)
                self.ataque_extra(self.ataque_ext)

                # reproducir bucle de sonido de muerte del enemigo durante 10 segundos
                self.sonido_de_muerte.play(loops=21)
                # volumen del sonido de muerte del enemigo
                self.sonido_de_muerte.set_volume(0.3)



            else:
                self.kill()
                self.animacion_muerte(self.rect.center, self.nombre_enemigo)
                self.puntos_nuevos(self.exp)
                self.enemigos_derrotados(self.vivo)
                self.vida_extra(self.vida_ext)
                self.velocidad_extra(self.velocidad_ext)
                self.ataque_extra(self.ataque_ext)

                self.sonido_de_muerte.play()




    # Reaccion del enemigo al golpe
    def reaccion_al_golpe(self):
        if not self.vulnerabilidad:
            self.direccion *= -self.resistencia

    def update(self):
        self.reaccion_al_golpe()
        self.mover(self.velocidad)
        self.animar()
        self.bloqueo()
        self.verificar_muerte()



    def actualizacion_enemigo(self, jugador):
        self.estado(jugador)
        self.acciones(jugador)
