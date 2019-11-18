from flair.embeddings import FlairEmbeddings, BertEmbeddings, WordEmbeddings, DocumentRNNEmbeddings, ELMoEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.training_utils import EvaluationMetric
from flair.visual.training_curves import Plotter
from flair.datasets import ClassificationCorpus

from pathlib import Path

import flair, torch
flair.device = torch.device('cpu')

def train_sentiment_model(root_dir):

    corpus = ClassificationCorpus(root_dir)

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
    here = Path('.').resolve()
    trainer.train(here, max_epochs=25)

    plotter = Plotter()
    plotter.plot_training_curves(root_dir / 'loss.tsv')
    plotter.plot_weights(root_dir / 'weights.txt')

if __name__ == "__main__":
    root_path =  Path('./data_sets/SST_5').resolve()

    print(root_path)
    train_sentiment_model(root_path)
