from flair.embeddings import FlairEmbeddings, BertEmbeddings, WordEmbeddings, DocumentRNNEmbeddings, ELMoEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.training_utils import EvaluationMetric
from flair.visual.training_curves import Plotter
from flair.datasets import ClassificationCorpus


def train_sentiment_model(root_dir,train, dev, test):

    corpus = ClassificationCorpus(
        root_dir,
        train_file=train,
        dev_file=dev,
        test_file=test,
    )

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
    trainer.train('./',
                  EvaluationMetric.MACRO_F1_SCORE,
                  max_epochs=25)

    plotter = Plotter()
    plotter.plot_training_curves(file_path / 'loss.tsv')
    plotter.plot_weights(file_path / 'weights.txt')

if __name__ == "__main__":
    train_sentiment_model("./data_sets/SST_5",
                          "train.txt",
                          "dev.txt",
                          "train.txt")