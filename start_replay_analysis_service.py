import argparse

from replayanalysisservice import start_replay_analysis_service


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", help="The hostname to listen at", default="0.0.0.0")
    parser.add_argument("--port", "-p", help="The port to listen on", default=32331)
    args = parser.parse_args()

    start_replay_analysis_service(args.host, args.port)


if __name__ == "__main__":
    main()