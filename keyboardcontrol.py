import keyboard
import time
import serial

com_port = 'COM3'
flowrate = 100

z_pos = 0.0

def sendgcode(gcode, flowrate):
    if ser.is_open:
        gcodecomplete = f"{gcode} F{flowrate}"
        ser.write((gcodecomplete + "\n").encode())
        print("Sent:", gcodecomplete)
    else:
        print("Serial port not open")

def keyboardandserial():
        
        global z_pos
        
        up = keyboard.is_pressed('up')
        down = keyboard.is_pressed('down')  
        left = keyboard.is_pressed('left')
        right = keyboard.is_pressed('right')
        

        if left:
             z_pos += 1.0
             print("left pressed")
             sendgcode(f"G1 Z{z_pos:.2f}", flowrate)
        elif right:
             z_pos -= 1.0
             print("right pressed")
             sendgcode(f"G1 Z{z_pos:.2f}", flowrate)
        
def main():
    global ser
    try:
        ser = serial.Serial('COM3', 115200)
        time.sleep(2)

        while True:
            keyboardandserial()
            time.sleep(0.01) 

    except serial.SerialException as e:
        print("Serial error:", e)
        return

    except KeyboardInterrupt:
        print("Stopping safely...")
        ser.write(b"!\n")

    finally:
        ser.close()
        print("Serial closed.")

        
if __name__ == "__main__":
    main()