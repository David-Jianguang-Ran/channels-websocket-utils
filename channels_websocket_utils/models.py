from django.db                      import models
from django.conf                    import settings

import uuid


# Create your models here.
class WebSocketToken (models.Model):
  """
  
  """
  token_str         = models.UUIDField(null=False, default=uuid.uuid4, unique=True, primary_key=True)
  
  user              = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
  
  expired           = models.BooleanField(default=False)