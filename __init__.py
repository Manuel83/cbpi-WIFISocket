from modules import cbpi
from modules.core.hardware import ActorBase, SensorPassive, SensorActive
from modules.core.props import Property
import httplib2
from flask import request
import base64

@cbpi.actor
class WIFISocket(ActorBase):

    b_user = Property.Text("User", configurable=True, default_value="admin" )
    c_password = Property.Text("Password", configurable=True, default_value="")
    a_url = Property.Text("Url", configurable=True, default_value="http://")
    # Command so swtich wifi socket on
    onCommand = '<?xml version="1.0" encoding="utf-8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>ON</Device.System.Power.State></CMD></SMARTPLUG>'
    # Command so swtich wifi socket off
    offCommand = '<?xml version="1.0" encoding="utf-8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>OFF</Device.System.Power.State></CMD></SMARTPLUG>'

    def send(self,  command):
        try:
            h = httplib2.Http(".cache")
            auth = base64.encodestring( "%s:%s" % (self.b_user, self.c_password) )
            headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization' : 'Basic ' + auth}
            ## Sending http command ""
            h.add_credentials( self.b_user, self.c_password)
            (resp_headers, content) = h.request("%s/smartplug.cgi" % (self.a_url), "POST",  body=command, headers=headers)
        except Exception as e:
            self.api.app.logger.error("FAIELD to switch WIFI socket %s User: %s" % (self.url, self.user))

    def on(self, power=100):
        self.send(self.onCommand)

    def off(self):
        self.send(self.offCommand)


