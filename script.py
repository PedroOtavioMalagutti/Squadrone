from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

def readForms(body, word) :
    """Reads a attribute from a forms structured data"""
    bd = body.decode('utf-8')
    index = bd.find(word) + len(word) + 1
    speedStr = bd[index:]

    if not speedStr.isnumeric() :
        print('error: bad format!')
        return "ERROR: BAD FORMAT"

    return speedStr

def writeDutyCycle(dutyCycle) :    
    """Writes a value to Duty Cycle PWM control file"""
    # dir = "/sys/class/pwm/pwmchip8/pwm0/duty_cycle"
    dir = './duty_cycle'
    file = open(dir, 'w')
    duty_cycle = file.writelines([dutyCycle])
    file.close()
    return

class Server(BaseHTTPRequestHandler):
    """Extends BaseHTTPRequestHandler class to create our own web server"""

    def do_GET(self):
        """GET HTML Method to load index.html file as default"""
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        """POST HTML Method read and overwrite Duty Cycle PWM control file"""
        if self.path == '/':
            self.path = '/index.html'
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        
        writeDutyCycle(readForms(body, 'speed'))

        self.wfile.write(bytes(file_to_open, 'utf-8'))

def main() :
    """Creates the server"""
    httpd = HTTPServer(('localhost', 8080), Server)
    httpd.serve_forever()

if __name__ == '__main__' :
    main()