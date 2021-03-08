"""
"""
import pickle
import os
from abc import ABC, abstractmethod

URIS_FILE = os.path.join(os.getcwd(), 'uris.pkl')

class URIFactory(ABC):

    @abstractmethod
    def get_uri(self, uriRef) -> str:
        """ Gets the uri for a NonLiteralElement.

       Parameters
       ----------
       NonLiteralElement: uriRef
           NonLiteralElement to find a uri.

       Returns
       -------
       :str: uri
           Uri that corresponds to the NonLiteralElement
       """

    @abstractmethod
    def post_uri(self, uriRef, wb_uri) -> None:
        """ Posts the uri for a NonLiteralElement.

          Parameters
          ----------
          NonLiteralElement: uriRef
              NonLiteralElement that corresponds to the new uri.

          wb_uri: str
              Uri for the label .
          """

class URIFactoryMock(URIFactory):
    class __URIFactoryMock():
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
        if not URIFactoryMock.instance:
            URIFactoryMock.instance = URIFactoryMock.__URIFactoryMock()


    def get_uri(self, uriRef):
        return URIFactoryMock.instance.state[uriRef.uri] \
            if uriRef.uri in URIFactoryMock.instance.state else None

    def post_uri(self, uriRef, wb_uri):
        URIFactoryMock.instance.state[uriRef.uri] = wb_uri
        with open(URIS_FILE, 'wb') as f:
            pickle.dump(URIFactoryMock.instance.state, f)

    def reset_factory(self):
        URIFactoryMock.instance.state = {}
        with open(URIS_FILE, 'wb') as f:
            pickle.dump(URIFactoryMock.instance.state, f)
