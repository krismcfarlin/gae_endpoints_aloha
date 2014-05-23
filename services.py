import endpoints
from bp_content.themes.default.handlers.models import *
from protorpc import remote




@endpoints.api(name='contentapi', version='v1', description='Aloha API')
class AlohaModelApi(remote.Service):

    @AlohaModel.method(request_fields=('id','pageId','contentId','content','created'),path='aloha', http_method='POST', name='aloha.insert')
    def Insert(self, my_model):
        old_model = AlohaModel.query(AlohaModel.pageId==my_model.pageId, AlohaModel.contentId==my_model.contentId).get()
        if old_model:
            old_model.content=my_model.content
            old_model.put()
            return old_model
        else:
            my_model.put()
            return my_model


    @AlohaModel.method(request_fields=('id',),path='aloha/{id}', http_method='DELETE', name='aloha.delete')
    def Delete(self,my_model):
        ndb.delete_multi([my_model.key])
        return my_model

    @AlohaModel.method(request_fields=('id',), path='aloha/{id}', http_method='GET', name='aloha.get')
    def Get(self, my_model):
        if not my_model.from_datastore:
            raise endpoints.NotFoundException('MyModel not found.')
        return my_model

    @AlohaModel.query_method(query_fields=('limit', 'order'),path='aloha', name='aloha.list')
    def List(self, query):
        return query

application = endpoints.api_server([AlohaModelApi], restricted=False)