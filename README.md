This is a record of my exploration of GAE end points combined with my favourite wysiwyg editor Aloha.  

1.  Setup boilerplate https://github.com/coto/gae-boilerplate
Read the readme ad follow the instruction on how to setup your machine and get it up and running. 
2.  Go take a look at Aloha http://aloha-editor.org/.  Goto the demo and look at how it is to use http://aloha-editor.org/demos/3col/ .  We will base everything on the sample script found here http://www.aloha-editor.org/howto-store-data-with-aloha-editor-ajax.php

3.  Setup the models for storing the data.  This is based on the sample script all ready mentioned.  I used the scheme as described in the example and just added a created field.  Go into your project and  look in the bp_content folder(where all you content should go) and find the themes directory. The project would prefer you to create a new theme for your project under this folder and use the default as an example.  I prefer to just use the default!  Under bp_content/themese/default/handlers you will find the model.py file which will contain the models for this project.

	```
	from endpoints_proto_datastore.ndb import EndpointsModel
	from google.appengine.ext import ndb

	class AlohaModel(EndpointsModel):

    	id = ndb.IntegerProperty()
    	pageId = ndb.StringProperty()
    	contentId = ndb.StringProperty()
    	content = ndb.TextProperty()
    	created = ndb.DateTimeProperty(auto_now_add=True) 
	```


4.  Open up the app.yaml file.  
	a.  Find the handlers section and make it look like this:
			handlers:
			- url: /_ah/spi/.*
	  		  script: services.application	
	          ...
	          more handlers here, don't change.
	          ...
	b.  For handling javascript you need to add some more handlers
			- url: /js/(.*\.js)$
              mime_type: text/javascript
          	  static_files: bp_content/themes/default/static/js/\1
          	  upload: bp_content/themes/default/static/js/(.*\.js)$

			- url: /bower_components
  	  		  static_dir: bp_content/themes/default/static/js/bower_components

	b.  Find the libraries section and add
			- name: endpoints
  	  		  version: "latest"

5.  Create a new Service services.py in the root of your project folder.  

	```

	
		@AlohaModel.method(request_fields= ('id','pageId','contentId','content','created'), path='aloha', http_method='POST', name='aloha.insert')
    	def Insert(self, my_model):
        	old_model = AlohaModel.query(AlohaModel.pageId == my_model.pageId,AlohaModel.contentId == my_model.contentId).get()
        	if old_model:
            	old_model.content = my_model.content
            	old_model.put()
            	return old_model
        	else:
            	my_model.put()
            	return my_model


    	@AlohaModel.method(request_fields=('id', ), path='aloha/{id}', http_method='DELETE', name='aloha.delete')
    	def Delete(self, my_model):
        	ndb.delete_multi([my_model.key])
        	return my_model

    	@AlohaModel.method(request_fields=('id', ), path='aloha/{id}', http_method='GET', name='aloha.get')
    	def Get(self, my_model):
        	if not my_model.from_datastore:
            	raise endpoints.NotFoundException('MyModel not found.')
        	return my_model

    	@AlohaModel.query_method(query_fields=('limit', 'order'), path='aloha', name='aloha.list')
    	def List(self, query):
        	return query

	application = endpoints.api_server([AlohaModelApi], restricted=False)
	
	```
	
	This is almost exactly the same as my previous post but I will go over it again.
	Lets go over this:

  	a.  Import everything we need from the endpoints libraries  
		
		```
    	import endpoints
    	from protorpc import remote
		```
  	b.  Import the model we created earlier
		
		```
    	from bp_content.themes.default.handlers.models import *
		```
  	c.  Create a Api named 'contentapi' with a version of v1 and a description of 'Aloha API'.
		
		```
    	@endpoints.api(name='contentapi', version='v1', description='Aloha API')
		class AlohaModelApi(remote.Service):
		```

  	d.  Create a method that can take 'id', 'pageId', 'contentId', 'content', 'created' as a request parameter.  The path of the request will be aloha and can only be a POST.   It has a name of aloha.insert.  Notice that since this doesn't use the key id normally used to identify the content but instead uses contentId and pageId when need to do a special test for the old object already existing in the database.  If it already exists we update it, otherwise we create a new one. 
    
  		```
  		@AlohaModel.method(request_fields = ('id', 'pageId', 'contentId', 'content', 'created'), path = 'aloha', http_method = 'POST', name='aloha.insert')
    	def Insert(self, my_model):
        	old_model = AlohaModel.query(AlohaModel.pageId == my_model.pageId, AlohaModel.contentId == my_model.contentId).get()
        	if old_model:
            	old_model.content=my_model.content
            	old_model.put()
            	return old_model
        	else:
            	my_model.put()
            	return my_model
		```
  	e.  Here we have created a delete function that takes a parameter id.  Eventually we should change this to contentId and pageId.  Also note that the http_method must be a DELETE	
  	
		```
		@AlohaModel.method(request_fields=('id',),path='aloha/{id}', http_method='DELETE', name='aloha.delete')
    def Delete(self,my_model):
        ndb.delete_multi([my_model.key])
        return my_model
		```
  	f.  Here we have created a get function that takes a parameter id.  Eventually we should change this to contentId and pageId.  Also note that the http_method must be a GET

		```
		@AlohaModel.method(request_fields=('id',), path='aloha/{id}', http_method='GET', name='aloha.get')
    def Get(self, my_model):
        if not my_model.from_datastore:
            raise endpoints.NotFoundException('MyModel not found.')
        return my_model
		```
  	g.  Here we have created a list function that is used to get all entries.  We could limit these results by setting the limit and the order. 
  		
  		```
  		@AlohaModel.query_method(query_fields=('limit', 'order'),path='aloha', name='aloha.list')
    	def List(self, query):
        	return query
		```
      	

