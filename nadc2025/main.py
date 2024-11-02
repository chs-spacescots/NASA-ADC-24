import os
import platform
from ursina import *

try:
    import libdata as data
    import libui as ui
except ModuleNotFoundError:
    from nadc2025 import libdata as data
    from nadc2025 import libui as ui
except Exception as e:
    print("BIG OOPSY DOOPSIE IN IMPORTS!!")
    print(repr(e))

#load & read data
data.init()

# Initialize the Ursina application
app = Ursina()

# Set up the camera
EditorCamera()
# camera.look_at(Vec3(0, 0, 0))
# camera.start_position = Vec3(0, 0, -100)# Vec3(0, 0, 0)
# camera.position = Vec3(0, 0, 0)# Vec3(0, 0, 0)


# Create a mesh from the trajectory
data.wait_until_ready("trajectory")
trajectory_mesh = Entity(
    model=Mesh(vertices=data.trajectory_points, mode='line', thickness=1),
    color=color.blue
)

# Add origin and axis indicators
Entity(model='cube', color=color.red,
       scale=(.1, .1, .1), position=(0, 0, 0))  # Origin
Entity(model='cube', color=color.green, scale=(
    50, .1, .1), position=(25, 0, 0))  # X-axis
Entity(model='cube', color=color.blue,
       scale=(.1, 50, .1), position=(0, 25, 0))  # Y-axis
Entity(model='cube', color=color.white,
       scale=(.1, .1, 50), position=(0, 0, 25))  # Z-axis

# Sphere that moves along the trajectory
mark = Entity(model='sphere', color=color.red, scale=2)
mark.position = data.trajectory_points[0]


currentIndex=0
def update_sphere_position(perc):
    global currentIndex

    maxIndex = len(data.trajectory_points)-1
    currentIndex = int(perc * maxIndex)

    out = slerp(data.trajectory_points[currentIndex], data.trajectory_points[min(currentIndex+1,maxIndex)], perc)

    mark.position = out


# video stats
DURATION_SEC = 120
speed = 0
current_frac = 0

def step_frame(dt):
    global current_frac, speed, DURATION_SEC
    current_frac += speed/DURATION_SEC * dt
    current_frac = clamp(current_frac, 0, 1)

# video buttons
def play():
    global speed, camera
    if speed < 0:
        speed = 1
    else:
        speed += .5

def rev():
    global speed
    if speed > 0:
        speed = -1
    else:
        speed -= .5

def pause():
    global speed
    speed = 0



ui.add_elements([
    Text(
        text="TL",
        position=(-.5, .5),origin=(-.5, .5),
        scale=1,
        color=color.red,
        alpha=0.9
    ),
    Text(
        text="TR",
        position=(.5, .5),origin=(.5, .5),
        scale=1,
        color=color.red,
        alpha=0.9
    ),
    Text(
        text="BL",
        position=(-.5, -.5),origin=(-.5, -.5),
        scale=1,
        color=color.red,
        alpha=0.9
    ),
    Text(
        text="BR",
        position=(.5, -.5),origin=(.5, -.5),
        scale=1,
        color=color.red,
        alpha=0.9
    ),
])

# Play button
ui.add_elements([
    Button(
        text='Play',
        position=(-.3, -.2),
        text_size=ui.FONTSIZE_SMALL,
        scale=.1,
        color=color.black, text_color=color.green,
        on_click=play
    ),
    Button(
        text='Stop',
        position=(-.04, -.2),
        text_size=ui.FONTSIZE_SMALL,
        scale=.1,
        color=color.black, text_color=color.orange,
        on_click = pause
    ),
    Button(
        text='Rev',
        position=(.12, -.2),
        text_size=ui.FONTSIZE_SMALL,
        scale=.1,
        color=color.black, text_color=color.red,
        on_click = rev
    )
], parent=camera.ui)
# reverse_button.on_click = rev

# Instructions for dumbos
instructions_text = ui.add_element(Text(
    text="Hold right mouse to rotate\nWASD to move the camera while rotating\nCommand+Q to quit",
    position=(-.3, .2),
    color=color.white,
    alpha=0.9
))

info_text = ui.add_element(Text(
    text="Thrusting: ???\nTIME",
    position=(-.02, .022),
    text_size=ui.FONTSIZE_SMALL,
    color=color.white,
    alpha=0.9
))

thrusting=False
data.wait_until_ready("time")
def update_info(textE,thrusting):
    if currentIndex!=0 and data.mass[currentIndex]!=data.mass[currentIndex-1]:
        thrusting=True
    if thrusting and data.mass[currentIndex]==data.mass[currentIndex-1]:
        thrusting=False

    if thrusting:
        textE.text=f"Thrusting: YES {data.mass[currentIndex]}\n{int(data.time_min[currentIndex])}:{int(data.time_sec[currentIndex]%60)}"
        textE.color=color.green
    else:
        textE.text=f"Thrusting: NO {data.mass[currentIndex]}\n{int(data.time_min[currentIndex])}:{int(data.time_sec[currentIndex]%60)}"
        textE.color=color.black

# Run the application
ui.refit()
while True:
    # v+=1/60 * time.dt # one minute to completion.
    step_frame(time.dt)
    update_sphere_position(current_frac)
    update_info(info_text,thrusting)

    app.step()
