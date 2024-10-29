import os
import platform
import pandas as pd
from ursina import *

# Load the dataset
data = pd.read_csv(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'dataset.csv'))

# Extract the position coordinates
x = data['Rx(km)[J2000-EARTH]']
y = data['Ry(km)[J2000-EARTH]']
z = data['Rz(km)[J2000-EARTH]']

# Initialize the Ursina application
app = Ursina()

# Set up the camera
EditorCamera()
# camera.look_at(Vec3(0, 0, 0))
# camera.start_position = Vec3(0, 0, -100)# Vec3(0, 0, 0)
# camera.position = Vec3(0, 0, 0)# Vec3(0, 0, 0)


# Create an entity for the trajectory
trajectory_points = []
for i in range(len(x)):
    trajectory_points.append(Vec3(x[i], y[i], z[i])/1000)  # 1u = 1km

# Create a mesh for the trajectory
trajectory_mesh = Entity(
    model=Mesh(vertices=trajectory_points, mode='line', thickness=1),
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
mark.position = trajectory_points[0]


def update_sphere_position(perc):
    index = int(perc * (len(trajectory_points) - 1))

    out = slerp(trajectory_points[index], trajectory_points[index+1], perc)

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


if platform.system() == "Darwin":  # macOS
    button_scale = 0.05
    button_spacing = 0.006
    text_size = 0.09
    y_position = -.02
    x_position = -.02
    text_scale = (text_size, text_size)
else:
    button_scale = 0.25
    button_spacing = 0.05
    text_size = 0.9
    y_position = -.3
    x_position = -0.1
    text_scale = (text_size, text_size)
# Play button
play_button = Button(
    text='Play',
    position=(-0.1, y_position),
    text_size=text_size,  # Use normalized text size
    scale=button_scale,
    color=color.black,
    parent=camera.ui,
    text_color=color.green
)
play_button.on_click = play

# Pause button
pause_button = Button(
    text='Stop',
    position=(x_position + button_spacing + button_scale, y_position),
    text_size=text_size,
    scale=button_scale,
    color=color.black,
    parent=camera.ui,
    text_color=color.orange
)
pause_button.on_click = pause

# Reverse button
reverse_button = Button(
    text='Rev',
    position=(x_position + 2 * (button_spacing + button_scale), y_position),
    text_size=text_size,
    scale=button_scale,
    color=color.black,
    parent=camera.ui,
    text_color=color.red
)
reverse_button.on_click = rev

# Instructions for dumbos
instructions_text = Text(
    text="Hold right mouse to rotate\nWASD to move the camera while rotating\nCommand+Q to quit",
    position=(x_position, y_position + button_scale),
    scale=text_scale,
    color=color.white,
    alpha=0.9
)

# Run the application
while True:
    # v+=1/60 * time.dt # one minute to completion.
    step_frame(time.dt)
    update_sphere_position(current_frac)
    app.step()
