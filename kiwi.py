from kiwipiepy import Kiwi
import os
import sys
import re

#print(os.path.dirname(os.path.realpath(__file__))); sys.exit(1);

class kiwi:

    def __init__(self):
        self.new_stop_words = [] 
        self.kiwi_model = Kiwi(model_type='sbg', typos='basic')

        with open(os.path.dirname(os.path.realpath(__file__)) + '/dataset/stopwords.txt', 'r', encoding='UTF-8') as texts:
            self.new_stop_words = texts.read().split('')

    # 한글 외 제거
    def __replace_target(self, target):

        text = re.sub('[^\w\sㄱ-ㅎ가-힣_]', '', target)
        text = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', text)
        text = re.findall(r'[가-힣]+', text)
        return ' '.join(text)

    # 명사, 형용사만 추출
    def __polish(self, tokens):
        reVal = []
        for token in tokens:
            if len(token.form) < 2:
                continue

            # 명사 추출
            if token.tag in ['NNG', 'NNP']:
                reVal.append(token.form)

            # 형용사 추출
            elif token.tag in ['VA']:
                reVal.append(f'{token.form}다')

        return reVal

    # 불용어 체크 및 제거
    def __stop_word_check(self, filter_word):
        words = []
        for m, t in enumerate(filter_word):

            if t in self.new_stop_words:
                continue

            words.append(t)

        return words


    # 중복값 체크 및 제거
    def __re_word_check(self, filter_word):
        words = []
        for m, t in enumerate(filter_word):
           if t not in words:
                words.append(t)

        return words


    # 전처리(맞춤법, 공백, 특수문자)
    def process(self, text):
        try:
            nouns_word = self.__replace_target(text)

            if len(nouns_word) < 0:
                return []

            # 형태소 분석
            nouns_word = self.kiwi_model.tokenize(text)

            # 형태소 추출
            nouns_word = self.__polish(nouns_word)

            # 불용어 제거
            nouns_word = self.__stop_word_check(nouns_word)

            # 중복값 제거
            nouns_word = self.__re_word_check(nouns_word)

            return [x for x in nouns_word if x]

        except UnicodeError:
            print(text)
            print(nouns_word)
