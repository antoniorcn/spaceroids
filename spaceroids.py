import pygame
import spaceroids_classes as cls
from pygame.locals import FULLSCREEN, KEYDOWN, K_u, K_r
from pygame.locals import JOYBUTTONDOWN
from math import sqrt
from random import randint

pygame.init()

scr = pygame.display.set_mode((640, 480), FULLSCREEN, 32)

pygame.display.set_caption("Spaceroids")


cenario = cls.Cenario()


#tiro = pygame.image.load('tiro.png')




scrhorizontal = 640
scrvertical = 480
clock = pygame.time.Clock()


estado = "menu"

#mainloop
run = True
winner = 0
time1 = 0


while run:

    if estado == "menu":
        estado = "jogando"
    elif estado == "jogando":
        cenario.update()
        cenario.draw(scr)
        pygame.display.update()
    elif estado == "pausado":
        estado = "jogando"
    elif estado == "vitoria1":
        estado = "jogando"
    elif estado == "vitoria2":
        estado = "jogando"
    else:
        run = False

    # Tratamento de eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            estado = "fim"
        if e.type == KEYDOWN:
            if e.key == K_u:
                estado = "fim"
            elif e.key == K_r:
                cenario.restart()
                estado = "jogando"
        if e.type == JOYBUTTONDOWN:
            if e.joy == 0 and e.button == 4:
                cenario.restart()
                estado = "jogando"				
            if e.joy == 0 and e.button == 9:
                estado = "fim"	
        cenario.processa_evento( e )


    clock.tick(60)

# if winner == 1:
#    print('Jogador 2 Venceu')
#elif winner == 2:
#    print ('Jogador 1 Venceu')
#else:
#    print ('Ninguem venceu')
#print (p.score)
#print (p.score2)
pygame.mixer.music.stop()
pygame.quit()