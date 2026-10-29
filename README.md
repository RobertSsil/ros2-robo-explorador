[![ROS
2](https://img.shields.io/badge/ROS%202-Robot%20Operating%20System-22314E?logo=ros&logoColor=white)](https://ros.org/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![C++](https://img.shields.io/badge/C%2B%2B-Interfaces-00599C?logo=cplusplus&logoColor=white)](https://isocpp.org/)

**Disciplina:** Tópicos Especiais em Redes de Computadores - 2026.2\
**Avaliação:** 1ª Avaliação Prática - 28/10/2026

------------------------------------------------------------------------

### Cenário para as questões
Um robô móvel está se deslocando em um ambiente insalubre, em que há um baixo nível de oxigênio e altas temperaturas. O robô possui um GPS que dá as coordenadas de latitude e longitude, além de sensores de nível oxigênio e temperatura em graus Celsius, e um coletor de solo, que será analisado na estação base. Suponha que o GPS, os sensores e o coletor de solo sempre funcionem sem falhas.

-----------------------------------------------------------------------
### Estrutura dos arquivos
``` text
ros2_ws/
└── src/
    ├── robo_interfaces/
    │   ├── msg/
    │   │   └── Monitoramento.msg
    │   ├── srv/
    │   │   └── ColetaAmostra.srv
    │   ├── action/
    │   │   └── Deslocamento.action
    │   ├── CMakeLists.txt
    │   └── package.xml
    │
    └── robo_explorador/
        ├── robo_explorador/
        │   ├── __init__.py
        │   ├── robo_topico_publish.py
        │   ├── robo_topico_subscriber.py
        │   ├── robo_coleta_cliente.py
        │   ├── robo_coleta_servidor.py
        │   ├── robo_deslocamento_servidor.py
        │   ├── robo_deslocamento_cliente.py
        │   └── robo_deslocamento_cancela.py
        ├── resource/
        ├── package.xml
        ├── setup.py
        └── setup.cfg
```

#### 1. Pacotes ROS 2

-   **`robo_interfaces`**: reúne as interfaces de comunicação.
-   **`robo_explorador`**: reúne os nós Python que implementam o
    comportamento do sistema.

#### 2. Monitoramento ambiental

A interface `Monitoramento.msg` define os campos para o nível de
oxigênio e a temperatura.

-   **Publicador: `robo_topico_publish.py`:** gera valores aleatórios
    entre 1 e 100 e publica no tópico `/monitoramento`.
-   **Assinante: `robo_topico_subscriber.py`:** recebe os dados e
    classifica o ambiente:
    -   `Safe`: temperatura entre 10 e 40 °C, inclusive, e nível de
        oxigênio superior a 80.
    -   `Not Safe`: quando uma ou mais condições não são atendidas.

#### 3. Coleta de amostras

A interface `ColetaAmostra.srv` recebe a profundidade da coleta e
retorna um booleano indicando o sucesso.

-   **Cliente: `robo_coleta_cliente.py`:** solicita a coleta com
    profundidade aleatória entre 0,1 e 0,5.
-   **Servidor: `robo_coleta_servidor.py`:** determina o sucesso com
    probabilidade de 70%.

#### 4. Deslocamento do robô

A interface de ação define a meta de deslocamento, o feedback com a
localização atual e o resultado com a distância percorrida.

-   **Servidor:`robo_deslocamento_servidor.py`:** recebe a meta,
    simula o deslocamento e envia feedback periódico.
-   **Cliente: `robo_deslocamento_cliente.py`:** aguarda a conclusão
    da ação e apresenta a distância percorrida.
-   **Cliente com cancelamento: `robo_deslocamento_cancela.py`:**
    solicita o cancelamento após cinco segundos e apresenta as
    informações disponíveis da execução.


### Compilação

Os comandos a seguir pressupõem que o workspace se chama `ros2_ws` e
está localizado na pasta pessoal do usuário. Execute-os no ambiente em
que o ROS 2 está instalado.

``` bash
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```
Em cada novo terminal, carregue os ambientes antes de executar os nós:

``` bash
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
```

### Monitoramento

Terminal 1 - publicador:

``` bash
ros2 run robo_explorador robo_topico_publish
```

Terminal 2 - assinante:

``` bash
ros2 run robo_explorador robo_topico_subscriber
```

Para observar as mensagens diretamente:

``` bash
ros2 topic echo /monitoramento
```

### Coleta de amostras

Terminal 1 - servidor:

``` bash
ros2 run robo_explorador robo_coleta_servidor
```

Terminal 2 - cliente:

``` bash
ros2 run robo_explorador robo_coleta_cliente
```

### Deslocamento

Terminal 1 - servidor da ação:

``` bash
ros2 run robo_explorador robo_deslocamento_servidor
```

Terminal 2 - cliente que aguarda a conclusão:

``` bash
ros2 run robo_explorador robo_deslocamento_cliente
```

Para testar o cliente que solicita cancelamento após cinco segundos,
execute em outro terminal:

``` bash
ros2 run robo_explorador robo_deslocamento_cancela
```
