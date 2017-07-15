import argparse
import asyncio
import sc2reader

from sc2trainingassistant.replayhandler import create_training_assistant_replay_handler

HOST = "localhost"
PORT = 32332


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('replay_path', metavar='REPLAY_PATH', type=str, nargs=1,
                        help="Path to replay to submit for analysis.")
    args = parser.parse_args()

    replay_handler = create_training_assistant_replay_handler("http://{}:{}".format(HOST, PORT))
    replay = sc2reader.load_replay(args.replay_path[0])
    asyncio.get_event_loop().run_until_complete(replay_handler.handle_replay(replay))

if __name__ == '__main__':
    main()