from transformers import pipeline

def sentiment_analysis(comments):

    classifier_ru = pipeline("sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment-rusentiment")

    sentiment_result = {
        'POSITIVE': [],
        'NEGATIVE': [],
        'NEUTRAL': []
    }

    for i in comments:
        if len(i) <= 716:
            sentiment = classifier_ru(i)
            if sentiment[0]['label'] == 'POSITIVE':
                sentiment_result['POSITIVE'].append(i)
            elif sentiment[0]['label'] == 'NEGATIVE':
                sentiment_result['NEGATIVE'].append(i)
            elif sentiment[0]['label'] == 'NEUTRAL':
                sentiment_result['NEUTRAL'].append(i)

    return sentiment_result
