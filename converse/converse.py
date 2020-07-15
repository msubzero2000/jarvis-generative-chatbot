import json
import re
import boto3
import pickle
#import contractions


class Converse(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint
        self._client = boto3.client(service_name='runtime.sagemaker')

    def _clean_text(self, text):
        text = text.lower()

        # Remove any html/xml tag
        text = re.sub(r'<.*?>', '', text)
        text = text.replace("...", " ")
        text = text.replace("..", " ")
        text = text.replace(" - ", '. ')
        text = text.replace("-", ' ')
        text = text.replace("  ", ' ')

        text = contractions.fix(text)

        # Separate punctuations to reduce unecc vocab
        text = text.replace("?", " ?")
        text = text.replace("!", " !")
        text = text.replace(".", " .")
        text = text.replace(",", " ,")

        text = re.sub(r"  +", " ", text)
        text = re.sub(r"didn'", "did not", text)
        text = re.sub(r"'bout", "about", text)
        text = re.sub(r"'til", "until", text)

        # Replace tryin' into trying but don't replace man's into mangs
        text = re.sub(r"n'[^s]", "ng", text)

        text = re.sub(r"[^a-z0-9,.?!' ]+", '', text)

        return text

    def converse(self, sentence):
        payload = {"instances": []}
        cleaned_sentence = self._clean_text(sentence)

        payload["instances"].append({"data": cleaned_sentence})

        response = self._client.invoke_endpoint(
            EndpointName=self._endpoint,
            ContentType='application/json',
            Body=json.dumps(payload))

        response = response["Body"].read().decode("utf-8")
        response = json.loads(response)
        resp_text = response["predictions"][0]["target"]

        # Remove unknown vocab marker if any
        resp_text = re.sub(r'\<.*?\>', '', resp_text)

        return resp_text.strip()
