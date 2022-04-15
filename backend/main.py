from Bot.bot import runBot
from routes import runFlask
from threading import Thread
import sys


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg != "bot":
        print("Initializing Server")
        botThr = Thread(target=runFlask, daemon=True, args=[arg])
        botThr.start()
        print("initializing Bot")
        runBot()
    else:
        runBot(standalone=True)
