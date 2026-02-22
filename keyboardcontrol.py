import keyboard
import time
import serial
import threading

# Inställningar
com_port = 'COM3'
flowrate = 200
ser = None
lock = threading.Lock()  # Lås för trådsäkerhet
current_active_key = None

def send(cmd):
    if ser and ser.is_open:
        ser.write((cmd + "\n").encode())
        # print(f"Sent: {cmd}") # Avkommentera för felsökning

def start_move(direction, key_name):
    global current_active_key
    
    with lock:
        # Om vi redan håller ner samma tangent, gör ingenting
        if current_active_key == key_name:
            return
            
        # Uppdatera tillståndet direkt för att förhindra race conditions
        current_active_key = key_name
    
    print(f"--- Startar rörelse {key_name}: {direction} ---")
    
    # Skicka G91 bara en gång vid start av session eller var säker på att den är aktiv
    send("G91")        # Relativt läge
    send(f"G1 Z{direction} F{flowrate}") # Ändrade Z till X för Left/Right

def stop_move(key_name):
    global current_active_key
    
    with lock:
        # Kontrollera om det är denna tangent som styr rörelsen
        # Om vi bytt tangent mitt i, ska inte denna release stoppa den nya rörelsen
        if current_active_key != key_name:
            return
            
        print(f"--- Stoppar rörelse ({key_name}) ---")
        current_active_key = None

    send("!")          # Feed hold
    time.sleep(0.05)
    send("~")          # Resume
    # Ta bort G90 här för att undvika tillståndsförvirring vid nästa start

def main():
    global ser
    try:
        ser = serial.Serial(com_port, 115200, timeout=1)
        time.sleep(2)
        print(f"Ansluten till {com_port}")
        
        # Nollställ maskinens läge till relativt vid start
        send("G91") 
    except Exception as e:
        print(f"Fel: {e}")
        return

    # Bind tangenter
    # Notera: Vi skickar med key_name till stop_move också så den vet vad den ska stoppa
    keyboard.on_press_key("left", lambda e: start_move(50, "left"))   # Minska distansen för test (t.ex. 50mm)
    keyboard.on_release_key("left", lambda e: stop_move("left"))

    keyboard.on_press_key("right", lambda e: start_move(-50, "right"))
    keyboard.on_release_key("right", lambda e: stop_move("right"))

    print("Kontroll aktiv. Tryck 'Esc' för att avsluta.")
    keyboard.wait('esc')
    
    # Återställ till absolut läge vid avslut
    send("G90")
    if ser:
        ser.close()

if __name__ == "__main__":
    main()