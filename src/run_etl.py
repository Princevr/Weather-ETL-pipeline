import subprocess
from datetime import datetime
from send_email import send_alert

def run_etl():
    try:
        with open("etl_log.txt", "a") as log:
            log.write(f"\n----- ETL RUN at {datetime.now()} -----\n")
            log.write("Fetching weather data...\n")
            subprocess.run(["python", "src/fetch_weather.py"], stdout=log, stderr=log)

            log.write("Cleaning weather data...\n")
            subprocess.run(["python", "src/clean_weather.py"], stdout=log, stderr=log)

            log.write("Storing data...\n")
            subprocess.run(["python", "src/store_to_sqlite.py"], stdout=log, stderr=log)

            log.write("ETL completed.\n")

        send_alert(" ETL Success", "Your ETL pipeline ran successfully.")

    except Exception as e:
        send_alert(" ETL Failed", f"ETL failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    run_etl()
