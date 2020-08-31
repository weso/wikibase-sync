"""
"""
import pickle
import os

URIS_FILE = os.path.join(os.getcwd(), 'uris.pkl')

class URIFactory():
    class __URIFactory():
        def __init__(self):
            if not os.path.isfile(URIS_FILE):
                with open(URIS_FILE, 'wb') as f:
                    pickle.dump({}, f)

            with open(URIS_FILE, 'rb') as f:
                try:
                    self.state = pickle.load(f)
                except EOFError:
                    self.state = {}

    instance = None

    def __init__(self):
        if not URIFactory.instance:
            URIFactory.instance = URIFactory.__URIFactory()


    def get_uri(self, label):
        return URIFactory.instance.state[label] \
            if label in URIFactory.instance.state else None

    def post_uri(self, label, wb_uri):
        URIFactory.instance.state[label] = wb_uri
        with open(URIS_FILE, 'wb') as f:
            pickle.dump(URIFactory.instance.state, f)

    def reset_factory(self):
        URIFactory.instance.state = {}
        with open(URIS_FILE, 'wb') as f:
            pickle.dump(URIFactory.instance.state, f)
