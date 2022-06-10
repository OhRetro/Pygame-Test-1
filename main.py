#Pygame Test 1
#Originaly made on: 20-8-2021

import sys, os, time

try:
    import pygame
    from pygame.locals import *

except ImportError as e:
    raise e
    
#Game Class

class Game():
    def __init__(self, title="Game Name", version="Game Vesion", res:tuple=(None, None)):
        pygame.init()
        self.title = title
        self.version = version
        self.framerate = 60       
        self.screen = pygame.display.set_mode(res)
        pygame.display.set_caption(title)


    #Game Engine
    class Engine:
        def fps():
            return f"FPS: {round(clock.get_fps())}"         
  
    #Game Entity
    class Entity():
        def __init__(self, entity_type:str, pos_x:int, pos_y:int, vel_x:int, vel_y:int, is_playable:bool=False, entity_sprites_path:str=""):
            super().__init__()
            self.entity_type = entity_type
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.vel_x = vel_x
            self.vel_y = vel_y
            
            self.is_playable = is_playable
            
            self.entity_sprites_path = entity_sprites_path
            
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            
            self.facing_right = True
            self.facing_left = False
            
            self.idling = True
            self.running = False
            self.attacking = False
            
            #Pre Load Sprites
            self.idle_ = self.load_sprite("Idle")
            
        def load_sprite(self, name):
            temp_list = []
            for frames in range(len(os.listdir(f"./{self.entity_sprites_path}/{self.entity_type}/{name}/"))):
                frame = frames
                sprites = pygame.image.load(f"./{self.entity_sprites_path}/{self.entity_type}/{name}/{frame}.png")
                sprites = pygame.transform.scale(sprites, (sprites.get_width() * 3, sprites.get_height() * 3))
                temp_list.append(sprites)
            self.animation_list.append(temp_list)

            self.sprite = self.animation_list[self.action][self.frame_index]
            self.rect = self.sprite.get_rect()
            self.rect.center = (self.pos_x, self.pos_y)
        
        def update_frames(self):
            #Animations
            animation_cooldown = 100
            self.sprite = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                
                #Running
                if self.action == 1:
                    self.action = 0

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

                #Attacking
                if self.action in [2, 3, 4]:
                    self.attacking = False
                    self.idling = True
                    self.action = 0     

        def update_movements(self):
            #Controls
            if not self.is_playable:
                return 

            self.player_key_input_holding = pygame.key.get_pressed()

            if self.player_key_input_holding[pygame.K_z]:
                if not self.attacking and self.idling:
                    self.attacking = True
                    self.idling = False
                    self.frame_index = 0
                    #self.action = 2

                elif self.attacking and self.frame_index >= 4:
                    self.frame_index = 0
                    self.action += 1
                    
            if (self.player_key_input_holding[pygame.K_RIGHT] | self.player_key_input_holding[pygame.K_LEFT]) and not self.running:
                self.running = True
                self.idling = False

                if self.attacking:
                    return

                #self.action = 1 

                if self.player_key_input_holding[pygame.K_RIGHT]:
                    if not self.facing_right:
                        self.facing_right = True
                        self.facing_left = False
                    self.pos_x += self.vel_x * dt
                elif self.player_key_input_holding[pygame.K_LEFT]:
                    if not self.facing_left:
                        self.facing_right = False
                        self.facing_left = True
                    self.pos_x -= self.vel_x * dt      
                self.rect.center = (self.pos_x, self.pos_y)

                if self.pos_x >= 1285:
                    self.pos_x = 1280
                elif self.pos_x <= -5:
                    self.pos_x = 0

            if not self.player_key_input_holding[pygame.K_RIGHT | pygame.K_LEFT]:
                self.running = False
                self.idling = True

        def spawn(self):
            if self.facing_right:
                Game.screen.blit(self.sprite, self.rect)
            elif self.facing_left:
                Game.screen.blit(pygame.transform.flip(self.sprite ,True, False), self.rect)
          
        def update(self):
            self.update_frames()
            self.update_movements()
                            
        def debug(self):
            if self.facing_right: self.facing = "Right"
            elif self.facing_left: self.facing = "Left"
            
            if self.action == 0:
                self.action_debug = f"{self.action}(Idling)"
            elif self.action == 1:
                self.action_debug = f"{self.action}(Running)"
            elif self.action >= 2 and self.action <= 4:
                self.action_debug = f"{self.action}(Attacking{self.action - 1})"
            
            self.entity_pos_debug = f"X: {round(self.pos_x)}, Y: {round(self.pos_y)}"
            self.entity_info_debug = f"Entity type: '{self.entity_type}'|Action: {self.action_debug}|Facing: {self.facing}|Playable: {self.is_playable}"

    #Game Text
    class Text():
        def __init__(self, text, text_pos:tuple, text_color:tuple=(255,255,255)):
            self.text_pos = text_pos
                
            text_font = pygame.font.SysFont("monospace", 15)
            self.text_text = text_font.render(text, 1, text_color)
            Game.screen.blit(self.text_text, self.text_pos)
                        
        #Game Text List
        class List():            
            def __init__(self, texts:list, pos_x:int=10, pos_y:int=10):
                for text in texts:
                    self.text = Game.Text(text, (pos_x,pos_y))
                    pos_y += 15          

#Run Code
if __name__ == "__main__":
    try:
        #Run Game
        Game = Game("Pygame Test 1", "None", (1280, 720))
        
        clock = pygame.time.Clock()
        last_time = time.time()
    
        #Entities
        Player = Game.Entity("Player", 200, 600, 5, 0, True, "files")

        while True:   
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            Game.screen.fill((10,10,10))
            
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            Player.spawn()
            Player.debug()
            Player.update()

            Game.Text.List([Game.Engine.fps(), Player.entity_pos_debug, Player.entity_info_debug, f"Version: {Game.version}"])
            Game.Text.List([f"Idling: {Player.idling}", f"Running: {Player.running}", f"Attacking: {Player.attacking}"], pos_x=1000)
            Game.Text.List(["Left/Right to move", "Z to attack", "Esc to close"], pos_y=650)
            
            Game.Text("Player", (Player.pos_x-25, Player.pos_y-70))
           
            pygame.display.update()
            clock.tick(Game.framerate)

    except Exception as error:
        raise error