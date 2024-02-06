import sys
import tomotopy as tp


class tomoto:
    def __init__(self):
        self.model = tp.LDAModel(tw=tp.TermWeight.ONE, min_cf=2, rm_top=0, k=5)
        self.model.burn_in = 100
        self.training_count = 10
        self.topics = {}

    def process(self):
        self.__training()

        return self.get_topic()

    # 텍스트 리스트 추가
    def add_docs(self, docs):
        for doc in docs:
            self.add_doc(doc)

    # 텍스트 추가
    def add_doc(self, doc):
        self.model.add_doc(doc)

    # 모델 학습
    def __training(self):
        print('Training...', file=sys.stderr, flush=True)
        self.model.train(self.training_count)

    def get_topic(self):
        for k in range(self.model.k):
            topicnum = k + 1
            self.topics[topicnum] = []

            for word, weight in self.model.get_topic_words(k):
                self.topics[topicnum].append({
                    'word': word,
                    'weight': weight
                })

        return self.topics
