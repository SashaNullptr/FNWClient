from flair.embeddings import FlairEmbeddings, BertEmbeddings, WordEmbeddings, DocumentRNNEmbeddings


def train_sentiment_model():

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

if __name__ == "__main__":
    train_sentiment_model()