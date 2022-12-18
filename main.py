from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback
from script import *
import sys
import signal

LAST_RPM = '0000'
DBG = False

# Our signal handler
def signal_handler(signum, frame):  
    """Handles SIGNAL CTRL+C to stop PWM service correctly"""
    print('Closing server...')
    if not DBG :
        enable = "0"    
        with open("/sys/class/pwm/pwmchip8/pwm0/enable", "w") as file4:
            file4.writelines([enable])
    exit(0)

class Server(BaseHTTPRequestHandler):
    """Extends BaseHTTPRequestHandler class to create our own web server"""

    def do_GET(self):
        """GET HTML Method to load index.html file as default"""
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
        self.wfile.write(bytes(index, 'utf-8'))

    def do_POST(self):
        """POST HTML Method read and overwrite Duty Cycle PWM control file"""
        global DBG, LAST_RPM
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
        try :
            index, LAST_RPM = post_response(data, index, DBG)
        # If error in method, keep last valid speed
        except Exception as e :
            print(e)
            index = update_index(index, 'Actual Speed:', LAST_RPM)

        self.wfile.write(bytes(index, 'utf-8'))

def main() :

    global DBG

    # Register `SIGINT`handler (CTRL + C)
    signal.signal(signal.SIGINT, signal_handler)

    # Enter in DEBUG mode from terminal command line
    # ...\Squadrone> python main.py True 
    if len(sys.argv) == 1 :
        DBG = False
    else :
        DBG = sys.argv[1]

    # Setup values of PWM
    export = "0"
    period = "2000"
    duty_cycle = "0000"
    enable = "1"

    # Starts PWM Service
    if not DBG :
        with open("/sys/class/pwm/pwmchip8/export", "w") as file1:
            file1.writelines([export])
        with open("/sys/class/pwm/pwmchip8/pwm0/period", "w") as file2:
            file2.writelines([period])
        with open("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w") as file3:
            file3.writelines([duty_cycle])
        with open("/sys/class/pwm/pwmchip8/pwm0/enable", "w") as file4:
            file4.writelines([enable])

    # Creates server
    if DBG :
        httpd = HTTPServer(('localhost', 8080), Server)
    else :
        # TODO: EXTRACT OWN IP AUTOMATICALLY
        httpd = HTTPServer(('192.168.0.196', 8080), Server)

    httpd.serve_forever()

if __name__ == '__main__' :
    main()