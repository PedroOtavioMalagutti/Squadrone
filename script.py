from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback

def __read_forms(body, word) :
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

def __write_duty_cycle(dutyCycle, DBG) :    
    """Writes a value to Duty Cycle PWM control file"""
    if DBG : dir = './duty_cycle'
    else : dir = "/sys/class/pwm/pwmchip8/pwm0/duty_cycle"

    with open(dir, 'w') as file:
        duty_cycle = file.writelines([dutyCycle])

    return

def update_index(file, target, info) :
    """Method that searches and updates an index file"""
    info = ' ' + info
    aux = file.split(target)
    aux.insert(1, target)
    aux.insert(2, info)
    return ''.join(aux)

def post_response(data, index, DGB = 0) :
    """Main function called method of do_POST server class method"""
    speed_input = __read_forms(data, 'speed') 
    __write_duty_cycle(speed_input, DGB)

    # Updates the index base file         
    new_index = update_index(index, 'Actual Speed:', speed_input)

    return new_index, speed_input