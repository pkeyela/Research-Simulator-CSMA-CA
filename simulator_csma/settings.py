class Settings:
    def __init__(self):
        # Default parameters, if something is not specified
        self.simulation_parameters = {
            'total_simulation_time': 30_000_000,  # number of time ticks
            'total_simulations': 10,  # quantity
            'time_unit': 3.2,  # ns
            'probability_of_having_data': 1.0,  # probability
            'sphere_radius': 2,  # meters
            'node_number': 30,  # quantity
            'retry_number': 3,  # quantity
            'T_max': 12,  # quantity
            'sensing_backoff': True,  # boolean
            'sensing_out': True,  # boolean
            'sensing_idle': False,  # boolean
            'T_idle': 8 * 20 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
            'T_rts': 8 * 20 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
            'T_cts': 8 * 20 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
            'T_data': 8 * 100 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
            'T_ack': 8 * 20 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
            'T_out': 8 * 20 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
            'T_wait': 8 * 20 / (50_000_000_000 / 1_000_000_000),  # bits / (bits / ns), ns
        }

        self.debug_parameters = {
            'log': False,
            'stacktrace': False,
            'log_filename': 'simulation_log.txt',
            'stacktrace_filename': 'stacktrace.txt',
            'show_progress_bar': True,
        }

    def get_simulation_params(self):
        return self.simulation_parameters

    def get_debug_params(self):
        return self.debug_parameters
