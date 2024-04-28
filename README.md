# boca-utils
Collection of tools to test and profile solutions for problems packaged for the BOCA (Boca Online Contest Administrator)

## Runner

Runner lets you test your programs against test files from BOCA archives. The program only needs the "inputs" and "outputs" folders.

```
usage: runner.py [-h] -p PROGRAM [-V {1,2,3}]

Runner build your program and tests it against test inputs (placed in the inputs folder) and their respective outputs (placed in the outputs folder)

options:
  -h, --help            show this help message and exit
  -p PROGRAM, --program PROGRAM
                        The main source file of your program
  -V {1,2,3}, --verbosity {1,2,3}
                        This program has 3 levels of verbosity. 1 is the default and 3 is the highest
```
