from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback

def read_forms(body, word) :
    """Reads a attribute from a forms structured data"""
    bd = body.decode('utf-8')
    index = bd.find(word) + len(word) + 1
    if bd.find(word) == -1 :
        return str('not found')
    ending = bd.find('&', index)
    if ending == -1 : 
        data = bd[index:]
    else :
        data = bd[index:ending]
    print(body)
    print('(' + data + ')')

    if not data.isnumeric() :
        raise Exception("ERROR: BAD FORMAT")
    elif int(speedStr) > 100 :
        raise Exception("ERROR: BAD RANGE. MAX 100")
    elif int(speedStr) < 0 :
        raise Exception("ERROR: BAD RANGE. MIN 0")
    else :
        data = int(data)

    return str(data)

def write_duty_cycle(dutyCycle, DBG) :    
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
    speed_input = read_forms(data, 'speed') 
    kv_input = read_forms(data, 'kv')
    tensao_input = read_forms(data, 'Tensao')
    write_duty_cycle(speed_input, DGB)

    # Updates the index base file         
    new_index = update_index(index, 'Speed: ', speed_input)
    # Then returns the modified webpage
    return new_index, speed_input