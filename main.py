"""
Created on 
@author: Guilherme Soares Silvestre and Calvin Suzuki de Camargo
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback
from script import *
import sys
import signal
import socket

LAST_SPD = '0'
LAST_KV = '0'
LAST_VOLTAGE = '0'
DBG = True

# function to get wifi ip address from google connection
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def post_response(data, index):
    """Main function called method of do_POST server class method"""
    global DBG, LAST_SPD, LAST_KV, LAST_VOLTAGE
    speed_input = read_forms(data, 'speed')
    kv_input = read_forms(data, 'kv')
    voltage_input = read_forms(data, 'voltage')
    # Check all variables
    if speed_input == '' or speed_input == 'not found':
        speed_input = LAST_SPD
    else:
        LAST_SPD = speed_input
    if kv_input == '' or kv_input == 'not found':
        kv_input = LAST_KV
    else:
        LAST_KV = kv_input
    if voltage_input == '' or voltage_input == 'not found':
        voltage_input = LAST_VOLTAGE
    else:
        LAST_VOLTAGE = voltage_input

    # Controls motor speed
    duty_cycle = int(speed_input)/100 * 1e6 + 1e6
    write_duty_cycle(str(int(duty_cycle)), DBG)

    ## HTML UPDATE SECTION
    # SPEED RPM 
    speed = int(speed_input)*float(kv_input)*float(voltage_input)
    index = update_index(index, 'Speed: ', round(speed, 2))
    # RANGE SLIDER % LABEL
    index = update_index(index, '<div class="value">', speed_input)
    # RANGE SLIDER
    index = update_index(index, 'value=\"', speed_input)
    # KV PLACEHOLDER
    index = update_index(index, 'name="kv" placeholder=\"', kv_input)
    # VOLTAGE PLACEHOLDER
    index = update_index(index, 'name="voltage" placeholder=\"', voltage_input)
    # VELOCIMETER LEVEL
    index = update_index(index, '000', int(speed_input))

    # Then returns the modified webpage
    return index


def signal_handler(signum, frame):
    """Handles SIGNAL CTRL+C to stop PWM service correctly"""
    print('Closing server...')
    if not DBG:
        enable = "0"
        with open("/sys/class/pwm/pwmchip8/pwm0/enable", "w") as file4:
            file4.writelines([enable])
    exit(0)


class Server(BaseHTTPRequestHandler):
    """Extends BaseHTTPRequestHandler class to create our own web server"""

    def do_GET(self):
        """GET HTML Method to load index.html file as default"""
        global LAST_SPD
        # Reads index.html file
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        # Successful load
        try:
            index = open(self.path[1:]).read()
            self.send_response(200)
        # Error 404, file not found
        except:
            index = "File not found"
            self.send_response(404)
        self.end_headers()
        # VELOCIMETER LEVEL
        self.wfile.write(bytes(index, 'utf-8'))

    def do_POST(self):
        """POST HTML Method read and overwrite Duty Cycle PWM control file"""
        # Reads index.html file
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        # Successful load
        try:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            index = open(self.path[1:]).read()
            self.send_response(200)
        # Error 404, file not found
        except:
            index = "File not found"
            self.send_response(404)
        self.end_headers()

        # Executes post routine
        index = post_response(data, index)

        # Sends a updated index page
        self.wfile.write(bytes(index, 'utf-8'))


def main():
    global DBG
    # Register `SIGINT`handler (CTRL + C)
    signal.signal(signal.SIGINT, signal_handler)

    # Enter in DEBUG mode from terminal command line
    # ...\Squadrone> python main.py True

    if len(sys.argv) == 1:
        DBG = False
    else:
        DBG = sys.argv[1]

    # Setup values of PWM
    export = "0"
    period = "2000000"
    duty_cycle = "1000000"
    enable = "1"

    # print(f"Starting Squadrone \n export = {export}, period = {period}, duty_cycle = {duty_cycle}, enable = {enable}, debug = {DBG}")

    # print it without fstring
    print("Starting Squadrone \n export = %s, period = %s, duty_cycle = %s, enable = %s, debug = %s" % (
        export, period, duty_cycle, enable, DBG))

    # Starts PWM Service
    if not DBG:
        with open("/sys/class/pwm/pwmchip8/export", "w") as file1:
            file1.writelines([export])
        with open("/sys/class/pwm/pwmchip8/pwm0/period", "w") as file2:
            file2.writelines([period])
        with open("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w") as file3:
            file3.writelines([duty_cycle])
        with open("/sys/class/pwm/pwmchip8/pwm0/enable", "w") as file4:
            file4.writelines([enable])

    # Creates server
    if DBG:
        httpd = HTTPServer(('localhost', 8080), Server)
        print("Server started at http://localhost:8080")
    else:
        # TODO: EXTRACT OWN IP AUTOMATICALLY
        httpd = HTTPServer((get_ip(), 8080), Server)
        print("Server started at http://" + get_ip() + ":8080")

    httpd.serve_forever()


if __name__ == '__main__':
    main()
