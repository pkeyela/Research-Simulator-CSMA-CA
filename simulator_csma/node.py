import numpy as np


class Node:
    def __init__(self, num, parameters, debug):
        self.num = num
        self.pa = parameters['probability_of_having_data']
        self.retry_number = parameters['retry_number']
        self.debug = debug
        self.time_unit = parameters['time_unit']
        self.T_idle = parameters['T_idle']
        self.T_rts = parameters['T_rts']
        self.T_cts = parameters['T_cts']
        self.T_data = parameters['T_data']
        self.T_ack = parameters['T_ack']
        self.T_out = parameters['T_out']
        self.T_wait = parameters['T_wait']
        self.T_max = parameters['T_max']
        self.state = 'idle'
        self.next_state = ''
        self.channel_free = True
        self.collision = False
        self.ignored = False
        self.ignored_data = False
        self.error_accuracy = 0.00000001
        self.state_time = self.T_idle
        self.attempt = 1
        self.max_attempt = parameters['retry_number'] + 1

        self.message = None
        self.simulation_time = 0
        self.cycle_time = 0
        self.idle_time = 0
        self.bo_time = 0
        self.rts_time = 0
        self.data_time = 0
        self.wait_time = 0
        self.cts_time = 0
        self.ack_time = 0
        self.out_time = 0
        self.tau_prop = 0
        # Next 3 params are used to calculate statistic through one cycle [new]
        self.rts_failed = 0
        self.sensing_performed = 0
        self.cts_sensed = 0

        # TODO: simplify statistics (некоторые данные излишни)
        self.stats = {
            'rts_not_received': 0,  # by gateway, event A1
            'rts_received': 0,  # by gateway, event A2
            'channel_is_free': 0,  # event A3
            'channel_is_busy': 0,  # event A4
            'data_failure': 0,  # event A5
            'data_success': 0,  # event A6
            'cycle_times': [],
            'idle_times': [],
            'bo_times': [],
            'rts_times': [],
            'data_times': [],
            'ack_times': [],
            'cts_times': [],
            'out_times': [],
            'wait_times': [],
        }
        self.stacktrace = [["idle", self.simulation_time]]

    def get_state(self):
        return self.state

    def set_state(self, state):
        assert state in ['idle', 'bo', 'rts', 'out', 'wait', 'cts', 'data', 'ack']

        self.update_stacktrace(state)
        if state == 'idle':
            self.finish_cycle()
            self.state_time = self.T_idle

        elif state == 'bo':
            # If we came to BACKOFF from IDLE or OUT, start it from 1, else if we came here from WAIT, start it from 0
            self.state_time = np.random.randint(1, 2**self.attempt * self.T_max + 1) * self.T_rts  # 1

        # Если попали в RTS
        elif state == 'rts':
            self.state_time = self.T_rts
        # Если попали в WAIT
        elif state == 'wait':
            self.state_time = self.T_wait
        # Если попали в DATA
        elif state == 'data':
            self.state_time = self.T_data
        # Если попали в CTS
        elif state == 'cts':
            self.state_time = self.T_cts
            self.stats['rts_received'] += 1
        elif state == 'ack':
            self.state_time = self.T_ack
        # Если попали в OUT
        elif state == 'out':
            if self.collision and self.ignored and self.ignored_data:
                print("Strange collision #1. Observe!")
            if self.ignored and self.ignored_data:
                print("Strange collision #2. Observe!")
            if self.collision or self.ignored or self.ignored_data:
                self.stats['rts_not_received'] += 1
                self.rts_failed += 1
                self.attempt += 1
            self.collision = False
            self.ignored = False
            self.ignored_data = False
            self.state_time = self.T_out
        self.state = state

    def add_stacktrace(self, state):
        self.stacktrace.append([state, self.simulation_time])

    def update_stacktrace(self, state):
        self.stacktrace[-1].append(self.simulation_time)
        self.stacktrace[-1].append(self.stacktrace[-1][2] - self.stacktrace[-1][1])
        self.stacktrace.append([state, self.simulation_time])

    def clear_stacktrace(self):
        # TODO: recode stacktrace system (current version is difficult)
        if self.debug['stacktrace']:
            stacktrace_file = open(self.debug['stacktrace_filename'], "a")
            stacktrace_file.write(f'\nNode {self.num} stacktrace:\n')
            for data in self.stacktrace[:-1]:
                stacktrace_file.write(f'State: {data[0]}, from {data[1]} to {data[2]}; total {data[3]}\n')
            stacktrace_file.close()
        self.stacktrace = [["idle", self.simulation_time]]

    def clear_statistic(self):
        for k in self.stats.keys():
            if type(self.stats[k]) == int:
                self.stats[k] = 0
            elif type(self.stats[k] == list):
                self.stats[k] = []

    def finish_cycle(self):
        self.clear_stacktrace()
        self.attempt = 1
        self.stats['idle_times'].append(self.idle_time)
        self.idle_time = 0
        self.stats['cycle_times'].append(self.cycle_time)
        self.cycle_time = 0
        if self.get_state() != "idle":
            self.stats['bo_times'].append(self.bo_time)
            self.bo_time = 0
            self.stats['rts_times'].append(self.rts_time)
            self.rts_time = 0
            self.stats['data_times'].append(self.data_time)
            self.data_time = 0
            self.stats['wait_times'].append(self.wait_time)
            self.wait_time = 0
            self.stats['cts_times'].append(self.cts_time)
            self.cts_time = 0
            self.stats['ack_times'].append(self.ack_time)
            self.ack_time = 0
            self.stats['out_times'].append(self.out_time)
            self.out_time = 0
        self.rts_failed = 0
        self.sensing_performed = 0
        self.cts_sensed = 0

    def update_time(self):
        self.simulation_time += self.time_unit
        self.cycle_time += self.time_unit
        self.state_time -= self.time_unit

        # Добавляем такт к текущему состоянию
        if self.get_state() == 'idle':
            self.idle_time += self.time_unit
        elif self.get_state() == 'bo':
            self.bo_time += self.time_unit
        elif self.get_state() == 'rts':
            self.rts_time += self.time_unit
        elif self.get_state() == 'data':
            self.data_time += self.time_unit
        elif self.get_state() == 'wait':
            self.wait_time += self.time_unit
        elif self.get_state() == 'cts':
            self.cts_time += self.time_unit
        elif self.get_state() == 'ack':
            self.ack_time += self.time_unit
        elif self.get_state() == 'out':
            self.out_time += self.time_unit
