
import os
import logging
import torch

def set_logging(name=None, verbose=True):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    # Sets level and returns logger
    rank = int(os.getenv('RANK', -1))  # rank in world for Multi-GPU trainings
    logging.basicConfig(format="%(message)s", level=logging.INFO if (verbose and rank in (-1, 0)) else logging.WARNING)
    return logging.getLogger(name)

LOGGER = set_logging(__name__)  # define globally (used in train.py, val.py, detect.py, etc.)

LOGGERS = ('csv', 'tb')

CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if CUDA else 'cpu'

LOGGER_TENSORBOARD = 'tb'


class Loggers():
    def __init__(self, hyp):
        self.type = hyp['logger']['type']
        self.epochs = hyp['train']['epochs']
        self.writer = None
        if self.type == LOGGER_TENSORBOARD:
            from torch.utils.tensorboard import SummaryWriter
            self.writer = SummaryWriter(hyp['data']['save_dir'])


    def on_train_epoch_end(self, epoch, metrics):
        LOGGER.info(f'fin epoch {epoch}/{self.epochs}, metrics: {metrics}')
        if self.type == LOGGER_TENSORBOARD:
            for key in metrics.keys():
                self.writer.add_scalar(key, metrics[key], epoch)