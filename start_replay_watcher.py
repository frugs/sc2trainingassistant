import argparse

import sc2replaynotifier

from sc2trainingassistant.replayhandler import create_training_assistant_replay_handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-analysis-service-url", "-a", type=str,
                        help="Url of replay analysis service",
                        default="http://{}:{}".format("localhost", 32331))
    parser.add_argument("--training-assistant-url", "-t", type=str,
                        help="Url of training assistant",
                        default="http://{}:{}".format("localhost", 32332))
    args = parser.parse_args()

    replay_handler = create_training_assistant_replay_handler(
        args.replay_analysis_service_url,
        args.training_assistant_url)

    replay_notifier = sc2replaynotifier.create_replay_notifier(replay_handler)

    print("Waiting for replays...")

    replay_notifier.handle_replays()

if __name__ == '__main__':
    main()