6. Experimenting With what we have built.  Please run the application and point your browser and the local url/port .  In my case it is localhost:8080/_ah/api/explorer.  This should take you to GAE api explorer.  From here we will be able to test out that our api is working correctly.   
	a.  Fill out the form giving the pageId, contentId, and content a value
	  
	
	
		```
		POST http://localhost:8080/_ah/api/contentapi/v1/aloha
		Content-Type:  application/json
		X-JavaScript-User-Agent:  Google APIs Explorer

		{
			"pageId": "/page/",
			"contentId": "headline",
			"content": "test"
		}
		```
	

    b.  Go down and click the contentapi.aloha.list
    
    
    	```
    	GET http://localhost:8080/_ah/api/contentapi/v1/aloha
		X-JavaScript-User-Agent:  Google APIs Explorer

		
		{
			"items": 
			[
	
				{
					"content": "test",
					"contentId": "headline",
					"created": "2014-05-22T22:19:06.927069",
					"pageId": "/page/"
				}
			]
		}
		```
7.  We are going to now setup the javascript and html pages.
	a.  page.html 
	
		```
		<!doctype html>
		<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en">
		<head>
    	<title>Aloha Editor | Example how to save content</title>

    	<!-- load the jQuery and require.js libraries -->
    	<script type="text/javascript" src="http://cdn.aloha-editor.org/latest/lib/require.js"></script>
    	<script type="text/javascript" src="http://cdn.aloha-editor.org/latest/lib/vendor/jquery-1.7.2.js"></script>

    	<!-- here we have our Aloha Editor config -->
    	<script src="/js/aloha-config.js"></script>

    	<script src="http://cdn.aloha-editor.org/latest/lib/aloha.js"
        	data-aloha-plugins="common/ui,
                            common/format,
                            common/table,
                            common/list,
                            common/link,
                            common/highlighteditables,
                            common/block,
                            common/undo,
                            common/contenthandler,
                            common/paste,
                            common/commands,
                            common/abbr,
                            common/image"></script>

    	<link rel="stylesheet" href="http://cdn.aloha-editor.org/latest/css/aloha.css" type="text/css">

    	<!-- save the content of the page -->
    	<script src="/js/aloha-save.js"></script>

    	<script type="text/javascript">
        Aloha.ready( function() {
            var $ = Aloha.jQuery;
            // Make all elements with class=".editable" editable once Aloha is loaded and ready.
            $('.editable').aloha();
        });
    	</script>

    	<style>
        	#headline {
            	font-size: 1.3em;
        	}
        	#article {
            	margin-top: 20px;
        	}
        	#log {
            	border: 2px dashed green;
            	margin: 5px auto 5px auto;
            	padding: 5px;
            	width: 75%;
            	display: none;
        	}
    	</style>
		</head>
		<body>
    	<div id="log"></div>

    	<h1>My Page</h1>
    	<p>Click below to edit the text. When leaving editing mode (switch between editable areas or click outside an editable area) the content will be saved.</p>

    	<div class="editable" id="headline">{% if headline %}{{headline}}{%endif%}</div>
    	<div class="editable" id="article">{% if article %}{{article}}{%endif%}</div>

    	<h2>Textarea</h2>
    	<textarea name="mytextarea" id="mytextarea" rows="10" class="editable">{% if mytextarea %}{{mytextarea}}{%endif%}</textarea>
		</body>
		</html>
		```
		The only thing that was changed from the original is taking out the php function and replacing it with jinga2 templating for the editable areas.  
	
	b.
	
	
		```
	
		Aloha.ready(function() {
    	Aloha.require( ['aloha', 'aloha/jquery'], function( Aloha, jQuery) {

        // save all changes after leaving an editable
        Aloha.bind('aloha-editable-deactivated', function(){
            var content = Aloha.activeEditable.getContents();
            var contentId = Aloha.activeEditable.obj[0].id;
            var pageId = window.location.pathname;

            // textarea handling -- html id is "xy" and will be "xy-aloha" for the aloha editable
            if ( contentId.match(/-aloha$/gi) ) {
                contentId = contentId.replace( /-aloha/gi, '' );
            }

            var request = jQuery.ajax({
                url: '//' + window.location.host +"/_ah/api/contentapi/v1/aloha",
                type: "POST",
                data: JSON.stringify({
                    content : content,
                    contentId : contentId,
                    pageId : pageId
                }),
                dataType: "json"
            });

            request.done(function(msg) {
                jQuery("#log").html( msg ).show().delay(800).fadeOut();
            });

            request.error(function(jqXHR, textStatus) {
                alert( "Request failed: " + textStatus );
            });
        });

    	});
    	});
    
		```
		Here we made a few changes to the url so it points at out endpoints and then turned the data into json by JSON.stringify


8.   Finish hooking up the page file.  
	a.  In the bp_content/themes/default/handlers/handlers.py file add
		
		```
		class PageHandler(BaseHandler):
    		def get(self,*args,**kwargs):
      			pageId = self.request.get('pageId','/page/')
      			results=AlohaModel.query(AlohaModel.pageId==pageId).fetch()
      			params ={}
      			for result in results:
          			params[result.contentId]=result.content

      			return self.render_template('page.html', **params)
      ```
	  This goes out and find the content for all items on the page and then puts it in the params dictionary using the contentId as a key.  
    	

	b.  in the bp_content/themes/default/routes/__init__.py file add the following route
	 	
	 	```
    	RedirectRoute('/page', handlers.PageHandler, name='page', strict_slash=True)
		```
  

Voila!  We are done, and have a great example of google endpoints being used to supply data to my favourite editor Aloha!

