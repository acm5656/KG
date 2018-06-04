from Show_KG.Load.model import BiLSTM_CRF
import numpy as np
import os, argparse, time, random
import tensorflow as tf
from Show_KG.Load.utils import str2bool, get_logger, get_entity
from Show_KG.Load.data import read_corpus, read_dictionary, tag2label, random_embedding
from Show_KG.Load.Args import Args
## hyperparameters
# parser = argparse.ArgumentParser(description='BiLSTM-CRF for Chinese NER task')
# parser.add_argument('--train_data', type=str, default='data_path', help='train data source')
# parser.add_argument('--test_data', type=str, default='my_data_path', help='test data source')
# parser.add_argument('--batch_size', type=int, default=32, help='#sample of each minibatch')
# parser.add_argument('--epoch', type=int, default=60, help='#epoch of training')
# parser.add_argument('--hidden_dim', type=int, default=300, help='#dim of hidden state')
# parser.add_argument('--optimizer', type=str, default='Adam', help='Adam/Adadelta/Adagrad/RMSProp/Momentum/SGD')
# parser.add_argument('--CRF', type=str2bool, default=True, help='use CRF at the top layer. if False, use Softmax')
# parser.add_argument('--lr', type=float, default=0.001, help='learning rate')
# parser.add_argument('--clip', type=float, default=5.0, help='gradient clipping')
# parser.add_argument('--dropout', type=float, default=0.5, help='dropout keep_prob')
# parser.add_argument('--update_embedding', type=str2bool, default=True, help='update embedding during training')
# parser.add_argument('--pretrain_embedding', type=str, default='random', help='use pretrained char embedding or init it randomly')
# parser.add_argument('--embedding_dim', type=int, default=300, help='random init char embedding_dim')
# parser.add_argument('--shuffle', type=str2bool, default=True, help='shuffle training data before each epoch')
# parser.add_argument('--mode', type=str, default='demo', help='train/test/demo')
# parser.add_argument('--demo_model', type=str, default='1525046802', help='model for test and demo')
# args = parser.parse_args()

args = Args()
word2id = read_dictionary(os.path.join('.', args.train_data, 'word2id.pkl'))
if args.pretrain_embedding == 'random':
    embeddings = random_embedding(word2id, args.embedding_dim)
else:
    embedding_path = 'pretrain_embedding.npy'
    embeddings = np.array(np.load(embedding_path), dtype='float32')

if args.mode != 'demo':
    train_path = os.path.join('.', args.train_data, 'train_data')
    test_path = os.path.join('.', args.test_data, 'train_data_my_1')
    train_data = read_corpus(train_path)
    test_data = read_corpus(test_path)
    test_size = len(test_data)

## paths setting
timestamp = str(int(time.time())) if args.mode == 'train' else args.demo_model
output_path = os.path.join('.', args.train_data+"_save", timestamp)
if not os.path.exists(output_path): os.makedirs(output_path)
summary_path = os.path.join(output_path, "summaries")
if not os.path.exists(summary_path): os.makedirs(summary_path)
model_path = os.path.join(output_path, "checkpoints/")
if not os.path.exists(model_path): os.makedirs(model_path)
ckpt_prefix = os.path.join(model_path, "model")
result_path = os.path.join(output_path, "results")
if not os.path.exists(result_path): os.makedirs(result_path)
log_path = os.path.join(result_path, "log.txt")
get_logger(log_path).info(str(args))

## training model
if args.mode == 'train':
    model = BiLSTM_CRF(batch_size=args.batch_size, epoch_num=args.epoch, hidden_dim=args.hidden_dim, embeddings=embeddings,
                       dropout_keep=args.dropout, optimizer=args.optimizer, lr=args.lr, clip_grad=args.clip,
                       tag2label=tag2label, vocab=word2id, shuffle=args.shuffle,
                       model_path=ckpt_prefix, summary_path=summary_path, log_path=log_path, result_path=result_path,
                       CRF=args.CRF, update_embedding=args.update_embedding)
    model.build_graph()

    ## hyperparameters-tuning, split train/dev
    # dev_data = train_data[:5000]; dev_size = len(dev_data)
    # train_data = train_data[5000:]; train_size = len(train_data)
    # print("train data: {0}\ndev data: {1}".format(train_size, dev_size))
    # model.train(train_data, dev_data)

    ## train model on the whole training data
    print("train data: {}".format(len(train_data)))
    model.train(train_data, test_data)  # we could use test_data as the dev_data to see the overfitting phenomena

## testing model
elif args.mode == 'test':
    ckpt_file = tf.train.latest_checkpoint(model_path)
    print(ckpt_file)
    model = BiLSTM_CRF(batch_size=args.batch_size, epoch_num=args.epoch, hidden_dim=args.hidden_dim, embeddings=embeddings,
                       dropout_keep=args.dropout, optimizer=args.optimizer, lr=args.lr, clip_grad=args.clip,
                       tag2label=tag2label, vocab=word2id, shuffle=args.shuffle,
                       model_path=ckpt_file, summary_path=summary_path, log_path=log_path, result_path=result_path,
                       CRF=args.CRF, update_embedding=args.update_embedding)
    model.build_graph()
    print("test data: {}".format(test_size))
    model.test(test_data)

elif args.mode == 'demo':
    ckpt_file = tf.train.latest_checkpoint(model_path)
    print(ckpt_file)
    model = BiLSTM_CRF(batch_size=args.batch_size, epoch_num=args.epoch, hidden_dim=args.hidden_dim,
                       embeddings=embeddings,
                       dropout_keep=args.dropout, optimizer=args.optimizer, lr=args.lr, clip_grad=args.clip,
                       tag2label=tag2label, vocab=word2id, shuffle=args.shuffle,
                       model_path=ckpt_file, summary_path=summary_path, log_path=log_path, result_path=result_path,
                       CRF=args.CRF, update_embedding=args.update_embedding)
    model.build_graph()
    saver = tf.train.Saver()
    sess = tf.Session()
    # print('============= demo =============')
    # saver.restore(sess, ckpt_file)
    # demo_sent = "我是艾成铭"
    # demo_sent = list(demo_sent.strip())
    # demo_data = [(demo_sent, ['O'] * len(demo_sent))]
    # tag = model.demo_one(sess, demo_data)
    # PER, LOC, ORG = get_entity(tag, demo_sent)
    # print(PER,LOC,ORG)
    # # map = []
    # # map['per'] = PER
    # # map['loc'] = LOC
    # map['org'] = ORG

def ner(text):
    print('============= demo =============')
    saver.restore(sess, ckpt_file)
    demo_sent = text
    demo_sent = list(demo_sent.strip())
    demo_data = [(demo_sent, ['O'] * len(demo_sent))]
    tag = model.demo_one(sess, demo_data)
    PER, LOC, ORG = get_entity(tag, demo_sent)
    map = {}
    map['per'] = PER
    map['loc'] = LOC
    map['org'] = ORG
    return map