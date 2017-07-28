import argparse

from replayuploader import start_webapp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", help="The hostname to listen at", default="0.0.0.0")
    parser.add_argument("--port", "-p", help="The port to listen on", default=32333)
    parser.add_argument("--replay-analysis-service-url", "-a", type=str,
                        help="Url of replay analysis service",
                        default="http://{}:{}".format("localhost", 32331))
    parser.add_argument("--training-assistant-url", "-t", type=str,
                        help="Url of training assistant",
                        default="http://{}:{}".format("localhost", 32332))
    args = parser.parse_args()

    host = args.host
    port = args.port
    analyse_replay_endpoint = args.replay_analysis_service_url + "/submit"
    add_replay_analysis_endpoint = args.training_assistant_url + "/add/"
    show_replay_analysis_endpoint = args.training_assistant_url + "/analysis.html?hash="

    start_webapp(host, port, analyse_replay_endpoint, add_replay_analysis_endpoint, show_replay_analysis_endpoint)


if __name__ == "__main__":
    main()
