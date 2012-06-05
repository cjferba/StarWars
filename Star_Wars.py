# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
#   Juego PyGame
#Carlos Jesus Fernandez Basso <cjferba@gmail.com>
#-------------------------------------------------------------------
import random
import os, pygame,sys,time
from pygame.locals import *
ANCHO  = 800
ALTO = 600
Conexion = None
Pantalla = None
micursor = None
s=0




class Text:
	def __init__(self, FontName = None, FontSize = 30):
		pygame.font.init()
		self.font = pygame.font.Font(FontName, FontSize)
		self.size = FontSize
		
	def render(self, surface, text, color, pos):
		text = unicode(text, "UTF-8")
		x, y = pos
		for i in text.split("\r"):
			surface.blit(self.font.render(i, 1, color), (x, y))
			y += self.size 
#-------------------------------------------------------------------
#   Función cargarImagen()
#-------------------------------------------------------------------

def cargarImagen( archivo, usarTransparencia = False ):
    lugar = os.path.join( "data", archivo )
    try:
        imagen = pygame.image.load( lugar )
    except pygame.error, mensaje:
        print "No puedo cargar la imagen:", lugar
        raise SystemExit, mensaje
    imagen = imagen.convert()
    if usarTransparencia:
        colorTransparente = imagen.get_at( (0,0) )
        imagen.set_colorkey( colorTransparente )
    return imagen
#-------------------------------------------------------------------
#   Función cargarSonido() 
#-------------------------------------------------------------------
def cargarSonido( archivo ):
    class sinSonido:
        def play( self ):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return sinSonido()
    lugar = os.path.join( "data", archivo )
    try:
        sound = pygame.mixer.Sound( lugar )
    except pygame.error, message:
        print "No puedo cargar el sonido:", lugar
        raise SystemExit, message
    return sound
#-------------------------------------------------------------------
#    XWing 
#-------------------------------------------------------------------
class XWing( pygame.sprite.Sprite ):
    def __init__( self ):
        pygame.sprite.Sprite.__init__( self )
        self.image = cargarImagen( "xwing.bmp", True )
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO/2,ALTO)
        self.dx = 0
        self.dy = 0
    def update( self ):
        self.rect.move_ip( (self.dx, self.dy) )
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top <= ALTO/2:
            self.rect.top = ALTO/2
        elif self.rect.bottom >= ALTO:
            self.rect.bottom = ALTO
#-------------------------------------------------------------------
# TIE
#-------------------------------------------------------------------
 
class TIE( pygame.sprite.Sprite ):
    def __init__( self, posx ):
        pygame.sprite.Sprite.__init__( self )
        self.image = cargarImagen( "tie_fighter.bmp", True )
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = 120
        self.dx = random.randint( -5, 5 )
        self.dy = random.randint( -5, 5 )
        
    def update( self ,a):
        self.rect.move_ip( (self.dx, self.dy) )
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.dx = -(self.dx)
        if self.rect.top < 0 or self.rect.bottom > ALTO/2:
            self.dy = -(self.dy)
        disparar = random.randint( 1, a )
        if disparar == 1:
            tieLaserGrupo.add( TIELaser( self.rect.midbottom ) )
            tieDisparo.play()
#-------------------------------------------------------------------
#   Disparos del al nave del jugador
#-------------------------------------------------------------------
class XWingLaser( pygame.sprite.Sprite ):
    
    def __init__( self, pos ):
        pygame.sprite.Sprite.__init__( self )
        self.image = cargarImagen( "rebel_laser.bmp", True )
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update( self ):
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.move_ip( (0,-4) )
            
#-------------------------------------------------------------------
#   Laser enemigos
#-------------------------------------------------------------------
class TIELaser( pygame.sprite.Sprite ):
	
	def __init__( self, pos ):
		pygame.sprite.Sprite.__init__( self )
		self.image = cargarImagen( "empire_laser.bmp", True )
		self.rect = self.image.get_rect()
		self.rect.midtop = pos
        
	def update( self ):
		if self.rect.bottom >= ALTO:
			self.kill()
		else:
			self.rect.move_ip( (0,4) )

def fin(puntos,s):
	global Pantalla
	red = (255,0,0)
	blue = (0,0,255)
	texto = Text(None,36)
	i = 'Has hecho: '
	posx = ANCHO/2+50
	posy = 175
	jug = str(i)+str(puntos)
	texto.render(Pantalla,jug,blue,(posx,posy+30))
	pygame.display.update()
#-------------------------------------------------------------------
#   Cuerpo del juego
#-------------------------------------------------------------------

