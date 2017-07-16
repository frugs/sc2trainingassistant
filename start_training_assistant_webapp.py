import os

from sc2trainingassistant.webapp import start_webapp

HOST = "localhost"
PORT = 32332

APP_DATA_PATH = os.path.expanduser("~/.sc2trainingassistant")


def main():
    if not os.path.exists(APP_DATA_PATH):
        os.makedirs(APP_DATA_PATH)

    db_path = os.path.join(APP_DATA_PATH, "db.json")

    start_webapp(HOST, PORT, db_path)

if __name__ == "__main__":
    main()