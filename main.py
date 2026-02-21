import serial
import time
from Controller import get_controller_input

def scale_axis(value, max_mm=1):
    return value * max_mm

def apply_deadzone(value, threshold=0.15):
    return 0 if abs(value) < threshold else value

ser = serial.Serial('COM3', 115200)
time.sleep(2)

last_y = None
last_z = None

def main():
    global last_y, last_z

    try:
        while True:
            axes, buttons = get_controller_input()
            lx, ly = axes[0], axes[1]

            lx = apply_deadzone(lx)
            ly = apply_deadzone(ly)

            z = scale_axis(lx)
            y = scale_axis(-ly)

            if y != last_y or z != last_z:
                gcode = f"G1 Y{y:.2f} Z{z:.2f} F100"
                ser.write((gcode + "\n").encode())
                print("Sent:", gcode)

                last_y = y
                last_z = z

            time.sleep(0.01)  # 100 Hz loop

    except KeyboardInterrupt:
        print("Stopping safely...")
        ser.write(b"!\n")  # feed hold

    finally:
        ser.close()
        print("Serial closed.")

if __name__ == "__main__":
    main()