random.seed()
pygame.init()
laser=60
Pantalla = pygame.display.set_mode( (ANCHO, ALTO) )
pygame.display.set_caption( "Star Wars Vidas=3" )
gameover = cargarImagen( "gameover.jpg" )
fondo_imagen = cargarImagen( "background.bmp" )
fondo_imagen2 = cargarImagen( "nivel2.jpg" )
fondo_imagen3 = cargarImagen( "nivel3.jpg" )
Pantalla.blit(fondo_imagen, (0,0))
explotar = cargarSonido( "explode1.wav" )
tieDisparo = cargarSonido( "empire_laser.wav" )
xwingDisparo = cargarSonido( "rebel_laser.wav" )
xwing = XWing()
xwingGrupo = pygame.sprite.RenderUpdates(xwing)
xwingLaserGrupo = pygame.sprite.RenderUpdates()
tieGrupo = pygame.sprite.RenderUpdates()
tieGrupo.add( TIE( 150 ) )
tieGrupo.add( TIE( 400 ) )
tieGrupo.add( TIE( 650 ) )
tieLaserGrupo = pygame.sprite.RenderUpdates()
jugando = True
intervaloEnemigos = 0
reloj = pygame.time.Clock()
nivel=1
puntos=0
vida=3
primero=0
ban=True
red = (255,0,0)
while jugando:
	reloj.tick( 60 )
###NIVEL 1###
	if nivel == 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				jugando = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jugando = False
				if event.key == K_SPACE:
					xwingLaserGrupo.add( XWingLaser( xwing.rect.midtop ) )
					xwingDisparo.play()
			elif event.type == KEYUP:
				xwing.dx , xwing.dy = 0 , 0
		
		teclasPulsadas = pygame.key.get_pressed()
		if teclasPulsadas[K_LEFT]:
			xwing.dx = -4
		if teclasPulsadas[K_RIGHT]:
			xwing.dx = 4
		if teclasPulsadas[K_UP]:
			xwing.dy = -4
		if teclasPulsadas[K_DOWN]:
			xwing.dy = 4
		intervaloEnemigos += 1
		if intervaloEnemigos >= 150 and puntos<>10:
			tieGrupo.add( TIE( 320 ) )
			intervaloEnemigos = 0
		if puntos==10:
			nivel= 2
		xwingGrupo.update()
		xwingLaserGrupo.update()
		tieGrupo.update(laser)
		tieLaserGrupo.update()
		for e in pygame.sprite.groupcollide( tieGrupo, xwingLaserGrupo, 1, 1):
			explotar.play()
			puntos=puntos +1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida)+"Puntos"+str(puntos))
		pygame.sprite.groupcollide( tieLaserGrupo, xwingLaserGrupo, 1, 1)
		if vida==0:
			jugando=False
		if len(pygame.sprite.groupcollide( tieLaserGrupo, xwingGrupo, 1, 0))>=1:
			#print"pintar game over:",puntos
			vida=vida-1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida)+"Puntos"+str(puntos))
			#jugando = False
		tieLaserGrupo.clear( Pantalla, fondo_imagen )
		tieGrupo.clear( Pantalla, fondo_imagen )
		xwingLaserGrupo.clear( Pantalla, fondo_imagen)
		xwingGrupo.clear( Pantalla, fondo_imagen )
		tieLaserGrupo.draw( Pantalla )
		xwingLaserGrupo.draw( Pantalla )
		tieGrupo.draw( Pantalla )
		xwingGrupo.draw( Pantalla )
		pygame.display.update()
		
###NIVEL 2###
	elif nivel==2:
		Pantalla.blit(fondo_imagen2, (0,0))
		if primero==0:
			vida=vida+1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida)+"Puntos"+str(puntos))
			tieGrupo.add( TIE( 150 ) )
			tieGrupo.add( TIE( 400 ) )
			tieGrupo.add( TIE( 650 ) )
			primero =1
		for event in pygame.event.get():
			if event.type == QUIT:
				jugando = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jugando = False
				if event.key == K_SPACE:
					xwingLaserGrupo.add( XWingLaser( xwing.rect.midtop ) )
					xwingDisparo.play()
			elif event.type == KEYUP:
				xwing.dx , xwing.dy = 0 , 0
		teclasPulsadas = pygame.key.get_pressed()
		if teclasPulsadas[K_LEFT]:
			xwing.dx = -4
		if teclasPulsadas[K_RIGHT]:
			xwing.dx = 4
		if teclasPulsadas[K_UP]:
			xwing.dy = -4
		if teclasPulsadas[K_DOWN]:
			xwing.dy = 4
		intervaloEnemigos += 1
		if intervaloEnemigos >= 100 and puntos<>35:
			tieGrupo.add( TIE( 320 ) )
			intervaloEnemigos = 0
		xwingGrupo.update()
		xwingLaserGrupo.update()
		laser=50
		tieGrupo.update(laser)
		tieLaserGrupo.update()
		for e in pygame.sprite.groupcollide( tieGrupo, xwingLaserGrupo, 1, 1):
			explotar.play()
			puntos=puntos + 1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida)+"Puntos"+str(puntos))
		pygame.sprite.groupcollide( tieLaserGrupo, xwingLaserGrupo, 1, 0)
		if puntos==35:
			nivel= 3
		if vida==0:
			jugando=False
		if len(pygame.sprite.groupcollide( tieLaserGrupo, xwingGrupo, 1, 0))>=1:
