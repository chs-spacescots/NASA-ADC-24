import ursina

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

def add_elements(uielements, should_autoscale):
    [add_element(i,autoscale=should_autoscale) for i in uielements]
    return uielements

print(ursina.window.size)
