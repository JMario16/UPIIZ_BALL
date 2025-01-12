import pygame
import math
import sys

# - - - FUNCIONES - - -
def func_dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def func_col(cent_bal, cent_pun, velBx, velBy, reboteB):
    dx=cent_bal[0]-cent_pun[0]
    dy=cent_bal[1]-cent_pun[1]
    dist=math.sqrt(dx**2+dy**2)
    
    if dist==0:
        return velBx, velBy
    
    nx=dx/dist
    ny=dy/dist
    velR=velBx*nx+velBy*ny
    
    if velR>0:
        return velBx, velBy

    velBx-=2*velR*nx
    velBy-=2*velR*ny
    velBx*=reboteB
    velBy*=reboteB
    
    return velBx, velBy

# - - - CONSTANTES - - -
anch, larg=800, 600 #Ancho y largo de la ventana
grav=3708.87 #Gravedad en pixeles por segundo cuadrado
velM=3780.71 #Velocidad máxima en pixeles por segundo
fricc=0.25 #Constante de fricción del suelo suponiendolo de madera

pygame.init() #Iniciar los modulos de la librería
screen=pygame.display.set_mode((anch, larg)) #Dar tamaño a la ventana mediante variables
pygame.display.set_caption("UPIIZ BALL") #Agregar titulo a la ventana

balon=pygame.image.load("assets/balon.png").convert_alpha() #Cargar imagen del balon
fondo=pygame.image.load("assets/fondo.png").convert() #Cargar imagen del fondo
opacidad=pygame.Surface((800, 600), pygame.SRCALPHA) #Crear una superficie para objetos con opacidad
        
# - - - PROPIEDADES DEL BALON - - -
posBx, posBy=30, 420 #Posición inicial del balon en los ejes X, Y (x0, y0)
velBx, velBy=0, 0 #Velocidad inicial del balon en los ejes X, Y (vx0, vy0)
tiemLanz=None #Tiempo desde el lanzamiento
reboteB=-0.75 #Factor de rebote del balon (Para cada rebote pierde 25% de la velocidad y cambia de dirección, por eso el menos)
activoB=False #Variable para determinar si el balon ha sido lanzado
masa=0.62 #Masa del balón en kilogramos
peso=masa*grav #Peso del balón en newtons
Fnormal=peso #Fuerza normal del balón en newtons

# - - - PROPIEDADES DEL JOYSTICK - - -
posJx, posJy=400, 300 #Posición inicial del joystick en los ejes X, Y (x0, y0)
radJ=120 #Radio máximo de movimiento del joystick
activoJ=False #Variable para determinar si el joystick se esta arrastrando

# - - - VARIABLES PARA LA PARÁBOLA - - -
parabP=[]
tiP, dtP=0, 0.08
visibilidad=0, 0, 0, 180
cargar=False
p1=581, 165
p2=703, 165

clock=pygame.time.Clock() #Inicializar un reloj

running=True

