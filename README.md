# Gorod Krovi Valve Solver
During the Easter Egg of the Call of Duty: Black Ops 3 Zombies map *Gorod Krovi*, we need to solve one step that
requires connecting all the valves so that the air can flow from the green-lit valve to the valve containing the
cylinder.

Each valve is connected to three other valves as shown in the following image.

![Valve Connections](/resources/gk-valves.png)

We can view the valves as an *Undirected Graph* and the solution is to find a [Hamiltonian Path](https://en.wikipedia.org/wiki/Hamiltonian_path)
(i.e: the path that visits each vertex exactly once) starting from the green-lit valve and finishing at the valve
that contains the cylinder.
