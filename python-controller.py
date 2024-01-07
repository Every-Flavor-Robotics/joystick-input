import pygame
import socket
import time

# Function to read IP address from a file
def read_ip_address(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

# Initialize Pygame for Xbox controller input
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Read the IP address from the file
udp_ip = read_ip_address("ip_address.txt")  # Ensure the file 'ip_address.txt' is in the same directory
udp_port = 8008
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to get and invert joystick data
def get_joystick_data():
    pygame.event.pump()
    left_x = round(joystick.get_axis(0), 2)
    left_y = -round(joystick.get_axis(1), 2)  # Inverting the Y-axis
    right_x = round(joystick.get_axis(2), 2)
    right_y = -round(joystick.get_axis(3), 2)  # Inverting the Y-axis
    return left_x, left_y, right_x, right_y

last_time = time.perf_counter()

try:
    while True:
        # Get joystick data
        lx, ly, rx, ry = get_joystick_data()

        # Format the message
        message = f"LX: {lx}, LY: {ly}, RX: {rx}, RY: {ry}"

        # Send the message
        sock.sendto(message.encode('ascii'), (udp_ip, udp_port))
        print(lx, ly, rx, ry)
        # Calculate elapsed time and sleep accordingly
        elapsed = time.perf_counter() - last_time
        sleep_time = max(0.02 - elapsed, 0)  # Ensure sleep_time is not negative
        time.sleep(sleep_time)

        # Update last_time for the next iteration
        last_time = time.perf_counter()

except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    pygame.quit()
    sock.close()