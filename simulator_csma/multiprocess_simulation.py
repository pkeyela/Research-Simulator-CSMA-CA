import os
import time
import numpy as np
from multiprocessing import Process
from simulator import Simulator
from settings import Settings
import vk_log
import utils


class MultiprocessSimulation:
    def __init__(self):
        settings = Settings()
        self.simulation_params = settings.get_simulation_params()
        self.debug_params = settings.get_debug_params()
        self.threads_number = 5
        self.node_distribution = []

    def define_distribution_data(self):
        # Распределение, сколько узлов должен рассмотреть каждый поток для примерно одновременного завершения по времени
        nodes_list = np.arange(1, self.simulation_params['node_number'] + 1)
        nodes_distribution = []
        for i in range(self.threads_number):
            nodes_distribution.append([])
        i = 0
        for node in nodes_list:
            nodes_distribution[i].append(node)
            i += 1
            if i >= self.threads_number:
                i = 0
        print(nodes_distribution)
        return nodes_distribution

    def multiprocess(self, current_thread_number):
        thread_time = time.time()
        data_to_save = []
        headers = []
        for node in self.node_distribution[current_thread_number]:
            simulator = Simulator(self.simulation_params, nodes=node, debug=self.debug_params)
            stats = simulator.start(self.simulation_params['total_simulation_time'])
            if node == 1:
                headers = list(stats.keys())  # Save headers for future csv file
                np.save(f'temp_simulation_headers.npy', headers)
            data_to_save.append(list(stats.values()))
        finish_time = time.time()
        np.save(f'temp_simulation_{current_thread_number}.npy', np.array(data_to_save))
        print(f'Thread {current_thread_number + 1} has finished! Time: {finish_time - thread_time}')

    def run_simulation(self):
        self.debug_params['log'] = False
        self.debug_params['stacktrace'] = False

        self.node_distribution = self.define_distribution_data()

        print(f"Multi simulation with 1..{self.simulation_params['node_number']} nodes started!")
        start_time = time.time()

        data_to_save = []
        folder_to_save = "results"
        # Привязка ко времени: каждый результат сохраняется отдельно (формат: year-month-day hours:minutes)
        filename_to_save = f"mp {time.strftime('D %Y-%m-%d T %H-%M-%S')}.csv"

        processes = []
        all_data = []
        for current_thread_number in range(self.threads_number):
            processes.append(Process(target=self.multiprocess, args=(current_thread_number, )))

        for current_thread_number in range(self.threads_number):
            processes[current_thread_number].start()

        for current_thread_number in range(self.threads_number):
            processes[current_thread_number].join()

        for current_thread_number in range(self.threads_number):
            processes[current_thread_number].close()

        numpy_files = []
        for current_thread_number in range(self.threads_number):
            current_thread_file = f'temp_simulation_{current_thread_number}.npy'
            thread_data = np.load(current_thread_file)
            numpy_files.append(current_thread_file)
            for res in thread_data:
                all_data.append(list(res))

        header_file = 'temp_simulation_headers.npy'
        headers = np.load(header_file)
        numpy_files.append(header_file)

        if not os.path.exists(folder_to_save):
            os.mkdir(folder_to_save)

        all_data.sort()
        all_data.insert(0, headers)

        # Here we save our data to csv
        utils.save_to_csv(os.path.join(folder_to_save, filename_to_save), all_data)

        for file in numpy_files:
            os.remove(file)

        finish_time = time.time()
        print(f"Simulation finished! Results saved in '{os.path.join(folder_to_save, filename_to_save)}'")


