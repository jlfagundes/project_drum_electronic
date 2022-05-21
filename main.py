# importanto pygame e mixer
import pygame
from pygame import mixer 

# inicializando o pygame
pygame.init()

# configurando a tela
WIDTH = 1400
HEIGHT = 800

# adicioando cores
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
dark_gray = (50, 50, 50)

# criando a tela e definindo a legenda
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Electronic Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 24)
medium_font = pygame.font.Font('freesansbold.ttf', 16)

# taxa de quadros
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
# lista de beats
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = False
active_length = 0
active_beat = 0
beat_changed = True

# carregando os sons (quando tem diretorio usar "/" não "\")
# https://python-forum.io/thread-31219.html link de referencia para o problema encontrado
hi_hat = mixer.Sound('sounds/hi hat.WAV')
snare = mixer.Sound('sounds/snare.WAV')
kick = mixer.Sound('sounds/kick.WAV')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.wav')
tom = mixer.Sound('sounds/tom.WAV')

# tratando falta de som quando executado rapido com + 3 canais
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
  for i in range(len(clicked)):
    if clicked[i][active_beat] == 1 and active_list[i] == 1:
      if i == 0:
        hi_hat.play()
      if i == 1:
        snare.play()
      if i == 2:
        kick.play()
      if i == 3:
        crash.play()
      if i == 4:
        clap.play()
      if i == 5:
        tom.play()


def draw_grid(clicks, beat, actives):
  # rect(display, cor, [posição e altura], espessura da borda, arredondamento do canto)
  lef_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
  bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
  boxes = []
  # biblioteca de cores
  colors = [gray, white, gray]

  # botão dos instrumentos
  hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
  # blit(texto, posição) renderiza o texto na tela
  screen.blit(hi_hat_text, (30, 30))
  snare_text = label_font.render('Snare', True, colors[actives[1]])
  screen.blit(snare_text, (30, 130))
  kick_text = label_font.render('Bass Drum', True, colors[actives[2]])
  screen.blit(kick_text, (30, 230))
  crash_text = label_font.render('Crash', True, colors[actives[3]])
  screen.blit(crash_text, (30, 330))
  clap_text = label_font.render('Clap', True, colors[actives[4]])
  screen.blit(clap_text, (30, 430))
  floor_text = label_font.render('Floor Tom', True, colors[actives[5]])
  screen.blit(floor_text, (30, 530))

  # craindo linhas
  for i in range(instruments):
    # line(tela, cor, inicia da linha, fim da linha, espessora da linha)
    pygame.draw.line(screen, gray, (0, (i * 100) +100), (200, (i * 100) + 100), 5)

  # criando retangulos para as batidas
  for i in range(beats):
    for j in range(instruments):
      if clicks[j][i] == -1:
        color = gray
      else:
        if active_list[j] == 1:
          color = green
        else:
          color = dark_gray

      rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5,
        ((WIDTH - 200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)

      pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
        ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 5, 5)

      pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
        ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 2, 5)

      # armazenando os rectangulos, nos boxes, com posição de linha (i) e coluna (j)
      boxes.append((rect, (i, j)))

    # linha para saber a batida que esta tocando
    active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0,
      ((WIDTH - 200) // beats), instruments * 100], 5, 3)
  return boxes



# variavel de execução
run = True
while run:
  timer.tick(fps)
  screen.fill(black)

  # grade de desenho
  boxes = draw_grid(clicked, active_beat, active_list)

  # botão de pause
  play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
  play_text = label_font.render('Play / Pause', True, white)
  screen.blit(play_text, (70, HEIGHT - 130))
  if playing:
    play_text2 = medium_font.render('Playing', True, dark_gray)
  else:
    play_text2 = medium_font.render('Pause', True, dark_gray)
  screen.blit(play_text2, (70, HEIGHT - 100))

  # controle de bpm
  bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
  bpm_text = medium_font.render('Beats per Minute', True, white)
  screen.blit(bpm_text, (308, HEIGHT - 130))
  bpm_text2 = label_font.render(f'{bpm}', True, white)
  screen.blit(bpm_text2, (370, HEIGHT - 100))
  bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
  bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
  add_text = label_font.render('+5', True, white)
  sub_text = label_font.render('-5', True, white)
  screen.blit(add_text, (520, HEIGHT - 140))
  screen.blit(sub_text, (520, HEIGHT - 90))

  # controle de batidas
  beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
  beats_text = medium_font.render('Beats in loop', True, white)
  screen.blit(beats_text, (618, HEIGHT - 130))
  beats_text2 = label_font.render(f'{beats}', True, white)
  screen.blit(beats_text2, (680, HEIGHT - 100))
  beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
  beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
  add_text2 = label_font.render('+1', True, white)
  sub_text2 = label_font.render('-1', True, white)
  screen.blit(add_text2, (820, HEIGHT - 140))
  screen.blit(sub_text2, (820, HEIGHT - 90))

  # controle de instrumentos
  instruments_rect = []
  for i in range(instruments):
    # criar um retangula sem colocar na tela, usa tupla ao inves de lista com 4 caracteristicas
    rect = pygame.rect.Rect((0, i * 100), (200, 100))
    instruments_rect.append(rect)


  # salvar e carrgar lista de batidas
  save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
  save_text = label_font.render('Save Beat', True, white)
  screen.blit(save_text, (920, HEIGHT - 140))
  load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 200, 48], 0, 5)
  load_text = label_font.render('Load Beat', True, white)
  screen.blit(save_text, (920, HEIGHT - 90))

  # limpar batidas
  clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
  clear_text = label_font.render('Clear Board', True, white)
  screen.blit(clear_text, (1160, HEIGHT - 120))


  # verificando mudança de ritmo
  if beat_changed:
    play_notes()
    beat_changed = False


  # verificar click nas boxes e manipulação de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      for i in range(len(boxes)):
        # pegando as coordenadas do mouse usando função collidepoint()
        if boxes[i][0].collidepoint(event.pos):
          coords = boxes[i][1]
          # lista de beats clicked
          clicked[coords[1]][coords[0]] *= -1

    # capturando click botão pause
    if event.type == pygame.MOUSEBUTTONUP:
      if play_pause.collidepoint(event.pos):
        if playing:
          playing = False
        elif not playing:
          playing = True

      # capturando click para aumentar ou diminuir bpm
      elif bpm_add_rect.collidepoint(event.pos):
        bpm += 5
      elif bpm_sub_rect.collidepoint(event.pos):
        bpm -= 5

      # capturando click para aumentar ou diminuir batidas
      elif beats_add_rect.collidepoint(event.pos):
        beats += 1
        for i in range(len(clicked)):
          clicked[i].append(-1)
      elif beats_sub_rect.collidepoint(event.pos):
        beats -= 1
        for i in range(len(clicked)):
          clicked[i].pop(-1)
      
      # capturando click para limpar tela
      elif clear_button.collidepoint(event.pos):
        clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]

      # capturando click nos instrumentos
      for i in range(len(instruments_rect)):
        if instruments_rect[i].collidepoint(event.pos):
          active_list[i] *= -1


  # controle de duração de batida
  beat_length = 3600 // bpm

  # if estiver jogando então
  if playing:
    if active_length < beat_length:
      active_length += 1
    else:
      active_length = 0
      if active_beat < beats - 1:
        active_beat += 1
        beat_changed = True
      else:
        active_beat = 0
        beat_changed = True

  
  pygame.display.flip()
pygame.quit()

