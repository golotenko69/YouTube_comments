class Analysis:

    def __init__(self, sentiment_comments: dict):

        self.sentiment_comments = sentiment_comments

    def send_comments_sentiment(self, sentiment: str):

        self.all_comments = []

        if sentiment != 'ALL':
            return self.sentiment_comments[sentiment]
        else:
            for i in self.sentiment_comments:
                self.all_comments.extend(self.sentiment_comments[i])
            return self.all_comments

    def send_comments_length(self, sentiment: str):
        if sentiment != 'ALL':
            self.sentiment_dict = {
                'NEGATIVE': "Негативных",
                'POSITIVE': "Положительных",
                'NEUTRAL': "Нейтральных",
            }
            return f'{self.sentiment_dict[sentiment]} комментариев {len(self.sentiment_comments[sentiment])}'

        else:
            self.length_all = 0

            for i in self.sentiment_comments:
                self.length_all += len(self.sentiment_comments[i])

            return self.length_all


