import pygame
import threading
from threading import Thread
from threading import ThreadError
from datetime import datetime
import time
import chess_timer

TIME_LIMIT = 3 * 60
#TIME_LIMIT = 3

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
WINDOW_TITLE = "Chess Timer"
WINDOW_ICON = "icon_clock.png"
BACKGROUND_COLOR = (100, 255, 200)
TIMER_BACKGROUND_COLOR = (0,0,0)
TEXT_COLOR = (255, 255, 255)
TEXT_NOTI_COLOR = (100,200,10)
TITLE_COLOR = (180,180,10)

END_SOUND = "fire_alarm.ogg"
FONT = "arial.ttf"
CENTER_WIDTH = SCREEN_WIDTH / 2
CENTER_HEIGHT = SCREEN_HEIGHT / 2
CLOCK_WIDTH = 2 * SCREEN_WIDTH / 5
CLOCK_HEIGHT = SCREEN_HEIGHT / 3

TEXT_TIME_SIZE = int(CLOCK_HEIGHT)
TEXT_NOTI_SIZE = int(2 * CLOCK_HEIGHT / 6)
TEXT_TITLE_SIZE = int(CLOCK_HEIGHT / 2)

MOVE_DOWN_SCREEN_SIZE = 2*CLOCK_HEIGHT / 6
TIMER_ZONE = []
TIMER_ZONE.append(pygame.Rect(CLOCK_WIDTH / 8, CENTER_HEIGHT - CLOCK_HEIGHT / 2 + MOVE_DOWN_SCREEN_SIZE,
                    CLOCK_WIDTH,CLOCK_HEIGHT))
TIMER_ZONE.append(pygame.Rect(CENTER_WIDTH + CLOCK_WIDTH / 8, CENTER_HEIGHT - CLOCK_HEIGHT / 2 + MOVE_DOWN_SCREEN_SIZE,
                    CLOCK_WIDTH,CLOCK_HEIGHT))
NOTI_ZONE = []
NOTI_ZONE.append(pygame.Rect(CLOCK_WIDTH / 8, CENTER_HEIGHT - 2 * CLOCK_HEIGHT / 2 + MOVE_DOWN_SCREEN_SIZE,
                    CLOCK_WIDTH, CLOCK_HEIGHT / 2))
NOTI_ZONE.append(pygame.Rect(CENTER_WIDTH + CLOCK_WIDTH / 8, CENTER_HEIGHT - 2 * CLOCK_HEIGHT / 2 + MOVE_DOWN_SCREEN_SIZE,
                    CLOCK_WIDTH,CLOCK_HEIGHT / 2))
TITLE_ZONE = pygame.Rect(0,0,SCREEN_WIDTH, CLOCK_HEIGHT)
UPPER_NOTI_ZONE = pygame.Rect(0, CLOCK_HEIGHT, SCREEN_WIDTH, CENTER_HEIGHT - 2 * CLOCK_HEIGHT + MOVE_DOWN_SCREEN_SIZE)
BOTTOM_NOTI_ZONE = pygame.Rect(0, CENTER_HEIGHT + CLOCK_HEIGHT / 2 + MOVE_DOWN_SCREEN_SIZE,
                    SCREEN_WIDTH, CLOCK_HEIGHT / 2 - MOVE_DOWN_SCREEN_SIZE)

MOUSE_CODE_LEFT = 1
MOUSE_CODE_MIDDLE = 2
MOUSE_CODE_RIGHT = 3
MOUSE_CODE_SCROLL_UP = 4
MOUSE_CODE_SCROLL_DOWN = 5

class Running:
    def __init__(self):
        self.running = True
    def reset(self, to=False):
        self.running = to
    def get(self):
        return self.running

def set_text(screen, font, text, zone, text_color, background_color):
    text_rendered = font.render(text, True, text_color, background_color)
    text_rect = text_rendered.get_rect()
    text_rect.center = zone.center
    if text_rect.width > zone.width:
        text_rect.width=zone.width
    if text_rect.height>zone.height:
        text_rect.height=zone.height
    screen.blit(text_rendered, text_rect)

def set_text_timer(screen, timerid, text):
    set_text(screen, font, text, TIMER_ZONE[timerid - 1], TEXT_COLOR, TIMER_BACKGROUND_COLOR)

def set_text_noti(screen, timerid, text):
    font = pygame.font.Font(FONT, TEXT_NOTI_SIZE)
    set_text(screen, font, text, NOTI_ZONE[timerid - 1], TEXT_NOTI_COLOR, BACKGROUND_COLOR)

def alarm(stop = False):
    #timeout_sound = pygame.mixer.Sound("alarm.mp3")
    if not stop:
        timeout_sound = pygame.mixer.music.load(END_SOUND)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()
def get_time_text(seconds):
    if(seconds < 0):
        seconds = 0
    return "%d%d:%d%d"%(seconds / 600, seconds / 60 % 10,
                             seconds % 60 / 10, seconds % 60 % 10)

