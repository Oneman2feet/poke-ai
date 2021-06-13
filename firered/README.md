# Prerequisites

- `pip install pathfinding`

# Set up ROM

1. in integration ui app, click game > integrate and choose rom and keep default name
2. If you don't already have a state file, start the game and go to game > save state at the point where you want it to start
3. copy the `GameName` folder from contrib to stable `<Python37Path>\site-packages\retro\data`
4. load the rom with the command `python3 -m retro.import <Python37Path>\site-packages\retro\data\stable\<GameName>` and use the path of the directory you copied
5. copy paste the scenario, data, and state files to the `GameName` directory
6. in the python script, change the game name to match
7. run the python script!

# Record and playback

1. install [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) and put in PATH
2. `python3 -m retro.scripts.playback_movie <bk2file>` to render video