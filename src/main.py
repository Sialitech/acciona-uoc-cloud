from uoc import UOC
from utils import alarmas, visualizaciones, borrar_alarmas, format_url
import schedule, time, json
from os import getenv
import socket


def main():
    SEG_ALARMAR = 10
    INTERVALO_VISUALIZACIONES = '6-18'
    BORRAR_ALARMAS = 300

    with open('../cfg/credentials.json') as json_file:
        CREDENTIALS = json.load(json_file)

    URL_UOC = "{}:{}".format(format_url(getenv("URL_UOC")), getenv("PORT_UOC"))
    print(URL_UOC, flush=True)
    uoc = UOC(URL_UOC, 'admin', 'admin')
    schedule.every(10).seconds.do(alarmas, uoc, CREDENTIALS, SEG_ALARMAR)
    schedule.every(5).seconds.do(
        visualizaciones, uoc, CREDENTIALS, INTERVALO_VISUALIZACIONES)
    # schedule.every().hour.do(
    #     alarmas, uoc, CREDENTIALS, INTERVALO_VISUALIZACIONES)
    schedule.every(5).minutes.do(borrar_alarmas, uoc, BORRAR_ALARMAS)

    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
