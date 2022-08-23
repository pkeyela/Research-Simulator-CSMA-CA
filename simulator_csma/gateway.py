# DEPRECATED: The gateway no longer exists as independent unit
class Gateway:
    def __init__(self, parameters, debug=False):
        self.parameters = parameters
        self.debug = debug
        self.time_unit = parameters['time_unit']
        self.T_rts = parameters['T_rts']
        self.T_cts = parameters['T_cts']
        self.T_data = parameters['T_data']
        self.T_ack = parameters['T_ack']
        self.error_accuracy = 0.00000001
        self.state_time = 0
        self.simulation_time = 0
        self.state = 'idle'
        self.node = -1
        self.stats = {
            'arrived_rts': 0,
            'collided_rts': 0,
            'served_rts': 0
        }
        self.stacktrace = []
        self.set_state('idle')

    def get_state(self):
        return self.state

    def set_state(self, state, node=-1):
        if node != -1:
            self.node = node
        assert state in ['idle', 'rts', 'cts', 'data', 'ack']
        if state == 'idle':
            self.state_time = 0
        elif state == 'rts':
            self.state_time = self.T_rts
        elif state == 'cts':
            self.state_time = self.T_cts
        elif state == 'data':
            self.state_time = self.T_data
        elif state == 'ack':
            self.state_time = self.T_ack
        self.state = state
        if state != 'idle':
            self.add_stacktrace(state)

    def refresh_state(self):
        self.set_state(self.get_state())

    def add_stacktrace(self, state):
        self.stacktrace.append([state, self.simulation_time])

    def update_stacktrace(self):
        self.stacktrace[-1].append(self.simulation_time)
        self.stacktrace[-1].append(self.stacktrace[-1][2] - self.stacktrace[-1][1])

    def clear_stacktrace(self):
        if self.debug and not True:
            print(f'Gateway stacktrace:')
            for data in self.stacktrace:
                print(f'State: {data[0]}, from {data[1]} to {data[2]}; total {data[3]}')
        self.stacktrace = []

    def update_cycle(self):
        self.simulation_time += self.time_unit
        self.state_time -= self.time_unit
        # self.state_time = np.round(self.state_time, 5)
        if self.state_time < self.error_accuracy:
            if self.get_state() != 'idle':
                self.update_stacktrace()
            # Если сидим в idle, ничего не делаем, слушаем
            if self.get_state() == 'idle':
                pass

            elif self.get_state() == 'rts':
                self.set_state('cts')

            elif self.get_state() == 'cts':
                # self.set_state('data')
                pass

            elif self.get_state() == 'data':
                self.set_state('ack')

            elif self.get_state() == 'ack':
                self.clear_stacktrace()
                self.set_state('idle')
                self.node = -1
                self.stats['served_rts'] += 1
