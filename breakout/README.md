# Breakout Room Setup

Place files inside this directory using whatever naming scheme you want.

Each file should contain the names of the breakout rooms, each on a line by itsef.

For example, you could have a file "seminar-start.txt" containing:

```text
# You can commment your breakout text files
#
Virtual Cafe 1
Virtual Cafe 2
Virtual Cafe 3
Virtual Cafe 4
Virtual Cafe 5

# Empty lines are also ignored
#
Seminar Leader Room 1
Seminar Leader Room 2
```

Then invoke the `zoom-manager` application like this:

```bash
./zoom-manage breakout create breakout/seminar-start.txt
```
