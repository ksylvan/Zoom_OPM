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

NOTE: The `zoom-manager breakout create` command will set the
`Assign manually` option. Once the rooms are created, it is
recommended that you open and close the rooms immediately. This
is due to a bug, where if you click on the `Breakout Room` Zoom
Status menu, it will lose some of your room setup.
