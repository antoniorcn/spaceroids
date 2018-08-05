import pygame
import spaceroids_classes as cls
from pygame.locals import FULLSCREEN, KEYDOWN, K_u, K_r,MOUSEBUTTONDOWN, K_UP, K_DOWN, K_RETURN, K_p
from pygame.locals import JOYBUTTONDOWN
from math import sqrt
from random import randint

pygame.init()

scr = pygame.display.set_mode((640, 480), FULLSCREEN, 32)

font = pygame.font.SysFont("Arial", 32, False, False)

pygame.display.set_caption("Spaceroids")

#tiro = pygame.image.load('tiro.png')




scrhorizontal = 640
scrvertical = 480
clock = pygame.time.Clock()


estado = "menu"

#mainloop
run = True
winner = 0
time1 = 0

fabrica = cls.FabricaImagens("bw")
cenario = cls.Cenario(font, fabrica)


def jogar():
    global estado, cenario, fabrica
    cenario = cls.Cenario(font, fabrica)
    estado = "jogando"

def change_style():
    global fabrica
    if fabrica.get_style() == "bw":
        fabrica = cls.FabricaImagens("cor")
    else:
        fabrica = cls.FabricaImagens("bw")
    menu[menu_selected_item]["texto"] = "Style " + fabrica.get_style()

def sair():
    global estado
    estado = "sair"


menu_selected_item = 0

menu = [

    {"texto":"Jogar", "pos":(300, 100), "color":(255, 255, 0), "callback":jogar},
    {"texto":"Style " + fabrica.get_style(), "pos":(300, 200), "color":(255, 255, 0), "callback":change_style},
    {"texto":"Sair", "pos":(300, 300), "color":(255, 255, 0), "callback":sair}

]

def draw_menu(scr):
    global menu_selected_item
    scr.fill((0, 0, 0))
    for menu_index, item in enumerate(menu):
        item_menu = font.render(item["texto"], True, item["color"])
        r = item_menu.get_rect()
        r.x = item["pos"][0]
        r.y = item["pos"][1]
        item["rect"] = r
        scr.blit(item_menu, item["pos"])
        if (menu_index == menu_selected_item):
            pygame.draw.rect(scr, (255, 255, 255), r, 3)

def menu_processa_evento( ev ):
    global menu_selected_item, menu
    if ev.type == MOUSEBUTTONDOWN:
        print("botao mouse apertado ", ev.button)
        if ev.button == 1:
            print("botao esquerdo mouse apertado")
            for item in menu:
                if item["rect"].collidepoint(ev.pos):
                    print("Colidiu ", item["texto"])
                    item["callback"]()
    elif ev.type == KEYDOWN:
        if ev.key == K_UP:
            menu_selected_item -= 1
        if ev.key == K_DOWN:
            menu_selected_item += 1
        if ev.key == K_RETURN:
            menu[menu_selected_item]["callback"]()
        if menu_selected_item < 0:
            menu_selected_item = 0
        if menu_selected_item >= len(menu):
            menu_selected_item = len(menu) - 1





while run:

    if estado == "menu":
        draw_menu(scr)
        pygame.display.update()
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
            elif e.key == K_p:
                cenario.restart()
                estado = "menu"
        if e.type == JOYBUTTONDOWN:
            if e.joy == 0 and e.button == 4:
                cenario.restart()
                estado = "jogando"				
            if e.joy == 0 and e.button == 9:
                estado = "fim"

        menu_processa_evento(e)

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