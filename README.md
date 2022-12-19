# Squadrone

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

(Verificar se é possível enviar todos de uma vez)


## Executando o programa

No terminal do target, execute o arquivo main.py

```python3 main.py```

No terminal do host, abra o navegador e digite

```<IP toradex>:8080/index.html```
