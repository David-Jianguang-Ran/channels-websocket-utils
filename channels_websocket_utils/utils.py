from django.conf import settings
from django.contrib.auth import get_user_model
from .models import WebSocketToken


def debug_print(some_str):
  if settings.DEBUG:
    print("Debug Printout from module {} Below\n".format(__name__),some_str)


def get_websocket_token(user):
  """
  
  :param user: django user obj
  :return: token_str uuid4 string
  """
  new_token         = WebSocketToken()
  
  # only save user instance if a valid user is passed in
  if isinstance(user,get_user_model()):
    new_token.user    = user
    
  new_token.save()
  return str(new_token.token_str)


def validate_websocket_token(scope):
  """
  
  :param session:
  :param token:
  :return:
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
  elif token.user.id == user.id:
    return True
  else:
    return False
