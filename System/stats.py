import matplotlib.pyplot as plt
import logging
import csv
import settings

logger = logging.getLogger()
logger.setLevel('INFO')


class Stats:
    def __init__(self, path: str) -> None:
        """Loads settings from json.
        Args:
            path (str): Path to file.
        """
        self.content = settings.Configuration().load_settings(path)
        self.hist = self.content['hist']
        self.stats = self.content['statistics']

    def write_stats(self, cores: int, time: float) -> None:
        """Writes statistics in csv.
        Args:
            cores (int): Number of cores.
            time (float): Execution time.
        """
        try:
            with open(self.stats, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([cores, time])
            logging.info(f' Stats write to file {self.stats}')
        except OSError as err:
            logging.warning(f' Stats is not write\nError {err}')
            raise

    def load_stats(self) -> dict:
        """Loads statistics from csv.
        Returns:
            dict: Statistics.
        """
        try:
            with open(self.stats, "r", newline="") as f:
                read = csv.reader(f)
                list_stats = list(read)
                logging.info(f' Stats read from file {self.stats}')
        except OSError as err:
            logging.warning(f' Stats is not read\nError {err}')
            raise
        stats = {}
        for i in list_stats:
            cores, time = i
            stats[int(cores)] = float(time)
        logging.info('Stats is uploaded')
        return stats

    def draw_histogram(self, statistics: dict) -> plt:
        """Creates a histogram based on the data.
        Args:
            statistics (dict): Statistical data.
        Returns:
            plt: Histogram.
        """
        figure = plt.figure(figsize=(30, 5))
        plt.ylabel("Running time")
        plt.xlabel("Number of cores")
        plt.title("Addiction of running time on the number of cores")
        x = statistics.keys()
        y = statistics.values()
        plt.bar(x, y, color="green", width=0.25)
        plt.show(block=False)
        logging.info(' Histogram is constructed')
        return figure

    def save_histogram(self, figure: plt) -> None:
        """Saves the histogram image.
        Args:
            figure (plt): Histogram.
        """
        try:
            figure.savefig(self.hist)
            logging.info('Image saved successfully.')
        except OSError as err:
            logging.warning(f' Image is not saved\nError {err}')
            raise
