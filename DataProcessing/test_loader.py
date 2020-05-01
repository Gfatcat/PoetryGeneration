from loader import DataLoader


class Config(object):
    filename = 'poetry.csv'
    is_evaluate = True
    batch_size = 64
    train_rate = 0.8

config = Config()
data_loader = DataLoader(config)
data_loader.get_dataset()
pass
