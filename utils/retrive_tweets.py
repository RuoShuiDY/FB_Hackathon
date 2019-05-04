import json

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


def cleanData(data):
    json_data = json.loads(data)
    output = {"time": json_data['created_at']}

    if not json_data["truncated"]:
        output["text"] = json_data['text']
    else:
        output["text"] = json_data['extended_tweet']['full_text']

    if json_data['geo'] is not None:
        if json_data['geo']['coordinates'] is not None:
            output["location"] = (json_data['geo']['coordinates'][0], json_data['geo']['coordinates'][1])
            print(output["location"])
            with open('twitterdata.json', 'a') as outfile:
                outfile.write(json.dumps(output) + "\n")
            outfile.close()
            return

    if json_data['coordinates'] is not None:
        output["location"] = (json_data['coordinates'][0], json_data['coordinates'][1])
        print(output["location"])
        with open('twitterdata.json', 'a') as outfile:
            outfile.write(json.dumps(output) + "\n")
        outfile.close()
        return


# consumer key, consumer secret, access token, access secret.
ckey = "O1hDoL5J4CB3cLtkfJ7eHRrXc"
csecret = "fRItnO5PKTNVA4Qo8WXhpLz2HYrHcaw0rssUf7B1KsWitIBhGN"
atoken = "1124535186270539776-HyaShRaf2FNH55RAeuFOkjoA9vULKg"
asecret = "wRC9GdKMD7nT7mymGrUgm69Xm4mYVICgzWsfM8t23S0v0"


class listener(StreamListener):

    def on_data(self, data):
        print(data)
        cleanData(data)
        return (True)

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[144.90155334472656, -37.820984280171785, 144.98303232321211, -37.803273851858656])
