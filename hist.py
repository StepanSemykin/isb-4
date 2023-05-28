import matplotlib.pyplot as plt
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


def draw_histogram(statistics: dict) -> plt:
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel("Running time")
    plt.xlabel("Number of cores")
    plt.title("Addiction of running time on the number of cores")
    x = statistics.keys()
    y = statistics.values()
    plt.bar(x, y, color="green", width=0.05)
    plt.show(block = False)    
    logging.info(' Histogram is constructed')
    return fig
