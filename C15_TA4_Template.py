import pygame
import time
from firebase import firebase

# Create a game screen and set its title 
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Car Racing Game")

# Teacher Activity 1- Step 1: Replace databse URL with the database created in TA1
db = firebase.FirebaseApplication("CAR RACING DATABASE LINK", None)

def db_get_data(count):
   all_player = []
   for i in range(1,count+1):
       all_player.append(db.get("",i))
   return all_player
   
class Player:
    # Define the __init__ method with properties- self, num, name, xloc, yloc
    def __init__(self, num, name, xloc, yloc):
        pygame.init()
        self.name = name
        self.xloc = xloc
        self.yloc = yloc
        self.num = num
       
    def image_load(self, location, width, height):
        img = pygame.image.load(location).convert_alpha()
        img_scaled = pygame.transform.smoothscale(img,(width,height))
        return img_scaled
    
    def player_name(self, position):
        font = pygame.font.Font(None, 30)
        text = font.render(self.name, 1, (0, 255,255))
        screen.blit(text, position)
        
    def text_display(size,text,r,g,b,x,y):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, (r,g,b))
        screen.blit(text, (x,y))

    # Method to update time field in database
    def time_update(self,time):
        self.time = time
        
    # Method to update player data in database 
    def db_update(self):
        # The player data fileds to be added to database is given as a dictionary
         data = {"name":self.name,
                 "x":self.xloc,
                 "y":self.yloc,
                 "time":self.time}
         # The .put() function will add the data to database, "num" is the playercount value.
         db.put("",self.num, data)
        
# The .get() function retrieves the specific firld data from the database 
player_count = db.get("","PlayerCount")
print(player_count)

# If player count is less than 3 we will allow a new player creation and to participlate in the game else a warning is shown
if player_count < 3:
    player_count += 1
    db.put("","PlayerCount", player_count)
    
    bgy = 0
    counter = 0
    
    # Create a player1 object
    player1 = Player(player_count,"Daniel", 140, 450)
    
    carryOn = True
    t1 = time.time()
    
    while carryOn:
        bgImg = pygame.image.load("road.png").convert_alpha()
        bgImg_scaled = pygame.transform.smoothscale(bgImg,(650,600))
        screen.blit(bgImg_scaled,(0,0))
        
        yellow_car = player1.image_load("yellow_car.png", 230, 140)
        player1.player_name((player1.xloc+90, player1.yloc+130))
        
        # Update player location
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.yloc -= 50
                    bgy -= 10
                if event.key == pygame.K_DOWN:
                    player1.yloc += 50
                    bgy += 10
                if event.key==pygame.K_RIGHT:
                    player1.xloc += 50
                if event.key==pygame.K_LEFT:
                    player1.xloc -= 50   
        
        if player1.yloc <= 30:
            bgy = 0
            player1.yloc = 450
            counter += 1
    
        t2 = time.time()
        game_time = t2-t1
        game_time = round(game_time, 2)
        
        # Update time of player object by using time_update() method
        player1.time_update(game_time)
        
        # Display game time elapsed
        # Using player object specific game time here
        Player.text_display(35,"TIME ELAPSED: " + str(player1.time)+ "seconds", 0,255,255,130,15)
        players = db_get_data(player_count)
        
        # Display finish line after 1 iteration of game loop
        # Check if "counter" is equal to 1        
        if counter == 1:
            # Create and draw the finish line white-colored rectangle at (x,y)=(95, 40) with width=400 and height=30
            finish_line = pygame.Rect(95,40,400,30)
            pygame.draw.rect(screen,(255,255,255),finish_line)
            Player.text_display(40, "----------FINISH----------", 255,0,0,160,45)
            pygame.display.flip()
        
            # End the game loop after displaying finish line
            pygame.time.wait(3000)
            screen.fill((0,100,200))  
            # Using player object specific game time here
            texty = 100
            player_name = []
            player_time = []
            
            # Teacher Activity 4- Step 2: Explain the following code in for loop
            for i in players:
                Player.text_display(40, i["name"]+": "+str(round(i["time"],2))+ " seconds",255,255,255,140,texty)       
                texty += 100     
                # Determine the winner based on time consumed
                player_name.append(i["name"])
                player_time.append(round(i["time"],2))
                time_dict = (dict(zip(player_name, player_time)))
                key_list = list(time_dict.keys())
                val_list = list(time_dict.values())
                position = val_list.index(min(time_dict.values()))
                winner = key_list[position]
                pygame.display.flip()
            # Display the winner
            Player.text_display(40,"Winner is "+ winner, 255,255,0,140,texty)
            pygame.display.flip()
            pygame.time.wait(6000)
            # Break out of 'while' game loop
            break
        
        screen.blit(yellow_car, (player1.xloc, player1.yloc))
        player1.db_update()
        pygame.display.flip()
    pygame.quit()
else:
    # If there are 3 players in the game already then display Looby full message in console.
    print("LOBBY FULL! GAME CANNOT BE STARTED!")
    pygame.quit()
    
