from single_simulation import SingleSimulation
from multi_simulation import MultiSimulation

if __name__ == '__main__':
    # If True, simulator will go through all nodes from 1 to 'node_number'.
    # If False, simulator will calculate statistics only for 'node_number'.
    calculate_all_nodes = False
    if calculate_all_nodes:
        simulation = MultiSimulation()
    else:
        simulation = SingleSimulation()


    # Simulation is performing 'total_simulations' times with 'total_simulation_time' ticks in each simulation.
    # (Bigger value, more accurate results. Ideal params: 100_000 & 50 or more, but simulation will last long enough)
    simulation.simulation_params['total_simulation_time'] = 100_000      # number of ticks in one simulation
    simulation.simulation_params['total_simulations'] = 60              # number of simulations to average

    simulation.simulation_params['probability_of_having_data'] = 1.0
    simulation.simulation_params['time_unit'] = 3
    simulation.simulation_params['T_idle'] = 3
    simulation.simulation_params['T_rts'] = 3
    simulation.simulation_params['T_cts'] = 3
    simulation.simulation_params['T_data'] = 3
    simulation.simulation_params['T_ack'] = 3
    simulation.simulation_params['T_out'] = 6
    simulation.simulation_params['T_wait'] = 6

    simulation.simulation_params['T_max'] = 12
    simulation.simulation_params['node_number'] = 2
    simulation.simulation_params['retry_number'] = 3

    simulation.simulation_params['sensing_backoff'] = True
    simulation.simulation_params['sensing_out'] = True

    # Debug doesn't work in multi simulation (to prevent flood in output)
    # 'stacktrace' param traces every state of node in stacktrace.txt
    simulation.debug_params['stacktrace'] = True
    # log will write readable info in simulation_log.txt
    simulation.debug_params['log'] = True
    # Show progress bar of simulation (recommended)
    simulation.debug_params['show_progress_bar'] = True

    simulation.run_simulation()