if __name__ == '__main__':
    token = 'a5f92c3aa82877091fd3ba8a98f493b34d8355a0266b6bf5371268b9df05f78f8cdad25ace67a54448c0f'
    api_v = '5.101'
    vk = vk_log.Vk(token, api_v)
    uid = 0  # Vkontakte user id.
    # uid = 62619861  # Vkontakte id (Emil Khayrov). Don't uncomment this

    sim_start_time = time.time()
    # Отправить сообщение:
    vk.send_message(uid, f"New multiprocess simulation has started.")

    start_1_time = time.time()

    mp_sim = MultiprocessSimulation()
    mp_sim.simulation_params['total_simulation_time'] = 100_000
    mp_sim.simulation_params['total_simulations'] = 20
    mp_sim.simulation_params['probability_of_having_data'] = 1
    mp_sim.simulation_params['time_unit'] = 3
    mp_sim.simulation_params['T_idle'] = 3
    mp_sim.simulation_params['T_rts'] = 3
    mp_sim.simulation_params['T_cts'] = 3
    mp_sim.simulation_params['T_data'] = 3
    mp_sim.simulation_params['T_ack'] = 3
    mp_sim.simulation_params['T_out'] = mp_sim.simulation_params['T_data'] + mp_sim.simulation_params['T_ack']
    mp_sim.simulation_params['T_wait'] = mp_sim.simulation_params['T_data'] + mp_sim.simulation_params['T_ack']

    mp_sim.simulation_params['T_max'] = 12
    mp_sim.simulation_params['node_number'] = 50
    mp_sim.simulation_params['retry_number'] = 3

    mp_sim.simulation_params['sensing_backoff'] = True
    mp_sim.simulation_params['sensing_out'] = True
    mp_sim.simulation_params['sensing_idle'] = False

    mp_sim.debug_params['stacktrace'] = False
    mp_sim.debug_params['log'] = False
    mp_sim.debug_params['show_progress_bar'] = False  # it is broken when several processes are running
    mp_sim.run_simulation()

    info_message = f"Simulation part 1 has finished. It took {int(time.time() - start_1_time)} seconds"
    vk.send_message(uid, info_message)

    # start_2_time = time.time()
    #
    # mp_simulation = MultiprocessSimulation()
    # mp_simulation.simulation_params['total_simulation_time'] = 30_000
    # mp_simulation.simulation_params['total_simulations'] = 50
    # mp_simulation.simulation_params['probability_of_having_data'] = 1
    # mp_simulation.simulation_params['time_unit'] = 3
    # mp_simulation.simulation_params['T_idle'] = 3
    # mp_simulation.simulation_params['T_rts'] = 3
    # mp_simulation.simulation_params['T_cts'] = 3
    # mp_simulation.simulation_params['T_data'] = 3
    # mp_simulation.simulation_params['T_ack'] = 3
    # mp_simulation.simulation_params['T_out'] = 3
    # mp_simulation.simulation_params['T_wait'] = 3
    #
    # mp_simulation.simulation_params['T_max'] = 12
    # mp_simulation.simulation_params['node_number'] = 50
    # mp_simulation.simulation_params['retry_number'] = 3
    #
    # mp_simulation.simulation_params['sensing_backoff'] = True
    # mp_simulation.simulation_params['sensing_out'] = True
    # mp_simulation.simulation_params['sensing_idle'] = False
    #
    # mp_simulation.debug_params['stacktrace'] = False
    # mp_simulation.debug_params['log'] = False
    # mp_simulation.debug_params['show_progress_bar'] = False  # it is broken when several processes are running
    # mp_simulation.run_simulation()
    #
    # info_message = f"Simulation part 2 has finished. It took {int(time.time() - start_2_time)} seconds"
    # vk.send_message(uid, info_message)

    sim_finish_time = time.time()
    overall_time = sim_finish_time - sim_start_time
    seconds = int(overall_time % 60)
    minutes = int(overall_time / 60) % 60
    hours = int(overall_time / 60 / 60) % 24
    time_formatted = f"{str(hours) + 'h ' if hours else ''}{str(minutes) + 'm ' if minutes else ''}{str(seconds) + 's' if seconds else ''}"

    info_message = f"All simulations are done! Overall simulation time {time_formatted}"
    print(info_message)
    vk.send_message(uid, info_message)
