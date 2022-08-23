import time
import os
import utils
from simulator import Simulator
from settings import Settings


class MultiSimulation:
    def __init__(self):
        settings = Settings()
        self.simulation_params = settings.get_simulation_params()
        self.debug_params = settings.get_debug_params()

    def run_simulation(self):
        # Disable debug params in multi simulation (huge disk loads)
        # To debug use single simulation
        self.debug_params['log'] = False
        self.debug_params['stacktrace'] = False

        print(f"Multi simulation with 1...{self.simulation_params['node_number']} nodes started!")
        start_time = time.time()

        data_to_save = []
        folder_to_save = "results"
        # Привязка ко времени: каждый результат сохраняется отдельно (формат: D year-month-day T hours-minutes-seconds)
        filename_to_save = f"{time.strftime('D %Y-%m-%d T %H-%M-%S')}.csv"

        for node in range(1, self.simulation_params['node_number'] + 1):
            simulator = Simulator(self.simulation_params, nodes=node, debug=self.debug_params)
            stats = simulator.start(self.simulation_params['total_simulation_time'])
            time.sleep(0.5)  # To fix visual glitches with progress bar
            if node == 1:
                data_to_save.append(list(stats.keys()))  # Save headers for future csv file
            data_to_save.append(list(stats.values()))

        if not os.path.exists(folder_to_save):
            os.mkdir(folder_to_save)

        # Here we save our data to csv
        utils.save_to_csv(os.path.join(folder_to_save, filename_to_save), data_to_save)

        finish_time = time.time()
        print(f"Simulation finished! Results saved in '{os.path.join(folder_to_save, filename_to_save)}'")
        print('Total simulation time:', finish_time - start_time)
