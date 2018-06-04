class Args():
    train_data = None
    test_data = None
    batch_size = None
    epoch = None
    hidden_dim = None
    optimizer = None
    CRF = None
    lr = None
    clip = None
    dropout = None
    update_embedding = None
    pretrain_embedding = None
    embedding_dim = None
    shuffle = None
    mode = None
    demo_model = None
    pre_url = None
    def __init__(self):
        self.pre_url = 'Load'
        self.train_data = 'Show_KG/Load/data_path'
        self.test_data = 'Show_KG/Load/my_data_path'
        # self.train_data = 'data_path'
        # self.test_data = 'my_data_path'
        self.batch_size = 32
        self.epoch = 60
        self.hidden_dim = 300
        self.optimizer = 'Adam'
        self.CRF = True
        self.lr = 0.001
        self.clip = 5.0
        self.dropout = 0.5
        self.update_embedding = True
        self.pretrain_embedding = 'random'
        self.embedding_dim = 300
        self.shuffle = True
        self.mode = 'demo'
        self.demo_model = '1525046802'