# Chase in the maze solution


### Additional assumptions that were not specified in assignment
- Exit field doesn't block monster's path and it can step on it to reach the player's position
- If player chooses to wait in place during his turn, it still counts as taking a step for the end result

### Requirements
- Python >3.10

### Running from source
Program doesn't use any dependencies that aren't in standard library of python. So to run it you simply can do
```bash
python main.py
```
By default if `input.txt` file is present in directory, the program will take input from it. If the file is not present it will wait to take input from stdin that is accurate with assignment specification so for example:
```text
3 3
E..
.#.
P.M
```
