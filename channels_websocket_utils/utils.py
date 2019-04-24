from django.conf import settings
from django.contrib.auth import get_user_model
from .models import WebSocketToken


def debug_print(some_str):
  if settings.DEBUG:
    print("Debug Printout from module {} Below\n".format(__name__),some_str)
  else:
    # TODO pass for now, add logging later
    pass


def get_websocket_token(user):
  """
  This function generates a new token and assigns it to a user
  Note that ONLY signed in users can have ws token assigned to them (AnonymousUser is not a user )
  Note that this is a synchronous db function.
  :param user: django user obj
  :return: token_str uuid4 string
  """
  new_token         = WebSocketToken()
  
  # only save user instance if a valid user is passed in
  if isinstance(user,get_user_model()):
    new_token.user  = user
    
  new_token.save()
  return str(new_token.token_str)


def validate_websocket_token(scope):
  """
  This function checks if a connected user has a valid token assigned to them
  Note that this is a synchronous db function.
  :param scope: ASGI scope obj
  :return: bool
  """
  token_str         = scope['url_route']['kwargs']['token']
  user              = scope['user']
  
  # do we have a token?
  try:
    token = WebSocketToken.objects.get(token_str=token_str)
  except WebSocketToken.DoesNotExist:
    debug_print("ws ticket validation failed for user {}".format(user))
    return False
  
  debug_print("WS connection recieved \n token_user: {} user: {}".format(token.user,user))
  # is the token assigned to current session?
  if token.user is None:
    return False
  elif token.user  == user: # Yay Django models
    # mark token expired before returning
    token.expired   = True
    token.save()
    return True
  else:
    return False
