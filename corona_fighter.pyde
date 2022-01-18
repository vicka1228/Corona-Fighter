add_library('minim')
import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1000
HEIGHT = 720

    
class Creature:
    
    def __init__(self, x, y, r,img, w, h):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img)
        self.img_w = w
        self.img_h = h
            
    def display(self):
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)
        
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5
    
        
class Scientist(Creature):
    
    def __init__(self, x, y, r, img, w, h, num_frames):
       Creature.__init__(self, x, y, r, img, w, h)
       self.num_frames = num_frames
       self.frame = 0
       self.key_handler = {LEFT:False, RIGHT:False}
       self.health = 150
       self.hit_sound = player.loadFile(path + "/sounds/hit.wav")
       self.object_sound = player.loadFile(path + "/sounds/object.wav")
        
    def update(self):
        #For left and right movement
        if self.key_handler[LEFT] == True and self.x - self.r > 250:
            self.vx = -5
        
        elif self.key_handler[RIGHT] == True and self.x + self.r < 750:
            self.vx = 5
        
        else:
            self.vx = 0
        
        self.y += self.vy
        self.x += self.vx
        
        #Collision between scientist and virus
        for v in game.viruses:
            if self.distance(v) < self.r + v.r :
                self.health -= 10
                game.timer -= 1
                game.viruses.remove(v)
                self.hit_sound.rewind()
                self.hit_sound.play()
                
        for v in game.movingviruses:
            if self.distance(v) < self.r + v.r :
                self.health -= 10
                game.timer -= 1
                game.movingviruses.remove(v)
                self.hit_sound.rewind()
                self.hit_sound.play()  
            
        #Scientist picking up objects            
        for c in game.objects:
            if self.distance(c) <= self.r + c.r:
                game.objects.remove(c)
                if (self.health + 2) < 150 :
                    self.health += 2
                else:
                    while self.health < 150:
                        self.health += 1
                self.object_sound.rewind()
                self.object_sound.play()
        
        #For moving between frames at a slower rate        
        if frameCount % 5 == 0:
            self.frame = (self.frame + 1) % self.num_frames
        
    def display(self):
        self.update()
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
     
       
class Virus(Creature):
    
    def __init__(self, x, y, r, img, w, h):
       Creature.__init__(self, x, y, r, img, w, h)
       
    def update(self):
        self.y += 2
       
    def display(self):
        self.update()
        Creature.display(self)
        
    
class MovingVirus(Virus):
    
    def __init__(self, x, y, r, img, w, h, ll, rl):
        Virus.__init__(self, x, y, r, img, w, h)
        self.vx = random.randint(1, 5)
        self.dir = random.choice([LEFT, RIGHT])
        self.ll = ll
        self.rl = rl
        
        if self.dir == LEFT:
            self.vx *= -1
     
            
    def update(self):
        #For left and right movement between the road limits
        self.x += self.vx
        if self.x < self.ll:
            self.vx *= -1
            self.dir = RIGHT
        elif self.x > self.rl:
            self.vx *= -1
            self.dir = LEFT
            
        self.y += 2
    
    def display(self):
        self.update()  
        Virus.display(self) 
       
class Object:
    
    def __init__(self, x, y, r, img, w, h):
        self.x = x
        self.y = y
        self.r = r
        self.img = loadImage(path + "/images/" + img)
        self.img_w = w
        self.img_h = h
        
    def update(self):
        self.y += 2
        
    def display(self):
        self.update()
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)
        
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5
    
