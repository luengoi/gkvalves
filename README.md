# Gorod Krovi Valve Solver
During the Easter Egg of the Call of Duty: Black Ops 3 Zombies map *Gorod Krovi*, we need to solve one step that
requires connecting all the valves so that the air can flow from the green-lit valve to the valve containing the
cylinder.

Each valve is connected to three other valves as shown in the following image.

![Valve Connections](/resources/gk-valves.png)

We can view the valves as an *Undirected Graph* and the solution is to find a [Hamiltonian Path](https://en.wikipedia.org/wiki/Hamiltonian_path)
(i.e: the path that visits each vertex exactly once) starting from the green-lit valve and finishing at the valve
that contains the cylinder.

## Usage

Clone the repository and run the module. You must specify the location of the green valve and the location of the
valve containing the cylinder. These are the available locations:

```
0. Armory
1. Dept. Store
2. Dragon Command
3. Supply Depot
4. Infirmary
5. Tank Factory
```

The script will find a valid path that connects all valves and will tell you the position of each valve.

```bash
# cd into the cloned repository directory
cd gk-valves
python -m gkvalves 0 1  # find path for Armory (green) -> Dept. Store (cylinder)

Armory: 1
Supply Depot: 3
Tank Factory: 1
Infirmary: 3
Dragon Command: 2
```

**TODO**: I will try to add an integration to a package manager for an easier installation.
