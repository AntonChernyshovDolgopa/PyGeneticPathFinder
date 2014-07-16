from numpy import *
import time
import pygame,sys
from pygame.locals import *




condicionado=0  #1 es con inicio y final establecidos, 0 libres
Print " Once the map has been loaded left-click on a location to visit it"
ciudades=int(raw_input('How many place do you wanna visit?: ') )

def load_image(filename, transparent=False):
	try: image = pygame.image.load(filename)
	except pygame.error, message:
        	raise SystemExit, message
	image = image.convert()
	if transparent:
		color = image.get_at((0,0))
	        image.set_colorkey(color, RLEACCEL)
	return image

def inicio():

	WIDTH = 640
	HEIGHT = 480
	

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Shortest Path")
	loopFlag = True
	clk = pygame.time.Clock()
	background_image = load_image('Mapa.jpg')

	ptos=array(zeros((ciudades,2), dtype=int))
	dim=ptos.shape
	elementos=dim[0]
	k=0
	
	
	while loopFlag:
    		events = pygame.event.get()
		screen.blit(background_image, (0, 0))
    		for e in events:
			
        		if e.type==MOUSEBUTTONDOWN:
				print pygame.mouse.get_pos()
            			ptos[k]=array((pygame.mouse.get_pos()))
				k+=1
        		if e.type==QUIT:
            			loopFlag=False


		print ptos/30
		#screen.fill((255,255,255))
		j=0
		for n in ptos:
			
			pygame.draw.circle(screen, (0,0,int(j*255/elementos)), n, 10, 0)
			j+=1

  		
		pygame.display.flip()

		clk.tick(60)
		
		
		if k==elementos:
			return ptos


	return 0

ptos=inicio()
dim=ptos.shape
elementos=dim[0]
print elementos

def orden(longitud):

	inicio=0
	final=elementos-1

	b=range(0,longitud)
	a=range(0,longitud)
	
		
	if condicionado==1:
	
		a[0]=inicio
		b.remove(inicio)	
		a[longitud-1]=final
		b.remove(final)
		
	else:
		a[0]=(b[random.randint(longitud)])		
		b.remove(int(a[0]))
		a[longitud-1]=(b[random.randint(longitud-1)])		
		b.remove(int(a[longitud-1]))
	
	for i in range(1,longitud-1):
		a[i]=(b[random.randint(longitud-i-1)])		
		b.remove(int(a[i]))

	return a


def distancia(a,b):
	dist=0.0
	dist+=sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
	return dist

#la matriz con las relaciones de distancias

def matrizD(ptos):
	dim=ptos.shape
	elementos=int(dim[0])
	
	mat=array(zeros((elementos,elementos), dtype=float))
	for i in range(0,elementos):
		for j in range(0,elementos):
			mat[i][j]=distancia(ptos[i],ptos[j])
			mat[j][i]=mat[i][j]	
	return mat


def evaluar(a,matrizD):
	dist=0.0	
	for i in range(0,len(a)-1):
		dist+=matrizD[a[i]][a[i+1]]
	return dist

def valoracion(matrizPOS,matrizD):
	dim=matrizPOS.shape
	elementos=int(dim[0])
	b=[]
	for i in range(0,elementos):
		b.append(evaluar(matrizPOS[i],matrizD))

	return b

def desordenar(Ar):
	elementos=len(Ar)
	if condicionado==1:
		a=random.randint(1,elementos-1)
		b=random.randint(1,elementos-1)
	else:
		a=random.randint(0,elementos)
		b=random.randint(0,elementos)
	c=Ar[a]
	Ar[a]=Ar[b]
	Ar[b]=c
	if random.randint(4)==0:
		Ar=desordenar(Ar)
	return Ar

def combinar(a,b):
	elementos=len(a)
	c=range(0,elementos)
	d=range(0,elementos)
	e=[]
	for i in range(0,elementos):
		if condicionado==1:			
			if a[i]==b[i]:
				c[i]=a[i]
				d.remove(a[i])
	
			else:
				e.append(i)
				a[i]=0
		else:
			if a[i]==b[i] or a[i]==b[elementos-i-1]:
				c[i]=a[i]
				d.remove(a[i])
	
			else:
				e.append(i)
				a[i]=0
	for i in e:
		a[i]=d[random.randint(0,len(d))]
		d.remove(a[i])		
	return a
	

def design(ptos,individuos,generaciones):
	
	matrizDistancias = matrizD(ptos)
	dim=ptos.shape
	elementos=int(dim[0])
	matriz=array(zeros((individuos,elementos), dtype=int))
	
	for i in range(0,individuos):

		matriz[i]=orden(elementos)
	
	for i in range (0,generaciones):

		valores=valoracion(matriz,matrizDistancias)
		#comparacion
		for g in range(0,individuos):
			
			aleatorio=random.randint(individuos)

			if valores[g]>valores[aleatorio]:	
				matriz[g]=matriz[aleatorio]
		#combinacion
		#for j in range(0,int(individuos/3)):
		#	aleatorio=random.randint(individuos)
		#	matriz[aleatorio]=combinar(matriz[aleatorio],matriz[random.randint(individuos)])
		#mutacion
		#for h in range(0,int(individuos/80)):
		#	matriz[random.randint(individuos)]=orden(elementos)

		for h in range(0,int(individuos/2)):	
			aleatorio=random.randint(individuos)
			matriz[aleatorio]=desordenar(matriz[aleatorio])
		
		winner=matriz[0]
		g=0
		for i in range (1,individuos):
			if valores[g]>valores[i]:
				winner=matriz[i]
				g=i

		print valores[g]
	
	valores=valoracion(matriz,matrizDistancias)
	
	winner=matriz[0]
	g=0
	for i in range (1,individuos):
		if valores[g]>valores[i]:
			winner=matriz[i]
			g=i

	print valores[g]
	return winner



individuos=elementos**2/2
generaciones=1000
condicionado=0
matriz=array(zeros((15,elementos), dtype=int))
for i in range(0,15):
	winner=design(ptos,individuos,generaciones)
	matriz[i]=winner

matrizDistancias = matrizD(ptos)
valores=valoracion(matriz,matrizDistancias)
winner=matriz[0]
g=0
for i in range (1,15):
	if valores[g]>valores[i]:
		winner=matriz[i]
		g=i

print individuos
print winner

# Constantes
WIDTH = 640
HEIGHT = 480

def coord(n):
	return ptos[n]

print 'coordo' , ptos[1]

def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Camino mas corto")
	loopFlag = True
	clk = pygame.time.Clock()
	background_image = load_image('Mapa.jpg')

	while loopFlag:
    		events = pygame.event.get()
		
    		for e in events:
        		if e.type==QUIT:
            			loopFlag=False
        		if e.type==KEYDOWN:
            			loopFlag=False

		screen.blit(background_image, (0, 0))   #screen.fill((255,255,255))
		j=0
		for n in winner:
			pygame.draw.circle(screen, (0,0,int(j*255/elementos)), coord(n), 10, 0)
			j+=1
		for i in range(0,elementos-1):
			pygame.draw.line(screen, (55,0,int(i*255/elementos)), coord(winner[i]), coord(winner[i+1]), 2)
  
		pygame.display.flip()

		clk.tick(60)


	return 0
	 
if __name__ == '__main__':
	pygame.init()
	main()



