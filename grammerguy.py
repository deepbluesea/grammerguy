import twitter
import random 

class TwitterBot:
    api = twitter.Api(consumer_key='key',
        consumer_secret='key',
        access_token_key='key',
        access_token_secret='key')

    people_helped = [line.replace("\n", "") for line in
            open("people_that_were_helped.txt").readlines()]
    
    def find_tweets(self):
        #Search for some dweebs
        results = self.api.GetSearch("intensive purposes")
        self.tweets_list = [(tweet.id, tweet.user.screen_name,  tweet.text) for tweet in results]

    def print_tweets(self):
        for tweet in self.tweets_list:
            print tweet

    def is_sarcastic(self, text):
        sarcastic = False
        triggers = ("grammar", "Grammar", "English", "english", "intents",
        "instead", "wrong", "bad", "stupid", "idiot", "learn", "actually",
        "not", "smart", "hate", "worst", "worse", "isn't", "care less")

        for word in triggers:
            if word in text:
                sarcastic = True

        return sarcastic

    def is_retweet(self, text):
        if "RT" in text:
            return True
        else:
            return False

    def generate_response(self):
        responses = open("responses.txt").readlines()
        return random.choice(responses)

    def was_already_helped(self, name):
        for person in self.people_helped:
            if name == person:
                return True

        return False

    def save_name(self, name):
        with open("people_that_were_helped.txt", "a") as f:
            print>>f, name

    def ok_to_tweet(self, name, tweet):
        if self.is_sarcastic(tweet):
            return False

        if self.is_retweet(tweet):
            return False

        if self.was_already_helped(name):
            return False

        return True

if __name__ == "__main__":
    bot = TwitterBot()
    bot.find_tweets()
    
    for tweetid, user, tweet in bot.tweets_list:
        if bot.ok_to_tweet(user, tweet): 
            response = bot.generate_response()
            full_tweet = "@{0} {1}".format(user, response)
            print("Replying to user {0}".format(user))
            bot.api.PostUpdate(status=full_tweet,
                    in_reply_to_status_id=tweetid)
            bot.save_name(user)
            break


