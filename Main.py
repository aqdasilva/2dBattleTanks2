import arcade
import self as self

import TiledWindow
import json
from network import Network

HOST = "10.0.0.91"  # replace with your IP ADDRESS
PORT = 8888

class GameStuf(arcade.View):
    def __init__(self):
        super().__init__()
        self.server = Network()



def main():
    window: TiledWindow.TiledWindow = TiledWindow.TiledWindow()
    window.setup()

    arcade.run()


if __name__ == '__main__':
    main()
