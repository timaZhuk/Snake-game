from tkinter import *
import random 

#-------assign CONSTANTS----------
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 90
SPACE_SIZE = 50 # size of snake parts or food
BODY_PARTS = 3 # length of snake(3-body parts)
SNAKE_COLOR = '#0335fc' 
FOOD_COLOR = '#fc5e03'
BACKGROUND_COLLOR = '#998f26'
#-------------------------------------



#-----classes---------------
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        #draw the snake (initial position)
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0]) # snake appears at the left-top corner
        # create the parts of snake and add to list of squares
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')
            self.squares.append(square) 


class Food:
    def __init__(self):

        # define random position on our Game board (in px)
        x = random.randint(0, int(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE

        self.coordinates = [x,y]
        #ceate object food (x_0,y_0, x_end, y_end)
        canvas.create_oval(x,y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")


#---------------------functions-----------------
def next_turn(snake, food):
    x,y = snake.coordinates[0] # head of snake

    if direction == 'up':
        y -=SPACE_SIZE
    elif direction == 'down':
        y +=SPACE_SIZE

    elif direction == 'left':
        x -=SPACE_SIZE
    elif direction == 'right':
        x +=SPACE_SIZE
    
    #update the shake's head position , insert(index, (x,y)-coordinates)
    snake.coordinates.insert(0,(x,y))

    # draw snake's head new position
    square = canvas.create_rectangle(x,y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)
    # update the Snake squares list
    snake.squares.insert(0, square) 

    if x == food.coordinates[0] and y==food.coordinates[1]:
        global score
        score += 1
        label.config(text='Score: {}'.format(score))
        #delete food object
        canvas.delete('food')
        # and create again Food object
        food = Food()
    else:
        # we delete snake part only if sanke doesn't eat food
        # delete last coordinates of snake movements (we don't want to draw it)
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1]) # on board
        del snake.squares[-1] # in list actually
    
    #collisions with body of snake
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED,next_turn, snake, food)

def change_direction(new_direction):
    #access to global variable
    global direction
    #if statements 
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction



def check_collisions(snake):
    x,y = snake.coordinates[0]

    if x<0 or x>=GAME_WIDTH:
        print("Game Over")
        return True
    elif y<0 or y>=GAME_HEIGHT:
        print("Game Over")
        return True
    for body_parts in snake.coordinates[1:]:
        if x == body_parts[0] and y == body_parts[1]:
            return True
    
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
                     font=('consolas', 60),text="Game Over", fill='red', tag='gameover'   )

#-------------Create Game Window--------------------
window = Tk()
window.title('Snake Game')
window.resizable(False, False) # if we won't change size of game window

#---initial parameters
score = 0
direction = 'down'

#---create Label for scores 
label = Label(window, text='Score: {}'.format(score), font=('consolas', 40))
label.pack() # add to window

#------creating canvas object for game bord (inside put widow object)
canvas = Canvas(window, bg=BACKGROUND_COLLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# -------------we want our game window will be at the centre of screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2)-(window_width/2))
y = int((screen_height/2)-(window_height/1.5))

window.geometry(f'{window_width}x{window_height}+{x}+{y}')
#--------------------------------------------------------------
# add left arrow key
window.bind('<Left>', lambda event:change_direction('left'))
window.bind('<Right>', lambda event:change_direction('right'))
window.bind('<Up>', lambda event:change_direction('up'))
window.bind('<Down>', lambda event:change_direction('down'))





#--------create objects (Snake and Food)--------------
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
