from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

KEY = '7e6281e1d9654acbac4a53d1617203f2'
ENDPOINT = 'https://appelletext.cognitiveservices.azure.com/'

def authenticate_client():
    ta_credential = AzureKeyCredential(KEY)
    text_analytics_client = TextAnalyticsClient(
        endpoint=ENDPOINT, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sentiment_analysis_example(client,user_text):
    documents = []

    documents.append(user_text)
    response = client.analyze_sentiment(documents=documents)[0]
    text = "Document Sentiment: {}".format(response.sentiment)
    text = text + "\n" +"Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f}".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    )
    for idx, sentence in enumerate(response.sentences):
        text2 = "\n" + "Sentence: {}".format(sentence.text)
        text = text + "\n" + "Sentence {} sentiment: {}".format(idx + 1, sentence.sentiment)
        text = text +"\n"+"Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        )
    return text

def transmitdata(text):
    return sentiment_analysis_example(client, text)
