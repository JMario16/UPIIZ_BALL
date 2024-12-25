import pygame
import math
import sys

# - - - VARIABLES - - -
anch=800 #Ancho de la ventana
larg=600 #Largo de la ventana
grav=3708.8667 #En pixeles por segundo cuadrado

pygame.init() #Iniciar los modulos de la librería
screen=pygame.display.set_mode((anch, larg)) #Dar tamaño a la ventana mediante variables
pygame.display.set_caption("UPIIZ BALL") #Agregar titulo a la ventana

balon=pygame.image.load("assets/balon.png").convert_alpha() #Cargar imagen del balon
fondo=pygame.image.load("assets/fondo.png").convert() #Cargar imagen del fondo
opacidad=pygame.Surface((800, 600), pygame.SRCALPHA) #Crear una superficie para objetos con opacidad
        
# - - - PROPIEDADES DEL BALON - - -
posBx=30 #Posición inicial del balon en X (x0)
posBy=0 #Posición inicial del balon en Y (y0)
velBy=0 #Velocidad inicial del balon (v0)
reboteB=-0.75 #Factor de rebote del balon (Para cada rebote pierde 25% de la velocidad y cambia de dirección, por eso el menos)
colisionB=larg-90 #Colision del balon con el suelo (el balon tiene 90px de diametro)

clock=pygame.time.Clock() #Inicializar un reloj

running=True

while running: #Mientras la variable "running" sea "True", se ejecuta el programa
    for event in pygame.event.get(): #Para todo evento
        if event.type==pygame.QUIT: #Si ese evento es "pygame.QUIT" (Cerrar)
            running=False  #"running" sera "False". Por lo tanto se detiene el programa

    pygame.draw.circle(opacidad, (225, 225, 225, 180), (400, 300), 75) #Dibujar circulos para el joystick en la superficie "opacidad"
    pygame.draw.circle(opacidad, (120, 120, 120, 180), (400, 300), 55)
    pygame.draw.circle(opacidad, (180, 180, 180, 180), (400, 300), 25)

    dt=clock.tick(60)/1000 #Diferencial de tiempo
    velBy+=grav*dt #Calcular la velocidad
    posBy+=velBy*dt #Calcular la posición

    if posBy>=colisionB: #Si la posición en el eje Y es mayor o igual al punto de colisión
        posBy=colisionB #La posición de la pelota será el punto de colisión
        velBy*=reboteB #Multiplicar la velocidad en el eje Y por el factor de rebote

    screen.fill((225, 225, 225)) #Rellenar el fondo de la ventana
    screen.blit(fondo, (0, 0)) #Insertar imagen de fondo con inicio en 0, 0
    screen.blit(balon, (posBx, posBy)) #Insertar imagen del balon en la posición dada mediante variables 
    screen.blit(opacidad, (0, 0)) #Insertar superficie para objetos con opacidad

    pygame.display.flip() #Actualizar la ventana para cargar los cambios

pygame.quit() #Salir del pprograma
sys.exit()