from django.contrib import admin
from .models        import WebSocketToken

# Register your models here.


class WebSocketTokenAdmin(admin.ModelAdmin):
  pass


admin.site.register(WebSocketToken, WebSocketTokenAdmin)