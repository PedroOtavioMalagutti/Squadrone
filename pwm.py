"""
Created on 

@author: Kiyoshi Frade Araki
"""
# Python program to write files
import time 

export = "0" #//pino a ser utiliza
period = "2000" #//Período do PWM
duty_cycle = "0000"
habilitate = "1" #//Liga o PWM

file1 = open("/sys/class/pwm/pwmchip8/export", "w")
L1 = [export]
file1.writelines(L1)
file1.close()

#Escreve no arquivo que define o período do pwm
file2 = open("/sys/class/pwm/pwmchip8/pwmo0/period", "w")
L2 = [period]
file2.writelines(L2)
file2.close()

file3 = open("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w")
L3 = [duty_cycle]
file3.writelines(L3)
file3.close()

file4 = open("/sys/class/pwm/pwmchip8/pwm0/enable", "w")
L4 = [habilitate]
file4.writelines(L4)
file4.close()

for i in range(1000,2000,10): 
    print("ola", i)
    with open("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w") as file3:
        file3.write(i)
    file3.close()
time.sleep(0.25)




