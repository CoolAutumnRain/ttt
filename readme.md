# Tic and tac on my toe
## **Note: readme requires at least 74 lines width to process correctly!**

## Running the program
It's set up to be ran as a python-program, just run `tic_tac_toe.py` and it should work flawlessly.
Respond to the queries asked by the program with the indicated numbers. Coordinates for placing tics or tacs read the *first* and *final* value in the input, so inputting the coordinates ``"1, 2, 3"`` will be read as position 1,3.
## Simplified program-flow overview
```
                        user choice
      <----------------------|--------------------->
New game(1)        Load games/replays(2)        statistics(3)
    |                        |                      |
boardsize     (1)won/draws  <-> in-progress(2)      |
    |               |               |               |
game loop**       boardsize*       boardsize*     boardsize*
    |               |               |               |
win/draw+save       v               v               v
    >---------------->------|------<---------------<
                        user choice
```
*When the program asks for boardsize after the load-command or statistics-command has been given, it's asking for the boardsize as a search-filter. **This means statistics shown are on a per size basis and not overall!**

** Not shown in the flow-chart is the `Save` command which saves the current game and returns to `user choice` in the flow chart.


## Flow control
`Exit` can be used at any time to exit the program with code(0).

`Save` can be used during a game that's in progress to save the current game.

## Incorrect input
Every input should be protected from `Exceptions`. It will either call the main function(effectively going back to `user choice` in the flowchart above) *or* it will ask for a new input and it will not break this loop unless `Exit` is given.

## Local Data
if no local file called `tic_tac_toe_data.txt` exists, it will be created upon the program finishing *and* reaching a win state **OR** if the `Save` command is given during a game.
The program should be able to handle any and all read errors from the data-file not being present.