class Game:
    
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.scientist = Scientist(500, 500, 57, "Scientist.png", 100, 140, 4)
        self.objects = []
        self.viruses = []
        self.movingviruses = []
        self.health_percentage = 100
        self.game_over = False
        self.timer = 65
        self.object_options = ["mask.png","sanitiser.png"]
        self.road = {"img": loadImage(path + "/images/road.png"), "w": 500, "h": 613}
        self.roadheight = self.road["h"]
        self.count = 1
        self.finishline_y = -2600
        self.finishline = loadImage(path + "/images/finishline.png")
        self.background_sound = player.loadFile(path + "/sounds/retro.mp3")
        self.background_sound.rewind()
        self.background_sound.loop()
        self.lab_y = -2975
        self.lab = loadImage(path + "/images/lab.png")

        #For intialising the two different types of objects
        for o in range(30):
            choice = self.object_options[random.randint(0,1)]
            if choice == "mask.png" :
                w = 70
                h = 45
            else:
                w = 34
                h = 60
        
            self.objects.append(Object(random.randint(275,725), random.randint(-5200,695), 25, choice, w, h))
            
            #To make sure objects don't overlap
            for ob in self.objects:
                if len(self.objects) > 1 and ob != self.objects[-1] and ob.distance(self.objects[-1]) < 50 :
                    while ob.distance(self.objects[-1]) < 50:
                        self.objects.pop()
                        self.objects.append(Object(random.randint(275,725), random.randint(-5200,695), 25, choice, w, h))
         
        #For intialising the two different types of viruses            
        for v in range(30):
            self.viruses.append(Virus(random.randint(275,725), random.randint(-5200,690), 30, "virus2.png", 120, 120))
            
            #To make sure viruses don't overlap
            for ob in self.viruses:
                if len(self.viruses) > 1 and ob != self.viruses[-1] and ob.distance(self.viruses[-1]) < 60 :
                    while ob.distance(self.viruses[-1]) < 60:
                        self.viruses.pop()
                        self.viruses.append(Virus(random.randint(275,725), random.randint(-5200,690), 30, "virus2.png", 120, 120))
                    
        for mv in range(20):
            self.movingviruses.append(MovingVirus(random.randint(280,720), random.randint(-12000,690), 30, "virus1.png", 120, 120, 280, 720))
            
            #To make sure viruses don't overlap
            for ob in self.movingviruses:
                if len(self.movingviruses) > 1 and ob != self.movingviruses[-1] and ob.distance(self.movingviruses[-1]) < 60 :
                    while ob.distance(self.movingviruses[-1]) < 60:
                        self.movingviruses.pop()
                        self.movingviruses.append(MovingVirus(random.randint(275,725), random.randint(-12000,690), 30, "virus1.png", 120, 120, 280, 720)) 
                        
                        
        
    def display(self):
        
        #Timer countdown
        if frameCount % 60 == 0:
            self.timer -= 1
            
        #End Screens
        if self.scientist.y == self.finishline_y + 52:
            background(0,0,0)
            fill(255,255,255)
            textSize(60)
            text("Congratulations!", 275, 300)
            text("You saved the world!", 240, 365)
            textSize(30)
            text("Click to play again", 365, 435)
            self.background_sound.pause()
            self.game_over = True
            return
        if self.scientist.health <= 0 or self.timer <= 0:
            background(0,0,0)
            fill(255,255,255)
            textSize(100)
            text("Game Over!", 245, 310)
            textSize(30)
            text("Click to play again", 365, 415)
            self.background_sound.pause()
            self.game_over = True
            return
        
        roadtop = self.h - self.roadheight
        image(self.road["img"], 250, roadtop, 500, self.road["h"], 0, 0, self.road["w"], self.road["h"])
        image(self.road["img"], 250, self.road["h"] - (self.h - roadtop), 500, self.h - roadtop, 0, self.road["h"] - (self.h - roadtop), 500, self.road["h"])
        roadheight = (self.road["h"] * self.count) % self.h
        self.count += 1
        
        #Object/Virus display
        for o in self.objects:
            o.display()
        for v in self.viruses:
            v.display()
        for mv in self.movingviruses:
            mv.display()
            
        image(self.finishline, 250, self.finishline_y, 500, 52)
        self.finishline_y += 1
        
        image(self.lab, 100, self.lab_y, 800, 500)
        self.lab_y += 1
        
        #To display health bar
        fill(255, 255, 255)
        textSize(20)
        text("Health: " , 780, 100)
        self.health_percentage = int((self.scientist.health * 100) / 150.0 * 100) / 100.0
        noStroke()
        
        #To change colour depending on health
        if self.health_percentage >= 50:
            fill(0, 250, 0)
        elif self.health_percentage >= 20:
            fill(255, 255, 0)    
        else: 
            fill(255, 0, 0)
        rect(780, 125, self.scientist.health, 25)
        noFill()
        strokeWeight(5)
        stroke(255, 255, 255)
        rect(780, 125, 150, 25)
        fill(255, 255, 255)
        textSize(15)
        text(str(self.health_percentage) + "%", 935, 140)
        
        #To display timer
        fill(255, 255, 255)
        textSize(20)
        text("Time: ", 780, 200)
        textSize(25)
        text(str(self.timer) , 780, 225)
        
        self.scientist.display()
    
    
game = Game(WIDTH, HEIGHT)
 
def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    noStroke()
    fill(0, 0, 0)
    rect(0,0,250,720)
    rect(750,0,1000,720)
    game.display()
    
def mouseClicked():
    global game
    if game.game_over == True:
        game = Game(WIDTH, HEIGHT)

def keyPressed():
    if keyCode == LEFT:
        game.scientist.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.scientist.key_handler[RIGHT] = True
        
def keyReleased():
    if keyCode == LEFT:
        game.scientist.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.scientist.key_handler[RIGHT] = False
