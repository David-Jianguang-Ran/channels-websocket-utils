##Channels WebSocket Utils

This is a Django Channels app used to manage WebSocket Connections.
Please note that all functions are synchronous.

Thanks and Enjoy! 

David Ran 04/19


## This package contains:
- JS WebSocketManager object for sending JSON message down Websocket and routing server side messages to JS functions.
- Utility functions for getting and validating tokens for WebSocket connections
- Decorator functions for requiring perms to call consumer methods

## How To Use

### Install Django app

- Clone this repo and either:

  - Manually copy channels_websocket_utils to your project directory
  
     _OR_
     
  - Install with pip
    ```
    $ pip install <repo_root>/dist/channels-websocket-utils-0.1.tar.gz
    ```
    
- Add channels_websocket_utils to INSTALLED_APPS in settings.py

- create database tables for models.
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Include Client side script
The JS file could either be included in html template below
```jinja2
<script src="{% static 'websocket_utils/WebSocketManager.js' %}"></script>
```

or imported and bundled via webpack.

## Features

#### Message Routing
with the below python land consumer methods:
```python
# yourapp/consumers.py
from channels_websocket_utils.decorators import auto_route

class YourConsumer(SyncConsumer):

  # the below method is required if the JS app want to route message by type like channels
  def receive_json(self, content, **kwargs):
      target_method = getattr(self,content['type'])
      target_method(content)
  
  # the auto route feature is optional
  @auto_route    
  def your_method(self,event):
      python_object = {}
      return python_object

```

You can do this in JS:
```ecmascript 6
let path      = null // this is a string url path
let token     = null // this is a string used for the websocket authentication feature
let wsManager = WebSocketManager(path,token)

let replyHandler = function (reply) {
  // do some cool stuff with data sent from backend
}

const message = {
  'type' : "your_method", // note that the "type" here doesn't follow channels conventions, it is just the method name
  "key"  : "value"
}

// use the function call below to send data to consumer method (must have python set up above) 
wsManager.sendJSON(message, replyHandler)

// if you are not expecting data back, or nor using @auto_route, simply call
wsManager.sendJSON(message)

// to receive data from backend
let yourHandler = function (message) {
  // something cool with data
}

wsManager.addMessageListener("someTextKey",yourHandler)
```

#### WebSocket Authentication

In order to use the token authentication system, you'll have to implement your app like the example code below.

Python Land
```python
# in views.py
from channels_websocket_utils.utils import get_websocket_token, validate_websocket_token

def your_view(request):
  token_str         = get_websocket_token(request.user)
  return render(request, "main.html",context={"token":token_str})

# in routing.py
# implement the below pattern 
path("path/<str:token>", YourConsumer)

# in consumer.py
class YourConsumer(SyncConsumer):
  def connect (self):
    # the below function will return a boolian, do as you see fit with it
    # note that only signed in user can validate token
    boolian_result = validate_websocket_token(self.scope)

```
In your html template
```html
<script> const token = {{ token }}</script>
<script src="{% static 'websocket_utils/WebSocketManager.js' %}"></script>
```

#### Consumer Method Permission
With the supplied decorator you can also require user permission for a particular consumer method.
```python
from channels_websocket_utils.decorators import require_perms

class YourConsumer(SyncConsumer):

  @require_perms(list_o_django_perms)
  def top_secret (self):
    pass
``` 