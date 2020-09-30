from queries import last_messages, get_follows
from pprint import pprint


def initialLoginView(context):
    last_msg = last_messages(context, 10)
    influencers = get_follows(context, 5)
    pprint(last_msg)
    pprint(influencers)
    


