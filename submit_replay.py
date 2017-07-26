import argparse
import asyncio

from trainingassistantreplaywatcher import create_training_assistant_replay_handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-analysis-service-url", "-a", type=str,
                        help="Url of replay analysis service",
                        default="http://{}:{}".format("localhost", 32331))
    parser.add_argument("--training-assistant-url", "-t", type=str,
                        help="Url of training assistant",
                        default="http://{}:{}".format("localhost", 32332))
    parser.add_argument('replay_path', metavar='REPLAY_PATH', type=str, nargs=1,
                        help="Path to replay to submit for analysis.")
    args = parser.parse_args()

    replay_handler = create_training_assistant_replay_handler(
        args.replay_analysis_service_url,
        args.training_assistant_url)
    asyncio.get_event_loop().run_until_complete(replay_handler.handle_replay(args.replay_path[0]))

if __name__ == '__main__':
    main()