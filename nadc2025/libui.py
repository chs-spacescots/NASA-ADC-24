import ursina
import platform
from ursina import Vec3

_all      = []
_dynamic  = []#autoscale+move with screen size
_static   = []#don't automatically reposition


#for appending elements to the UI scaling lists
def add_element(uielement, autoscale=True):
    _all.append(uielement)

    if autoscale:
        _dynamic.append(uielement)
    else:
        _static .append(uielement)

    return uielement

def add_elements(uielements, autoscale_all=True, parent=None):
    [add_element(i,autoscale=autoscale_all) for i in uielements]
    if parent:
        for e in uielements:
            e.parent=parent

    return uielements

print(f"Ursina Window Size: {ursina.window.size}")
#assuming a windowed screen size of Vec2(1280, 720)...

#caveman checks
# if platform.system() == "Darwin":  # macOS
#     button_scale = 0.005
#     button_spacing = 0.006
#     text_size = 0.09
#     y_position = -.02
#     x_position = -.02
#     text_scale = (text_size, .1)
# elif platform.system() == "Windows": #Windows
#     button_scale = 0.1
#     button_spacing = 0.06
#     text_size = 0.9
#     y_position = -0.3
#     x_position = -0.2
#     text_scale = (text_size, 1)
# else: #Linux, pls change vals as you see fit
#     button_scale = 0.1
#     button_spacing = 0.06
#     text_size = 0.9
#     y_position = -.075
#     x_position = -.02
#     text_scale = (text_size, 1)

#...convert to caveman SCALING factors
size_scale=pos_scale=text_scale = 1
if platform.system() == "Darwin":  # macOS
    size_scale = .05#=.05 (but why?)
    x_scale  = .05
    y_scale  = .05
    text_scale = .1
elif platform.system() == "Windows": #Windows
    # please adjust these values until TL,TR,BL,BR are at the corners of your screen!!
    size_scale = 1
    x_scale  = 1.775
    y_scale  = 1
    text_scale = 1
    pass
else: #Linux
    # please adjust these values until TL,TR,BL,BR are at the corners of your screen!!
    size_scale = 1
    x_scale  = .1
    y_scale  = .1
    text_scale = 1

def refit():
    for element in _dynamic:
        assert element.parent.name=="ui"# don't rescale if it's not a UI element

        element.position = Vec3(
            element.position.x * x_scale, 
            element.position.y * y_scale, 
            element.position.z
        )
        element.scale*=size_scale
        if hasattr(element, 'text_size'):#check if it has text before scaling text
            element.text_size*=text_scale
