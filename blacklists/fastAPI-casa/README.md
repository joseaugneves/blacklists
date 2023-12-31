# Readme first

## Conteudo do folder


.\
├── Dockerfile **<-- ficheiro de configuração da Imagem**\
├── README.md **<-- It is I, Leclerc**\
├── app  **<-- Folder onde estão os ficheiros da app**\
│   ├── __init__.py\
│   ├── gunicorn_conf.py **<-- configurações do FastAPI**\
│   ├── main.py **<-- ficheiro principal da app, tem de existir**\
│   ├── prestart.sh **<-- script que arranca antes da app**\
│   └── requirements.txt **<-- libs a instalar via pip**\
├── app.env **<-- variaveis para as Imagens** \
├── build.sh **<-- script para build da Imagem**\
├── docker-compose.yml **<-- ficheiro de configuração do container**\
├── run.sh **<-- script para arrancar o container**\
├── stop.sh **<-- script para parar o container**\
├── teste.py **<-- programa exemplo para teste de performance**\
└── teste.sh **<-- script com chamadas à app**\


## Para usar

1. Criar um folder para o projecto e colocar lá estes files
2. Configurar as variveis específicas da app, no file app.env
3. Desenvolver a app. Começar com o file app\main.py, que tem de existir sempre. Seguir o formato, documentar todos os métodos como exemplificado
4. Executar `sh build.sh`
5. Executar `sh run.sh`

A app deverá ficar disponível em http://localhost:{port_publico_definido_no_app.env}\
Para testar os endpoints da api, abrir o browser em http://localhost:port/docs 