def timer_update(screen, timer, alarm_running):
    #prev time
    timer1 = -1
    timer2 = -1
    while True:
        try:
            cur_time1 = timer.get_time1_seconds(TIME_LIMIT)
            cur_time2 = timer.get_time2_seconds(TIME_LIMIT)
            #print("curtime1:",cur_time1)
            #print("curtime2:", cur_time2)

            if(cur_time1 != timer1):
                set_text_timer(screen, 1, get_time_text(cur_time1))
                timer1 = cur_time1
                if timer1 <= 0:
                    set_text_noti(screen, 1, "Time out")
                    alarm_running.reset()
                    return
            if(cur_time2 != timer2):
                set_text_timer(screen, 2, get_time_text(cur_time2))
                timer2 = cur_time2
                if timer2 <= 0:
                    set_text_noti(screen, 2, "Time out")
                    alarm_running.reset()
                    return
        except Exception as e:
            print("ha")
            print(e)
    print("heresg                 +")

def thread_sleep(running, seconds=3):
    time.sleep(seconds)
    running.reset()

#MAIN
pygame.init()
if not pygame.get_init():
    exit()
#create screen (window)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
icon_img = pygame.image.load(WINDOW_ICON)
pygame.display.set_icon(icon_img)
screen.fill(BACKGROUND_COLOR)

#set big title
font = pygame.font.Font(FONT, TEXT_TITLE_SIZE)
set_text(screen, font, WINDOW_TITLE, TITLE_ZONE, TITLE_COLOR, BACKGROUND_COLOR)

#draw zone for time
pygame.draw.rect(screen, TIMER_BACKGROUND_COLOR, TIMER_ZONE[0])
pygame.draw.rect(screen, TIMER_BACKGROUND_COLOR, TIMER_ZONE[1])

app_running = True
while app_running:
    #set font of time
    font = pygame.font.Font(FONT, TEXT_TIME_SIZE)
    #reset
    set_text_timer(screen, 1, get_time_text(TIME_LIMIT))
    set_text_timer(screen, 2, get_time_text(TIME_LIMIT))
    pygame.display.update()
    #wait to start
    running_ask = True
    while running_ask:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.MOUSEBUTTONDOWN and event.button == MOUSE_CODE_MIDDLE):
                running_ask = False
                app_running=False
                continue
            elif event.type == pygame.KEYDOWN or (event.type==pygame.MOUSEBUTTONDOWN and event.button != MOUSE_CODE_MIDDLE):
                running_ask = False
    if not app_running:
        break
    #must be object to pass into other thread
    alarm_running = Running()
    #another thread to manage timer display; main thread to check for switch turn
    timer = chess_timer.chess_timer()
    thread_update_time = Thread(target=timer_update, args=(screen, timer, alarm_running), daemon=True)
    thread_update_time.start()
    #main thread
    while alarm_running.get():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alarm_running.reset()
                app_running=False
                print("pygame quit 1")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    timer.change_turn()
                elif event.key == pygame.K_LEFT:
                    timer.change_turn(to_turn = 2)
                elif event.key == pygame.K_RIGHT:
                    timer.change_turn(to_turn = 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_CODE_LEFT:
                    timer.change_turn(to_turn = 2)
                elif event.button == MOUSE_CODE_RIGHT:
                    timer.change_turn(to_turn = 1)

        pygame.display.update()    
    print("Exited loop")
    pygame.display.update()
    del alarm_running
    if not app_running:
        break
    continuing = False
    #alarm-sleeping
    alarm()
    sleep_running = Running()
    sleep = Thread(target=thread_sleep, args=(sleep_running,), daemon=True)
    sleep.start()
    while(sleep_running.get()):
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.MOUSEBUTTONDOWN and event.button == MOUSE_CODE_MIDDLE):
                sleep_running.reset()
                app_running=False
            elif event.type==pygame.KEYDOWN or (event.type==pygame.MOUSEBUTTONDOWN and event.button != MOUSE_CODE_MIDDLE):
                sleep_running.reset()
                continuing = True

    alarm(stop = True)
    del sleep_running
    if not app_running:
        break
    #ask if continue
    if continuing:
        set_text_noti(screen, 1, "               ")
        set_text_noti(screen, 2, "               ")
        continue
    running_ask = True
    while running_ask and continuing==False:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.MOUSEBUTTONDOWN and event.button == MOUSE_CODE_MIDDLE):
                running_ask = False
                app_running=False
            elif event.type == pygame.KEYDOWN or (event.type==pygame.MOUSEBUTTONDOWN and event.button != MOUSE_CODE_MIDDLE):
                continuing=True

    set_text_noti(screen, 1, "               ")
    set_text_noti(screen, 2, "               ")


#end
del timer
pygame.quit() 
