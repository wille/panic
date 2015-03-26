import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument("-b", "--bport", dest = "buttonport")
argparse.add_argument("-s", "--sport", dest = "signalport")
args = argparse.parse_args()

global button_port
button_port = int(args.buttonport or 8080)

global signal_port
signal_port = int(args.signalport or 1301)

if __name__ == "__main__":
    pass