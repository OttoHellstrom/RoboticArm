from Controller import get_controller_input

while True:
    axes, buttons = get_controller_input()

    lx = axes[0]
    ly = axes[1]

    x_button = buttons[0]

    #print("LX:", lx, "LY:", ly, "X:", x_button)

    if x_button:
        print("X button pressed")
    
    if lx > 0.9:
        print("Right")
    elif lx < -0.9:
        print("Left")
    
    if ly > 0.9:
        print("Down")
    elif ly < -0.9:
        print("Up")

    

