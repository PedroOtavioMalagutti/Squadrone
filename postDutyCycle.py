from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

def readForms(body, word) :
    bd = body.decode('utf-8')
    index = bd.find(word) + len(word) + 1
    speedStr = bd[index:len(bd)]
    return speedStr

def writeDutyCycle(dutyCycle) :
    # TODO: FORMAT INPUT
    # dir = "/sys/class/pwm/pwmchip8/pwm0/duty_cycle"
    dir = './duty_cycle'
    file = open(dir, 'w')
    duty_cycle = file.writelines([dutyCycle])
    file.close()
    return

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
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
    httpd = HTTPServer(('localhost', 8080), Serv)
    httpd.serve_forever()

if __name__ == '__main__' :
    main()