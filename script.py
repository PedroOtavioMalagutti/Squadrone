from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback

LAST_RPM = '0000'

def readForms(body, word) :
    """Reads a attribute from a forms structured data"""
    bd = body.decode('utf-8')
    index = bd.find(word) + len(word) + 1
    speedStr = bd[index:]
    print('(' + speedStr + ')')

    if not speedStr.isnumeric() :
        raise Exception("ERROR: BAD FORMAT")
    else :
        speedStr = int(speedStr)

    return str(speedStr)

def writeDutyCycle(dutyCycle) :    
    """Writes a value to Duty Cycle PWM control file"""
    dir = "/sys/class/pwm/pwmchip8/pwm0/duty_cycle"
    # dir = './duty_cycle'

    with open(dir, 'w') as file:
        duty_cycle = file.writelines([dutyCycle])

    return

def updateIndex(file, target, info) :
    # Atualiza pagina
    info = ' ' + info
    aux = file.split(target)
    aux.insert(1, target)
    aux.insert(2, info)
    return ''.join(aux)

class Server(BaseHTTPRequestHandler):
    """Extends BaseHTTPRequestHandler class to create our own web server"""
    

    def do_GET(self):
        """GET HTML Method to load index.html file as default"""
        if self.path == '/':
            self.path = '/index.html'
        try:
            index = open(self.path[1:]).read()
            self.send_response(200)
        except:
            index = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(index, 'utf-8'))

    def do_POST(self):
        """POST HTML Method read and overwrite Duty Cycle PWM control file"""

        global LAST_RPM
        if self.path == '/':
            self.path = '/index.html'
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            index = open(self.path[1:]).read()
            self.send_response(200)
        except:
            index = "File not found"
            self.send_response(404)
        self.end_headers()
        
        try :
            speedInput = readForms(body, 'speed') 

            writeDutyCycle(speedInput)

            # Atualiza pagina
            index = updateIndex(index, 'Actual Speed:', speedInput)
            self.wfile.write(bytes(index, 'utf-8'))
            LAST_RPM = speedInput
        except Exception as e :
            print(e)
            index = updateIndex(index, 'Actual Speed:', LAST_RPM)
            self.wfile.write(bytes(index, 'utf-8'))

def main() :

    export = "0"
    period = "2000"
    duty_cycle = "0000"
    enable = "1"

    with open("/sys/class/pwm/pwmchip8/export", "w") as file1:
        file1.writelines([export])
        
    with open("/sys/class/pwm/pwmchip8/pwm0/period", "w") as file2:
        file2.writelines([period])
        
    with open("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w") as file3:
        file3.writelines([duty_cycle])
        
    with open("/sys/class/pwm/pwmchip8/pwm0/enable", "w") as file4:
        file4.writelines([enable])

    """Creates the server"""
    httpd = HTTPServer(('localhost', 8080), Server)
    httpd.serve_forever()

if __name__ == '__main__' :
    main()