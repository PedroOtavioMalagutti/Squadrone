# Squadrone
## Membros
* Caio Brandolim Rovetta
* Calvin Suzuki de Camargo 
* Guilherme Soares Silvestre
* Kiyoshi Araki Frade
* Pedro Otavio Malagutti

## Objetivo
Desenvolvimento do controle de um motor de drone a partir de uma Colibri VF50, através dos pinos de PWM disponíveis.

## Materiais

* Toradex Colibri VF50
* Toradex Viola Carrier Board
* Motor Brushless
* ESC
* Fonte 5V
* Cabo Ethernet
* Roteador Wi-fi

## Montagem

Primeiramente é necessário conectar o sistema embarcado (target) e o computador de desenvolvimento (host) na mesma rede LAN, utilizando o protocolo ssh. Segue na imagem abaixo a montagem do sistema:

<img src="https://i.imgur.com/Uvr4Nv4.jpg=250x250" alt="drawing" width="300"/>

Com o host conectado no wi-fi, abra um terminal e digite o seguinte comando:

``` ip -a  ```

Busque pela interface wlp3s0

<img src="https://i.imgur.com/kv1xyzG.png" alt="drawing"/>

Em seguida execute 

```sudo arp-scan --localhost --interface=wlp3s0```

(imagem do terminal)

Copie o IP obtido para a Toradex no campo indicado abaixo

```ssh root@<IP toradex>```

Com isso, o terminal passa agora a operar no target

<img src="https://i.imgur.com/LBFAXkp.png" alt="drawing"/>

# Instalação do python no Embarcado

Dentro do terminal da VF50, basta utilizar o comando opkg para instalar o interpretador do python e seus pacotes padrões. Antes de usar certifique que o mesmo enontra-se atualizado.

```opkg update```


```opkg install python3```


# Transferência dos arquivos para o Embarcado

Primeiramente, crie uma pasta referente ao projeto no target

```mkdir Squadrone```

Para executar o programa na placa, é necessário transferir os seguintes arquivos do repositório

* main.py
* script.py
* index.html
* index.js
* style.css
* assets

Para tanto basta executar no terminal do host

```scp <nome dos arquivos> root@<IP toradex>:/root/Squadrone```


## Montagem da ESC + Motor

Conecte corretamente os terminais da ESC no motor (atente-se às especificações do seu equipamento) e a alimente. Então resta conectar a porta que fará o controle da velocidade, a PWM que, para o este projeto, foi desenvolvida no pino 42 da placa Viola Carrier Board

<img src="https://i.imgur.com/ppkXWCl.png" alt="drawing" width="300"/>

<img src="https://i.imgur.com/WXrWl84.png" alt="drawing"/>

## Executando o programa

No terminal do target, execute o arquivo main.py

```python3 main.py```

No terminal do host, abra o navegador e digite

```<IP toradex>:8080/index.html```

Preencha os campos indicados da tabela com os respectivos valores de Kv e Tensão de bateria de acordo com o equipamento utilizado. Pressione o botão submit configurations ao final.

<img src="https://i.imgur.com/aQahOpF.gif" alt="drawing"/>

Por fim, para controlar a velocidade, basta arrastar o slider para o percentual desejado e pressionar o botão submit.

<img src="https://i.imgur.com/s0B86Pf.gif" alt="drawing"/>

## Considerações Finais

### Front-end

Dentre as opções disponíveis, estavam o software de desenvolvimento QT-Creator e a aplicação web.

Vantagens do web sobre o QT:

* Biblioteca mais atualizada
* Escalabilidade
* Interface gráfica é processada no Client

Obs: A versão do QT-creator compatível com a Colibri VF50 era muito antigo, gerando dificuldades para encontrá-lo e instalar no embarcado.

### Back-end

Com a escolha da aplicação web para o Front-end, o python foi selecionado com o intuito de simplificar a hospedagem do web-server, devido ao fato de possuir a biblioteca *http.server* que auxilia nessa tarefa.