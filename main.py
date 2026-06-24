from graphics import Canvas 
import random 

'''
SuperRace game
This program is a racing game. When the game starts, the action is frozen, and the 
player is prompted to choose a side using the interactive dashboard at the 
bottom of the screen. Clicking the left side of the panel places a bet on the 
Red Team (top lane), while clicking the right side backs the Blue Team 
(bottom lane). Once a team is selected, the countdown ends and the race instantly 
starts.

To simulate a sense of high-speed travel down an endless highway, the road lines 
and fence text scroll continuously, looping back to the right edge as they move 
off-screen. Both racing cars move using a fair randomized speed logic, making the 
outcome unpredictable until the very last second. Near the end of the race, checkered 
flags appear, and the exact positions of the cars are evaluated the moment they 
cross the line to instantly display the winning team on the dashboard.
'''
    
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

# Background layout boundaries for sky (Vertical positions from top)
SKY_BOTTOM_LINE = 140

# Cloud generation settings
CLOUD_BASE_LEVEL = 150
CLOUD_WIDTH = 80
CLOUD_SPACING = 35

# Background layout boundaries for fence
FENCE_BOTTOM_LINE = 170
# Fence text reset boundaries for the infinite loop effect
TEXT_OFFSCREEN_LIMIT = -150
TEXT_TELEPORT_DISTANCE = 800

# Background layout boundaries for grass
HIGHER_GRASS_BOTTOM_LINE = 220
LOWER_GRASS_BOTTOM_LINE = 440

# Racetrack border pattern settings
HIGHER_CURB_BOTTOM_LINE = 230
LOWER_CURB_BOTTOM_LINE = 390
LOWER_CURB_TOP_LINE = 380 
STRIPE_WIDTH = 40

# Road line reset boundaries for the infinite loop effect
LINE_OFFSCREEN_LIMIT = -30
LINE_TELEPORT_DISTANCE = 640

# Race configuration
TOTAL_RACE_DISTANCE = 5000
WORLD_SPEED = 12
SLEEP_RATE = 40
END_GAME_DELAY = 5000

# Starting horizontal positions
CAR_START_POSITION = 135
INITIAL_FINISH_POSITION = 350

# Safe horizontal boundaries for the cars on the track
MIN_TRACK_LIMIT = 50
MAX_TRACK_LIMIT = 400

# The position where the finish line stops and triggers braking
FINISH_LINE_STOP_LIMIT = 280

# Starting brake speeds for both cars
TOP_CAR_BRAKE_SPEED = 7
BOTTOM_CAR_BRAKE_SPEED = 5

# Controls how fast the cars slow down 
BRAKE_DECELERATION_RATE = 6

# Distance before the end of the race to spawn the finish line (5000 - 80)
FINISH_SPAWN_TRIGGER = 80

