import serial
from Controller import get_controller_input

def scale_axis(value, max_mm=10):
    return value * max_mm

def joystick_to_gcode(lx, ly, feedrate=500):
    x = scale_axis(lx)
    y = scale_axis(-ly)

    return f"G1 X{x:.2f} Y{y:.2f} F{feedrate}"

ser = serial.Serial('COM3', 115200)

def main():
    while True:
        axes, buttons = get_controller_input()
        lx = axes[0]
        ly = axes[1]
        
        axes, buttons = get_controller_input()
        lx, ly = axes[0], axes[1]

        gcode = joystick_to_gcode(lx, ly)
        ser.write((gcode + "\n").encode())

        print("Sent:", gcode)
        






    
