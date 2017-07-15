import sc2replaynotifier

from sc2trainingassistant.replayhandler import create_training_assistant_replay_handler

HOST = "localhost"
PORT = 32332


def main():
    replay_handler = create_training_assistant_replay_handler("http://{}:{}".format(HOST, PORT))
    replay_notifier = sc2replaynotifier.create_replay_notifier(replay_handler)

    replay_notifier.handle_replays()

if __name__ == '__main__':
    main()