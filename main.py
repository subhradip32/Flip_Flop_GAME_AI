import neat.population
import neat.reproduction
import pygame 
import neat 
import pickle
import os 
import random
pygame.font.init()

# Creating constants 
WIN_WIDTH = 500 
WIN_HEIGHT = 800
#loading Iamges 
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',"bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',"bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',"bird3.png"))),
            ]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',"pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',"base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',"bg.png")))

STA_FONT = pygame.font.SysFont("comicsans",50)


class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.velocity = -10.5 #In pygame -ve means the top and backward and +ve is the bottom and forward 
        self.tick_count = 0 
        self.height = self.y
    
    def move(self):#every single frame 
        self.tick_count = self.tick_count + 1 
        d = self.velocity * self.tick_count + 1.5 * self.tick_count**2
        #setting the terminal velocity 
        if d >= 16:  
            d = 16
        if d < 0: 
            d -= 2
        self.y = self.y + d 

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.MAX_ROTATION

    def draw(self, win):
        self.img_count += 1

        # Animation sequence
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Adjust the image based on tilt without breaking the animation
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2  # Keeps the animation state in sync

        # Rotate the image
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    

class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self,x):
        self.x = x 
        self.height = 0
        
        self.top = 0
        self.bottom = 0 
        self.PIPE_BOTTOM = PIPE_IMAGE
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self,win):
        win.blit(self.PIPE_TOP , (self.x,self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom) )

    #pixel perfect collison 
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x,self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True
        return False 
    
class Base: 
    VEL = 5
    WIDTH = BASE_IMAGE.get_width()
    IMG = BASE_IMAGE

    def __init__(self,y):
        self.y = y 
        self.x1 = 0
        self.x2 = self.WIDTH 
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL 

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y)) 
        win.blit(self.IMG,(self.x2,self.y)) 

def draw_window(win,birds,pipes,base,score): 
    win.blit(BG_IMAGE,(0,0))
    
    for pipe in pipes: 
        pipe.draw(win) 
    
    base.draw(win) 
    text = STA_FONT.render(f"Score: {str(score)}", 1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))

    for bird in birds:
        bird.draw(win) 
    pygame.display.update()


def save_genome(genome, filename):
    with open(filename, 'wb') as f:
        pickle.dump(genome, f)

def load_genome(filename):
    with open(filename, 'rb') as f:
        genome = pickle.load(f)
    return genome

#converted main function to act as the fitness function for the game 
def main(genomes,config):
    nets = []
    ge = []
    birds = []
    
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)


    base = Base(730)
    pipes = [Pipe(700)]

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    
    Score = 0 
    clock = pygame.time.Clock()
    run = True
    while run: 
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                save_genome(max(ge, key=lambda g: g.fitness), 'best_genome.pkl')
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if len(birds) > 0 :
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1  
        else:
            run = False
            break

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1 

            outputs = nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].height), abs(bird.y-pipes[pipe_ind].bottom)))
            if outputs[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    
            
                if not pipe.passed and pipe.x < bird.x: 
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()
        
        if add_pipe: 
            Score += 1
            for g in ge:
                g.fitness += 5 
            pipes.append(Pipe(700))
        
        for r in rem:
            pipes.remove(r)

        for x,bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        bird.move()
        base.move()
        draw_window(win,birds ,pipes,base,Score)



def train(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    p = neat.Population(config)
    
    #optional 
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(main,50)

def test(config_path,GENOME):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    net = neat.nn.FeedForwardNetwork.create(GENOME, config)

    birds = [Bird(230, 350)]

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    score = 0
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        for bird in birds:
            bird.move()
            output = net.activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(birds[0]):
                run = False
                break

            if not pipe.passed and pipe.x < birds[0].x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if birds[0].y + birds[0].img.get_height() >= 730 or birds[0].y < 0:
            run = False

        base.move()
        draw_window(win, birds, pipes, base, score)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")

    #Train the best model 
    train(config_path)
    
    #using the best model 
    test(config_path,load_genome("best_genome.pkl"))