#			print"puntos:",puntos
			vida=vida-1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida) )
		tieLaserGrupo.clear( Pantalla, fondo_imagen2 )
		tieGrupo.clear( Pantalla, fondo_imagen2 )
		xwingLaserGrupo.clear( Pantalla, fondo_imagen2)
		xwingGrupo.clear( Pantalla, fondo_imagen2 )
		tieLaserGrupo.draw( Pantalla )
		xwingLaserGrupo.draw( Pantalla )
		tieGrupo.draw( Pantalla )
		xwingGrupo.draw( Pantalla )
		pygame.display.update()
###NIVEL 3###
	elif nivel==3:
		Pantalla.blit(fondo_imagen2, (0,0))
		if primero==0:
			vida=vida+1
			tieGrupo.add( TIE( 150 ) )
			tieGrupo.add( TIE( 400 ) )
			tieGrupo.add( TIE( 650 ) )
			primero =1
		for event in pygame.event.get():
			if event.type == QUIT:
				jugando = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jugando = False
				if event.key == K_SPACE:
					xwingLaserGrupo.add( XWingLaser( xwing.rect.midtop ) )
					xwingDisparo.play()
			elif event.type == KEYUP:
				xwing.dx , xwing.dy = 0 , 0
		teclasPulsadas = pygame.key.get_pressed()
		if teclasPulsadas[K_LEFT]:
			xwing.dx = -4 
		if teclasPulsadas[K_RIGHT]:
			xwing.dx = 4
		if teclasPulsadas[K_UP]:
			xwing.dy = -4
		if teclasPulsadas[K_DOWN]:
			xwing.dy = 4
		intervaloEnemigos += 1
		if intervaloEnemigos >= 50:
			tieGrupo.add( TIE( 320 ) )
			tieGrupo.add( TIE( 120 ) )
			intervaloEnemigos = 0
		laser=40
		xwingGrupo.update()
		xwingLaserGrupo.update()
		tieGrupo.update(laser)
		tieLaserGrupo.update()
		for e in pygame.sprite.groupcollide( tieGrupo, xwingLaserGrupo, 1, 1):
			explotar.play()
			puntos=puntos + 1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida)+"Puntos"+str(puntos))
		pygame.sprite.groupcollide( tieLaserGrupo, xwingLaserGrupo, 1, 0)
		if vida==0:
			jugando=False
		if len(pygame.sprite.groupcollide( tieLaserGrupo, xwingGrupo, 1, 0))>=1:
			#print"puntos:",puntos
			vida=vida-1
			pygame.display.set_caption( "Star Wars Vidas="+str(vida)+"Puntos"+str(puntos))
		tieLaserGrupo.clear( Pantalla, fondo_imagen2 )
		tieGrupo.clear( Pantalla, fondo_imagen2 )
		xwingLaserGrupo.clear( Pantalla, fondo_imagen2)
		xwingGrupo.clear( Pantalla, fondo_imagen2 )
		tieLaserGrupo.draw( Pantalla )
		xwingLaserGrupo.draw( Pantalla )
		tieGrupo.draw( Pantalla )
		xwingGrupo.draw( Pantalla )
		pygame.display.update()
	if vida==0:
		Pantalla.blit(gameover, (0,0))
		e=True
		texto = Text(None,36)
		texto.size = 20
		texto.render(Pantalla, "¿Jugar de nuevo? (S/N)", red,(ANCHO-350,300))
		fin(puntos,s)
		pygame.display.update()
		while e:
			for event in pygame.event.get():
				if event.type == QUIT:
					e=False
				teclasPulsadas = pygame.key.get_pressed()
				if teclasPulsadas [K_n]:
					e=False
				elif teclasPulsadas [K_s]:
					xwing = XWing()
					xwingGrupo = pygame.sprite.RenderUpdates(xwing)
					xwingLaserGrupo = pygame.sprite.RenderUpdates()
					tieGrupo = pygame.sprite.RenderUpdates()
					tieGrupo.add( TIE( 150 ) )
					tieGrupo.add( TIE( 400 ) )
					tieGrupo.add( TIE( 650 ) )
					tieLaserGrupo = pygame.sprite.RenderUpdates()
					e=False
					Jugando=True
					intervaloEnemigos = 0
					nivel=1
					puntos=0
					vida=3
					Pantalla.blit(fondo_imagen, (0,0))
					pygame.display.update()
			pygame.display.update()

