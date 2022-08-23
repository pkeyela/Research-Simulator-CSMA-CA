# simulator_csma
Run **main.py** to simulate CSMA/CA protocol with specific number of nodes. Use 'calculate_all_nodes' boolean 
variable to choose which nodes to simulate. If True, simulator will go through 1 to 'node_number' param defined 
below. If False, it will simulate only 'node_number' number of nodes (faster, easy to debug or test new feature).

File **single_simulation.py** describes the simulation with 'calculate_all_nodes = False'.

File **multi_simulation.py** describes the simulation with 'calculate_all_nodes = True' and saves the result in 
'results/multi_simulation results.csv' (by default).

**settings.py** describes all default settings variables, which will be used if other not specified in **main.py**.

**simulator.py** contains fundamental logic of simulation, and **node.py** describes Node class.

File **multiprocess_simulation.py** is responsible for long-time simulations with multithreading (faster 
simulations, but more energy consuming and causes lags). I don't recommend using it if you are planning to 
use PC/laptop when simulation is running. I usually use it on PC at nights when I need different simulations 
by the morning. It also has the advantage of sending VK message about state of simulation process (**vk_log.py**). 
