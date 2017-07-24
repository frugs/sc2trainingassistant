import argparse
import os

from sc2trainingassistant.webapp import start_webapp

APP_DATA_DEFAULT_PATH = os.path.expanduser("~/.sc2trainingassistant/db.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", help="The hostname to listen at", default="0.0.0.0")
    parser.add_argument("--port", "-p", help="The port to listen on", default=32332)
    parser.add_argument("--dbpath", "-d", help="The path to the local database", default=APP_DATA_DEFAULT_PATH)
    args = parser.parse_args()

    host = args.host
    port = args.port
    db_path = args.dbpath

    if not os.path.exists(db_path):
        db_dir = os.path.dirname(db_path)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    elif not os.path.isfile(db_path):
        raise ValueError("Object at database path (" + db_path + ") is not a file.")

    start_webapp(host, port, db_path)

if __name__ == "__main__":
    main()