# Visual alignment offsets for finish elements
FLAGS_INITIAL_MOVE = -105


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Draw static background environment
    draw_background(canvas) 

    # Create the text elements that will scroll along the fence 
    moving_fence_texts = draw_moving_text(canvas)
 
    # Draw broken lines in the middle of the road
    road_center_lines = draw_road_center_lines(canvas)

    # Spawn the racing cars (top lane and bottom lane)
    top_car_elements = draw_top_car(canvas)
    bottom_car_elements = draw_bottom_car(canvas)

    # Clear any accidental clicks recorded during window startup
    canvas.get_new_mouse_clicks()

    # Display the initial prompt and store the text reference
    info_text = update_panel_text(canvas, None, "CLICK YOUR TEAM!")
    player_choice = None

    # Interactive wait loop: game remains frozen until a team is selected
    while player_choice is None:
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            if click is not None:
                # Unpack the click tuple into separate X and Y coordinates
                click_x, click_y = click
                
                # Check if the click happened inside the betting panel region
                if click_y >= 440:
                    # Split the screen into Left (Red) and Right (Blue) zones
                    if click_x < CANVAS_WIDTH // 2:
                        player_choice = 'red'
                    else:
                        player_choice = 'blue'

        # Sleep briefly during the wait phase                
        canvas.sleep(SLEEP_RATE)

    # Update the prompt and add a short delay before the cars launch
    info_text = update_panel_text(canvas, info_text, "RACE IS ON!")
    canvas.sleep(500)
 
    # Track variables for the race progression (distance and state)
    race_distance = 0
    race_is_running = True
    brake_timer = 0

    # Current horizontal positions of both cars
    top_car_position = CAR_START_POSITION
    bottom_car_position = CAR_START_POSITION
 
    # Visual elements that will appear later during the race
    finish_flags = None

    # Current horizontal position of the finish line
    finish_line_position = INITIAL_FINISH_POSITION

    while True:
        if race_is_running:
            # Advance the race distance based on world speed
            race_distance += WORLD_SPEED

            # Move text on the fence to create an infinite scrolling effect
            for word in moving_fence_texts:
                canvas.move(word, -WORLD_SPEED, 0)
                # Get the current horizontal position of the word
                word_position = canvas.get_x(word)
                # If the text goes off_screen to the left, teleport it to the right
                if word_position < TEXT_OFFSCREEN_LIMIT:
                    canvas.move(word, TEXT_TELEPORT_DISTANCE, 0)
 
            # Move road center lines to create an infinite driving effect
            for line in road_center_lines:
                canvas.move(line, -WORLD_SPEED, 0)
                # Get the current horizontal position of the line
                line_position = canvas.get_x(line)
                # If the line goes off_screen to the left, teleport it to the right
                if line_position < LINE_OFFSCREEN_LIMIT:
                    canvas.move(line, LINE_TELEPORT_DISTANCE, 0)

            # Spawn the finish flags near the end of the race
            is_near_finish = race_distance >= (TOTAL_RACE_DISTANCE - FINISH_SPAWN_TRIGGER)
            if is_near_finish and finish_flags is None:
                # Create and position the finish flags
                finish_flags = draw_finish_flags(canvas)
                for flag in finish_flags:
                    canvas.move(flag, FLAGS_INITIAL_MOVE, 0)

                # Set the starting position of the finish line
                finish_line_position = INITIAL_FINISH_POSITION
    
            # Move the flags toward the cars
            if finish_flags is not None:
                for element in finish_flags:
                    canvas.move(element, -WORLD_SPEED, 0)
                finish_line_position -= WORLD_SPEED
            
            # Simulate random car movement 
            top_car_move = random.randint(-8, 9)
            bottom_car_move = random.randint(-8, 9)
            
            # Move top car if it stays within safe track boundaries
            is_top_car_safe = MIN_TRACK_LIMIT < (top_car_position + top_car_move) < MAX_TRACK_LIMIT
            if is_top_car_safe:
                for element in top_car_elements:
                    canvas.move(element, top_car_move, 0)
                top_car_position += top_car_move 

            # Move bottom car if it stays within safe track boundaries
            is_bottom_car_safe = MIN_TRACK_LIMIT < (bottom_car_position + bottom_car_move) < MAX_TRACK_LIMIT
            if is_bottom_car_safe:
                for element in bottom_car_elements:
                    canvas.move(element, bottom_car_move, 0)
                bottom_car_position += bottom_car_move
            
            # Check if the finish line has reached the cars to end the race
            if finish_flags is not None and finish_line_position <= FINISH_LINE_STOP_LIMIT:
                race_is_running = False

                # Determine the race outcome right at the finish line crossing
                if top_car_position > bottom_car_position:
                    result_text = "RED TEAM WON!"
                elif bottom_car_position > top_car_position:
                    result_text = "BLUE TEAM WON!"
                else:
                    result_text = "IT'S A DRAW!"

                # Instantly print the final race result on the dashboard

                update_panel_text(canvas, info_text, result_text)

        else:
            brake_timer += 1
            
            # Calculate declining speeds 
            top_car_final_speed = max(0, TOP_CAR_BRAKE_SPEED - (brake_timer // BRAKE_DECELERATION_RATE))
            bottom_car_final_speed = max(0, BOTTOM_CAR_BRAKE_SPEED - (brake_timer // BRAKE_DECELERATION_RATE))
            
            # Move top car at its braking speed
            for element in top_car_elements:
                canvas.move(element, top_car_final_speed, 0)
            # Move bottom car at its braking speed
            for element in bottom_car_elements:
                canvas.move(element, bottom_car_final_speed, 0)

            # Stop the main game loop completely when both cars hit 0 speed
            if top_car_final_speed == 0 and bottom_car_final_speed == 0:
                break

        # Pause to control the animation frame rate         
        canvas.sleep(SLEEP_RATE)

    # The race is finished and cars have stopped. Wait before closing the window.
    canvas.sleep(END_GAME_DELAY)


def draw_background(canvas):

    draw_sky(canvas)
    draw_clouds(canvas)
    draw_fence(canvas)

    draw_top_grass(canvas)
    draw_top_track_border(canvas)
    draw_racetrack(canvas)
    draw_bottom_track_border(canvas)
    draw_bottom_grass(canvas)
    draw_betting_panel(canvas)


def draw_sky(canvas):
    # Draw the blue sky background at the top of the canvas
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, SKY_BOTTOM_LINE, 'deepskyblue')

def draw_clouds(canvas):
    # Generates a row of simple random-height clouds across the sky
    # We start from -40 to ensure clouds cover the left edge of the screen
    for current_horizontal in range(-40, CANVAS_WIDTH, CLOUD_SPACING):
        # Generate a random top edge position for each cloud oval
        cloud_top_edge = random.randint(50, 90)

        canvas.create_oval(
            current_horizontal, 
            cloud_top_edge, 
            current_horizontal + CLOUD_WIDTH, 
            CLOUD_BASE_LEVEL, 
            'azure', 
            'azure'
        )

def draw_fence(canvas):
    # Draw a brown wooden fence line below the sky
    canvas.create_rectangle(0, SKY_BOTTOM_LINE, CANVAS_WIDTH, FENCE_BOTTOM_LINE, 'brown')

def draw_top_grass(canvas):
    # Draw the green grass area between the fence and the racetrack
    canvas.create_rectangle(0, FENCE_BOTTOM_LINE, CANVAS_WIDTH, HIGHER_CURB_BOTTOM_LINE, 'green')

def draw_top_track_border(canvas):

    # Draws a checkered brown and white border line above the racetrack
    for stripe in range(0, CANVAS_WIDTH, STRIPE_WIDTH):
        # Determine the stripe number to alternate colors
        stripe_number = stripe // STRIPE_WIDTH
        
        if stripe_number % 2 == 0:
            current_color = 'brown'
        else:
            current_color = 'white'
        
        # Draw each individual stripe of the border
        canvas.create_rectangle(
            stripe, 
            HIGHER_GRASS_BOTTOM_LINE, 
            stripe + STRIPE_WIDTH, 
            HIGHER_CURB_BOTTOM_LINE, 
            current_color, 
            'brown'
        )

def draw_racetrack(canvas):
    # Draw the gray area of the racing track
    canvas.create_rectangle(0, HIGHER_CURB_BOTTOM_LINE, CANVAS_WIDTH, LOWER_CURB_TOP_LINE, 'grey') 

def draw_bottom_track_border(canvas):
    # Draw a checkered brown and white curb line below the racetrack
    for stripe in range(0, CANVAS_WIDTH, STRIPE_WIDTH):
        stripe_number = stripe // STRIPE_WIDTH
        if stripe_number % 2 == 0:
            current_color = 'brown'
        else:
            current_color = 'white'
        
        # Draw each individual stripe of the lower curb
        canvas.create_rectangle(
            stripe, 
            LOWER_CURB_TOP_LINE, 
            stripe + STRIPE_WIDTH, 
            LOWER_CURB_BOTTOM_LINE, 
            current_color, 
            'brown'
        )

def draw_bottom_grass(canvas):
    # Draw the green grass area at the bottom of the screen
    canvas.create_rectangle(0, LOWER_CURB_BOTTOM_LINE, CANVAS_WIDTH, LOWER_GRASS_BOTTOM_LINE, 'green')

def draw_road_center_lines(canvas):
    # Generates a list of broken white lines in the middle of the road
    road_lines = []
    for line in range(0, 640, 80):
        single_line = canvas.create_line(line, 305, line + 30, 305, 'white')
        road_lines.append(single_line)
    return road_lines

def draw_moving_text(canvas):
    # Generate a list of scrolling text lines for the fence
    text_lines = []
    for num in range(8):
        line_position = -150 + (num * 100)
        text = canvas.create_text(
            line_position, 148, 
            text='SuperRace  >>>', 
            font='Impact', 
            font_size=15, 
            color='lime'
        )
        text_lines.append(text)
    return text_lines

def draw_finish_flags(canvas):
    # Generates a detailed list of visual elements 
    #for two checkered finish flags
    flags_list = []
    for i in range(2):
        left_flag = canvas.create_line(445 + i, 220, 445 + i, 175, 'orange')
        right_flag = canvas.create_line(470 + i, 220, 470 + i, 175, 'orange')
        flags_list.extend([left_flag, right_flag])
    
    #left flag
    for i in range(3):
        for j in range(3):
            hor_step = j * 10
            ver_step = i * 10
            if (i + j) % 2 == 0:
                color = 'blue'
            else:
                color = 'white'

            left_rect = canvas.create_rectangle(
                415 + hor_step, 
                175 + ver_step, 
                425 + hor_step, 
                185 + ver_step, 
                color
            )
            flags_list.append(left_rect) 
            
    # right flag
    for i in range(3):
        for j in range(3):
            hor_step = j * 10
            ver_step = i * 10
            if (i + j) % 2 == 0:
                color = 'red'
            else:
                color = 'white'

            right_rect = canvas.create_rectangle(
                470 + hor_step, 
                175 + ver_step, 
                480 + hor_step, 
                185 + ver_step, 
                color
            )
            flags_list.append(right_rect)

    return flags_list


def draw_top_car(canvas):

    # Generates all visual elements for the top racing car (Red)
    return [
    # Driver's helmet
    canvas.create_oval(61, 242, 77, 258, 'black'),
    
    # Main car body
    canvas.create_polygon(
    15, 280,   #bumper bottom
    15, 255,   # bumper top
    55, 235,   # roof (highest point)
    70, 255,   # Windshield to hood transition
    90, 247,   # Front wing scoop
    135, 275,  # Front nose top
    135, 280,  # Front nose bottom
    color='red'
    ),
    # Decorative white stripe on the side
    canvas.create_rectangle(15, 274, 134, 276, 'white'),
    
    # rear wheel
    canvas.create_oval(20, 260, 52, 292, 'black'),
    canvas.create_oval(28, 268, 44, 284, 'white'),
    
    # Front wheel 
    canvas.create_oval(90, 260, 122, 292, 'black'),
    canvas.create_oval(98, 268, 114, 284, 'white', 'white')
    ]


def draw_bottom_car(canvas):

    return [
    # Driver's helmet
    canvas.create_oval(62, 312, 80, 328, 'black'),
    
    # Main car body
    canvas.create_polygon(
        15, 350,   # Rear bumper bottom
        15, 325,   # Rear bumper top
        55, 305,   # roof (highest point)
        70, 325,   # Windshield to hood transition
        90, 317,   # Front wing scoop
        135, 345,  # Front nose top
        135, 350,  # Front nose bottom
        color="blue"
    ),
    
    # Decorative white stripe on the side
    canvas.create_rectangle(15, 344, 135, 346, 'white'),
    
    # Rear wheel 
    canvas.create_oval(20, 330, 52, 362, 'black'),       
    canvas.create_oval(28, 338, 44, 354, 'white', 'white'),
    # Front wheel
    canvas.create_oval(90, 330, 122, 362, 'black'),
    canvas.create_oval(98, 338, 114, 354, 'white', 'white')
    ]

def draw_betting_panel(canvas):
    canvas.create_image_with_size(0, 440, 600, 160, 'dashboard.png')


def update_panel_text(canvas, old_text_obj, new_string):
    """
    Safely updates the text displayed on the betting dashboard.
    If an older text object exists, it is moved off-screen to prevent 
    overlapping layers, and a new text object is created at the center.
    """
    # Horizontal and vertical coordinates for the panel text window
    text_x = 230  
    text_y = 570  

    if old_text_obj is not None:
        # Move the old text far off-screen to avoid visual overlapping
        canvas.delete(old_text_obj)
    
    # Create and return the new text element within the dashboard window
    return canvas.create_text(
        text_x, 
        text_y, 
        text=new_string, 
        font='Arial', 
        font_size=13, 
        color='lime'
    )


if __name__ == '__main__':
    main()