while running: #Mientras la variable "running" sea "True", se ejecuta el programa
    for event in pygame.event.get(): #Para todo evento
        if event.type==pygame.QUIT: #Si ese evento es "pygame.QUIT" (Cerrar)
            running=False  #"running" sera "False". Por lo tanto se detiene el programa

        elif event.type==pygame.MOUSEBUTTONDOWN: #Si ese evento es "pygame.MOUSEBUTTONDOWN" (Click derecho)
            mouse_x, mouse_y=pygame.mouse.get_pos() #Obtener la posición del mouse
            dist=math.sqrt((mouse_x-posJx)**2+(mouse_y-posJy)**2) #Obtener la distancia entre joystick y la del mouse
            if dist<=55: #Si el clic está dentro del círculo del joystick
                activoJ=True #El joystick está activo
    
        elif event.type==pygame.MOUSEMOTION and activoJ: #Si ese evento es "pygame.MOUSEMOTION" (Ratón en movimiento), y el joystick está activo
            mouse_x, mouse_y=pygame.mouse.get_pos() #Obtener la posición del mouse
            dx, dy=mouse_x-400, mouse_y-300 #Desplazamiento del mouse en cada eje respecto la posición inicial
            dist=math.sqrt(dx**2+dy**2) #Obtener la distancia entre la posición inicial del joystick y la del mouse
            visibilidad=0, 0, 0, 150

            if dist>radJ: #Si la distancia es mayor al radio máximo
                angu=math.atan2(dy, dx) #Obtener el angulo contiguo al origen, formado por el triángulo rectangulo con C.O=dy y C.A=dx, donde dy y dx son las distancias del mouse al punto inicial
                posJx=400+radJ*math.cos(angu) #Recalcular posición del joystick para evitar que sobrepase el area definida en el eje X, tomando como referencia la posición del mouse
                posJy=300+radJ*math.sin(angu) #Recalcular posición del joystick para evitar que sobrepase el area definida en el eje Y, tomando como referencia la posición del mouse
            else:
                posJx, posJy=mouse_x, mouse_y #La posición del joystick es igual a la posición del mouse

            if not activoB:
                tiP=0
                parabP=[]
                dx=posJx-400
                dy=posJy-300
                dist=math.sqrt(dx**2+dy**2)
                angu=math.atan2(dy, dx)
                    
                if dist>0:
                    vel=(velM/radJ)*dist    
                    velBx=-vel*math.cos(angu)
                    velBy=-vel*math.sin(angu)
                else:
                    velBx, velBy=0, 0

                for i in range(1, 10):
                    x=(posBx+45)+velBx*tiP
                    y=(posBy+45)+velBy*tiP+0.5*grav*tiP**2
                    parabP.append((int(x), int(y)))
                    tiP+=dtP
                cargar=True
        
        elif event.type==pygame.MOUSEBUTTONUP and activoJ: #Si ese evento es "pygame.MOUSEBUTTONUP" (Soltar click derecho)
            if activoJ and not activoB: #Si el joystick está activo
                dx=posJx-400 #Obtener distancia entre la posición inicial y la posición final del joystick en el eje X
                dy=posJy-300 #Obtener distancia entre la posición inicial y la posición final del joystick en el eje X
                dist=math.sqrt(dx**2 + dy**2) #Obtener distancia entre la posición inicial y la posición final del joystick
                angu=math.atan2(dy, dx) #Obtener el angulo contiguo al origen, formado por el triángulo rectangulo con C.O=dy y C.A=dx, donde dy y dx son las distancias del joystick al punto inicial

                if dist>0: #Si la distancia es mayor a 0
                    vel=(velM/radJ)*dist #Obtener la magnitud de la velocidad (donde la velocidad máxima será 10m/s o 3780.71 px/s)       
                    velBx=-vel*math.cos(angu) #Obtener magnitudes para el eje X (negativo por que se lanzara en dirección contraria al joystick)
                    velBy=-vel*math.sin(angu) #Obtener magnitudes para el eje Y (negativo por que se lanzara en dirección contraria al joystick)
                    activoB=True #El balón está activo
                    tiemLanz=pygame.time.get_ticks() #Guardar la cantidad de ticks desde que se inicializo el reloj
                    clock.tick() #Reinicar el reloj
                else:
                    velBx, velBy=0, 0 #El balón no tendrá velocidad

            activoJ=False #El joystock ya no está activo
            posJx, posJy=400, 300 #Reiniciar la posición del joystick

    if activoB: #Si el balón está activo
        visibilidad=0, 0, 0, 0
        dt=clock.tick(120)/1000 #Diferencial de tiempo
        PposBx, PposBy=posBx, posBy #Guardar valor de la posición en la primer iteración del reloj
        velBy+=grav*dt #Calcular la velocidad a partir de la gravedad en el eje Y
        posBx+=velBx*dt #Calcular la posición en el eje X
        posBy+=velBy*dt #Calcular la posición en el eje Y

        dif_posBx=abs(posBx-PposBx) #Obtener diferencial de posición en el eje X
        dif_posBy=abs(posBy-PposBy) #Obtener diferencial de posición en el eje Y

        if dif_posBx<0.1: #Si el diferencial de posición en el eje X es despreciable
            velBx=0 #Igualar la velocidad en el eje X a 0
        if dif_posBy<0.1 and posBy>=larg-90: #Si el diferencial de posición en el eje Y es despreciable, y la posición en dicho eje es mayor o igual al punto de colisión en el eje Y
            velBy=0 #Igualar la velocidad en el eje Y a 0

        if posBy>=larg-90: #Si la posición en el eje Y es mayor o igual al punto de colisión en el eje Y
            posBy=larg-90 #La posición de la pelota será el punto de colisión
            velBy*=reboteB #Multiplicar la velocidad en el eje Y por el factor de rebote
            
            if velBx!=0: #Si la velocidad en el eje X es diferente de 0
                friccF=fricc*peso #Calcular la fuerza de fricción a partir del coeficiente de fricción y el peso

                if velBx>0: #Si la velocidad es mayor a 0 (hacia el eje X positivo)
                    acelF=-friccF/masa #Calcular desaceleración debida a la fuerza de fricción
                    velBx+=acelF*dt #Recalcular la velocidad a partir de esa desaseleración
                else:
                    acelF=friccF/masa #Calcular desaceleración debida a la fuerza de fricción
                    velBx+=acelF*dt #Recalcular la velocidad a partir de esa desaseleración

        if posBx<=0: #Si la posición en el eje Y es mayor o igual al punto de colisión en el eje X, lado izquierdo
            posBx=0 #La posición de la pelota será el punto de colisión
            velBx*=reboteB #Multiplicar la velocidad en el eje X por el factor de rebote
        if posBx>=anch-90: #Si la posición en el eje Y es mayor o igual al punto de colisión en el eje X, lado derecho
            posBx=anch-90 #La posición de la pelota será el punto de colisión
            velBx*=reboteB #Multiplicar la velocidad en el eje X por el factor de rebote

        cent_bal=(posBx+45, posBy+45)

        if func_dist(cent_bal, p1)<46:
            posBx, posBy=PposBx, PposBy
            velBx, velBy=func_col(cent_bal, p1, velBx, velBy, -reboteB)
        if func_dist(cent_bal, p2)<46:
            posBx, posBy=PposBx, PposBy
            velBx, velBy=func_col(cent_bal, p2, velBx, velBy, -reboteB)

        if tiemLanz and pygame.time.get_ticks()-tiemLanz>5000: #Si "tiemLanz" no es "None", y el tiempo transcurrido desde que se inicializo el reloj menos el tiempo que transcurrio desde el lanzamiento, es mayor a 5 segundos (5000 milisegundos)
            posBx, posBy=30, 420 #Devolverr balon a su posición inicial
            velBx, velBy=0, 0 #Igualar el valor de las velocidades en cada eje a 0
            tiemLanz=None #Reiniciar la variable "tiemLanz"
            activoB=False #Establecer al balón como inactivo

    opacidad.fill((0, 0, 0, 0)) #Limpiar la superfice "opacidad"

    pygame.draw.circle(opacidad, (225, 225, 225, 180), (400, 300), 75) #Dibujar circulos para el joystick en la superficie "opacidad"
    pygame.draw.circle(opacidad, (120, 120, 120, 180), (posJx, posJy), 55)
    pygame.draw.circle(opacidad, (180, 180, 180, 180), (posJx, posJy), 25)

    pygame.draw.circle(opacidad, (0, 0, 0, 0), (581, 165), 1) #Dibujar puntos de colisión de la canasta
    pygame.draw.circle(opacidad, (0, 0, 0, 0), (703, 165), 1)

    if cargar==True:
        pygame.draw.circle(opacidad, visibilidad, parabP[0], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[1], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[2], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[3], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[4], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[5], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[6], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[7], 4)
        pygame.draw.circle(opacidad, visibilidad, parabP[8], 4)

    screen.fill((225, 225, 225)) #Rellenar el fondo de la ventana
    screen.blit(fondo, (0, 0)) #Insertar imagen de fondo con inicio en 0, 0
    screen.blit(opacidad, (0, 0)) #Insertar superficie para objetos con opacidad
    screen.blit(balon, (posBx, posBy)) #Insertar imagen del balon iniciando en la posición dada mediante variables

    pygame.display.flip() #Actualizar la ventana para cargar los cambios

pygame.quit() #Salir del programa
sys.exit()