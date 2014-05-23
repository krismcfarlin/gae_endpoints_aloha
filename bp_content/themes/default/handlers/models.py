from endpoints_proto_datastore.ndb import EndpointsModel
from google.appengine.ext import ndb

class AlohaModel(EndpointsModel):

    id = ndb.IntegerProperty()
    pageId = ndb.StringProperty()
    contentId = ndb.StringProperty()
    content = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)