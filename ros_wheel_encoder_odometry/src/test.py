import serial
import threading
import time

# Function to read data from serial port
def read_from_port(ser, event):
    while True:
        try:
            # Read a line of data from the serial port
            line = ser.readline().decode().strip()
            print("Received:", line)
            # Trigger the event if certain conditions are met
            if line == b'event_trigger':
                event.set()  # Set the event
        except Exception as e:
            print("Error reading from serial port:", e)

# Event handler function
def event_handler(event):
    while True:
        # Wait for the event to be set
        event.wait()
        # Event has been triggered, do something
        print("Event triggered!")
        # Reset the event
        event.clear()

# Open the serial port
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change port and baud rate as needed
except serial.SerialException as e:
    print("Error opening serial port:", e)
    exit()

# Create an event object
event = threading.Event()

# Create a thread to continuously read from the serial port
read_thread = threading.Thread(target=read_from_port, args=(ser, event))
read_thread.daemon = True
read_thread.start()

# Create a thread to handle events
event_thread = threading.Thread(target=event_handler, args=(event,))
event_thread.daemon = True
event_thread.start()

# Main loop to handle other tasks or wait for events
try:
    while True:
        # Perform other tasks or wait for events here
        time.sleep(1)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")
