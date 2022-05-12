# acciona-uoc-cloud

Permite sincronizar datos de las obras en el UOC, para ello se debe especificar en la tabla Obras del UOC las obras con su dirección (ip y puerto) para que se pude acceder a los datos. también hay que añadir al diccionario CREDENTIALS (en el main.py) las credenciales de las obras, con sl siguiente formato [ID_OBRA]: [[USUARIO], [PASSWORD]], ejem: 'ES102': ['admin', 'admin'].


El programa realiza las siguientes funciones periódicas con schedule:

- Cada 10 segundos guarda en el UOC las nuevas a alarmas de las diferentes obras. Si se asigna un valor entero a `SEG_ALARMAR` guardará sólo las alarmas que no lleven más de los X segundos establecidos en la variable.
- Cada hora, guarda o actualiza las visualizaciones en el UOC de las diferentes obras. Con `INTERVALO_VISUALIZACIONES` se puede asignar una valor string como `'10-16'` (de 10:00 a 16:00) para que solo se guarden o modifiquen las visualizaciones de las obras comprendidas en ese rango.
- Cada 5 minutos elimina las alamas antiguas en el UOC. Con `BORRAR_ALARMAS` (valores enteros) especifico que las alarmas que han pasado X segundos se deben borrar.


## Requisitos

Necesitas instalar schedule, puede ejecutar `pip3 install schedule` para instalarlo


## Ejecución
1. configurar bien las variables del docker-compose:
```yaml
- URL_UOC=django # url/ip donde está el servicio de django que contiene la API rest del UOC
- PORT_UOC=8000 # puerto donde está el servicio de django que contiene la API rest del UOC
- HORAS_VISUALIZACIONES=1 # ultimas horas de las que se quieren las visualizaciones. si es 1, se quieren visualizaciones de la última hora
```
2. Incluir el repo: [https://github.com/Sialitech/acciona-oasys-interface](https://github.com/Sialitech/acciona-oasys-interface). si se descarga aquí, poner bien la ruta al build del servicio django en el docker compose
3. ejecutar `docker-compose up`


## Crontab
Si quiere añadirlo en el crontab para que se ejecute cada vez que reinicies, con `crontab -e`, añade: 
`@reboot sleep 30 && /usr/bin/python3.8 /mydir/main.py > /home/$(whoami)/cronjoblog 2>&1

Importante: hay que añadir a la variable de entorno PYTHONPATH la ruta de las librerías instaladas, sino el crontab no las detectará. Añadir en el mismo crontab la siguiente linea:
    `PYTHONPATH=/home/pi/.local/lib/python3.8/site-packages`

Nota: 
- `mydir`: es el directorio donde tienes main.py, debes especificarlo
- `cronjoblog`: es un archivo que se creara en tu directorio home, cuando haya algún error al ejecutar el programa por el crontab, revisalo si hay fallos en al ejecución.
- El ejemplo se ha hecho con la version 3.8 de python3.8, en función de tu version deberás modificarlo 
