import matplotlib.pyplot as plt
import logging
import csv

logger = logging.getLogger()
logger.setLevel('INFO')


class Stats:
    def __init__(self, path: str) -> None:
        self.stats_path = path

    def write_stats(self, cores: int, time: float) -> None:
        try:
            with open(self.stats_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([cores, time])
            logging.info(f' Stats write to file {self.stats_path}')
        except OSError as err:
            logging.warning(f' Stats is not write\nError {err}')
            raise 

    def load_stats(self) -> dict:
        try:
            with open(self.stats_path, "r", newline="") as f:
                read = csv.reader(f)
                list_stats = list(read)
                logging.info(f' Stats read from file {self.stats_path}')
        except OSError as err:
            logging.warning(f' Stats is not read\nError {err}')
            raise 
        stats = {}
        for i in list_stats:
            cores, time = i
            stats[int(cores)] = float(time)
        logging.info('Stats is uploaded')
        return stats

    def draw_histogram(statistics: dict) -> plt:
        figure = plt.figure(figsize=(30, 5))
        plt.ylabel("Running time")
        plt.xlabel("Number of cores")
        plt.title("Addiction of running time on the number of cores")
        x = statistics.keys()
        y = statistics.values()
        plt.bar(x, y, color="green", width=0.05)
        plt.show(block = False)    
        logging.info(' Histogram is constructed')
        return figure
