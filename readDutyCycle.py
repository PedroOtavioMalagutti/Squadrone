from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

def readSpeed() :
    # dir = "/sys/class/pwm/pwmchip8/pwm0/duty_cycle"
    dir = './duty_cycle'
    file = open(dir, "r")
    duty_cycle = file.readlines()[0]
    file.close()
    return str(duty_cycle)

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(readSpeed().encode())

def main() :
    httpd = HTTPServer(('localhost', 8080), Serv)
    httpd.serve_forever()

if __name__ == '__main__' :
    main()