import argparse
from pathlib import Path

from flair.embeddings import FlairEmbeddings, BertEmbeddings, WordEmbeddings, DocumentRNNEmbeddings, ELMoEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.training_utils import EvaluationMetric
from flair.visual.training_curves import Plotter
from flair.datasets import ClassificationCorpus

import flair, torch

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)


def train_sentiment_model(rootdir, train, dev, test, num_epochs, device, outputdir):

    flair.device = torch.device(device)

    corpus = ClassificationCorpus(rootdir,
                                  train_file=train,
                                  dev_file=dev,
                                  test_file=test,
                                  in_memory=False)

    label_dict = corpus.make_label_dictionary()

    # init Flair embeddings
    flair_forward_embedding = FlairEmbeddings('multi-forward')
    flair_backward_embedding = FlairEmbeddings('multi-backward')

    optional_embedding = ELMoEmbeddings('original')

    word_embeddings = list(filter(None, [
        optional_embedding,
        FlairEmbeddings('news-forward'),
        FlairEmbeddings('news-backward'),
    ]))

    # Initialize document embedding by passing list of word embeddings
    #
    # Note this will kick off model generation that will take a long time (several hours)
    # This will produce final-model.pt and best-model.pt files which represent a stored trained model.
    document_embeddings = DocumentRNNEmbeddings(
        word_embeddings,
        hidden_size=512,
        reproject_words=True,
        reproject_words_dimension=256,
    )

    classifier = TextClassifier(document_embeddings,
                                label_dictionary=label_dict,
                                multi_label=False)

    trainer = ModelTrainer(classifier, corpus)
    trainer.train(outputdir, max_epochs=num_epochs)


if __name__ == "__main__":

    def gather_compute_devices():
        devices = ['cpu']
        if torch.cuda.is_available():
            devices.extend( ['cuda:'+str(idx) for idx in range(0,torch.cuda.device_count())] )
        return devices

    def check_file_path(root, file):
        file_path = root / file
        if not file_path.exists():
            raise FileNotFoundError( "Could find file at " + str(file_path) )

    compute_devices = gather_compute_devices()

    parser = argparse.ArgumentParser(description='Train a flair model to be used with the streaming analytics module.')
    parser.add_argument('--rootdir', type=str, help="Dataset path", default='./data_sets/SST_5')
    parser.add_argument('--outdir', type=str, help="Path to put output files", default='./')
    parser.add_argument('--train', type=str, help="Training set filename", default="train.txt")
    parser.add_argument('--dev', type=str, help="Dev set filename", default="dev.txt")
    parser.add_argument('--test', type=str, help="Test/validation set filename", default="test.txt")
    parser.add_argument('--epochs', type=int, help="Number of epochs", default=25)
    parser.add_argument('--device', choices=compute_devices, type=str, help="Which compute device to use", default='cpu')

    args = parser.parse_args()

    root_path =  Path(args.rootdir).resolve()
    if not root_path.is_dir():
        raise FileNotFoundError( "Couldn't find directory at: " + str(root_path) )

    train = args.train
    dev = args.dev
    test = args.test

    check_file_path( root_path, train )
    check_file_path( root_path, dev )
    check_file_path( root_path, test )

    out_path =  Path(args.outdir).resolve()
    if not out_path.is_dir():
        raise FileNotFoundError( "Couldn't find directory at: " + str(out_path) )

    epochs = args.epochs
    device = args.device

    logger.debug(
        "Extracting data from: " + str(root_path) + "\n"
        "   Using training set: " + str( root_path / train ) + "\n"
        "   Using dev set: " + str( root_path / dev ) + "\n"
        "   Using test set: " + str( root_path / test ) + "\n"
        "With max epochs set to: " + str(epochs) + "\n"
        "Using compute device: " + device + "\n"
        "   Given available compute devices: " + ", ".join(compute_devices) + "\n"
        "Saving results to: " + str(out_path)
    )

    train_sentiment_model(root_path, train, dev, test, epochs, device, out_path)