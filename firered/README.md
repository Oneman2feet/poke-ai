1. in integration ui app, click game > integrate and choose rom and keep default name
2. start the game and go to game > save state when you are outside the house. save the file as "Level1" in the <GameName> folder
3. copy the <GameName> folder from contrib to stable (<PythonPath>\Python37\site-packages\retro\data)
4. load the rom with the command (python3 -m retro.import <PythonPath>\Python37\site-packages\retro\data\stable\<GameName>) and use the path of the directory you copied
5. copy paste the scenario, data, and game files to the <GameName> directory
6. in game.py, change the game name to match the new game
6. run the python script with (python <PythonPath>\Python37\site-packages\retro\data\stable\<GameName>\game.py)
