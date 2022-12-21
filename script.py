# script.py - main.py modularization
# 
# Author: Calvin Suzuki
# 
# This file holds functions called in 'post_response' method in main.py file.
from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback

def read_forms(forms, word) :
    """Reads a attribute from a forms structured data"""
    forms_str = forms.decode('utf-8')
    index = forms_str.find(word) + len(word) + 1
    # If there is not 'word' in received forms
    if forms_str.find(word) == -1 :
        print( word + ': not found') 
        return str('not found')
    # Read until find next '&'
    ending = forms_str.find('&', index)
    # Or until the end of forms
    if ending == -1 : ending = len(forms_str)
    # Reads data
    data = forms_str[index:ending]
    # Check emptiness 
    if str(data) == '' : data = 'empty'
    # Shows info on terminal
    print( word + '(' + data + ')')
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
    info = str(info)
    aux = file.split(target)
    aux.insert(1, target)
    aux.insert(2, info)
    return ''.join(aux)
