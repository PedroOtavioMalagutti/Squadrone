#include <stdio.h>
#include <unistd.h>

int main(){

    /***************************************************
    Programa de teste do pino pwm da Viola Carrier Board
    com a placa Colibri Vf50, deve ser performado com um
    osciloscópio para verificaçãodo funcionamento e da
    precisão
    ****************************************************/

    //Definição dos ponteiros para os arquivos que definem o pwm
    FILE *fex, *fp, *fdc, *fh; 


    char export[1] = "0"; //pino a ser utilizado
    char period[7] = "2000"; //Período do PWM
    char duty_cycle[4] = "0000";
    char habilitate[1] = "1"; //Liga o PWM

    /*Escreve no arquivo que define o pino a ser utilizado.
    Nesse caso, como estamos na pasta pwmchip8, de acordo com
    o datacheet da Viola Carrier Board, temos a disposição os pinos
    42 para o caso de export = 0  e 44 para export = 1*/
    fex = fopen("/sys/class/pwm/pwmchip8/export", "w");
    fputs(export,fex);
    fclose(fex);

    //Escreve no arquivo que define o período do pwm
    fp = fopen("/sys/class/pwm/pwmchip8/pwm0/period", "w");
    fputs(period, fp);
    fclose(fp);

    //Escreve no arquivo que define o duty cycle
    fdc = fopen("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w");
    fputs(duty_cycle, fdc);
    fclose(fdc);

    /*Inicia o PWM com as características definidas nos arquivos
    e desabilita caso habilitar = 0*/
    fh= fopen("/sys/class/pwm/pwmchip8/pwm0/enable","w");
    fputs(habilitate, fh);
    fclose(fh);

    /*Para testar o programa, com um osciloscópio conectado à porta
    42, o valor do duty cycle vai aumentando gradativamente com seu 
    valor sendo mostrado no terminal a cada iteração, podendo-se
    verificar na tela do osciloscópio se duty cycle mostrado
    corresponde com o real*/
    for (int i = 1000; i <= 2000; i = i + 10) {
        printf("ola %d\n", i);
        fdc = fopen("/sys/class/pwm/pwmchip8/pwm0/duty_cycle", "w");
        fprintf(fdc, "%d", i);
        fclose(fdc);
        usleep(250000);
    }
    return(0);
}
