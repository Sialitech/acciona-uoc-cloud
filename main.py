from uoc import UOC
from utils import alarmas, visualizaciones, borrar_alarmas
import schedule
import time


def main():
    CREDENTIALS = {
        'C1070': ['admin', 'admin']
    }
    SEG_ALARMAR = 10
    INTERVALO_VISUALIZACIONES = '6-18'
    BORRAR_ALARMAS = 300

    uoc = UOC('http://localhost:80', 'admin', 'admin')
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
