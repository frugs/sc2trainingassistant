from sc2trainingassistant.webapp import start_webapp

HOST = "localhost"
PORT = 32332


def main():
    start_webapp(HOST, PORT, "/tmp/blah.json")

if __name__ == "__main__":
    main()