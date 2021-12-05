from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import paho.mqtt.client as mqtt

__author__ = 'jamiehoward430/JonStratton'

LOGGER = getLogger(__name__)

class mymqttskill(MycroftSkill):

    def __init__(self):
        super(mymqttskill, self).__init__(name="mymqttskill")
        self.settings['mqtthost'] = '192.168.2.194'
        if ( not self.settings.get('mqttport') ):
           self.settings['mqttport'] = '1883'
        self.mqttc = mqtt.Client("MycroftAI")

    def shutdown(self):
        self.mqttc.disconnect()
    
    def initialize(self):
        self.__build_single_command()
        
    def __build_single_command(self):
        intent = IntentBuilder("mymqttIntent").require("CommandKeyword").require("ModuleKeyword").require("ActionKeyword").build()
        self.register_intent(intent, self.handle_single_command)
        
    def handle_single_command(self, message):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                LOGGER.info("Connected to MQTT Broker!")
            else:
                LOGGER.info("Failed to connect, return code %d\n", rc)
        cmd_name = message.data.get("CommandKeyword").replace(' ', '_')
        dev_name = message.data.get("ModuleKeyword").replace(' ', '_')
        act_name = message.data.get("ActionKeyword").replace(' ', '_')
        
        #try:
        self.mqttc.on_connect = on_connect
        LOGGER.info( "MQTT Connect: " + self.settings['mqtthost'] + ':' + str(self.settings['mqttport']) )
        self.mqttc.connect("192.168.2.194")
        LOGGER.info( "after connect")
        self.mqttc.publish("domoticz/in", '{"type":"command","param":"switchlight","idx":"32","switchcmd":"On"}')
        LOGGER.info( "after publish")
        self.mqttc.disconnect()
        LOGGER.info( "after disconnect")
        self.speak_dialog("cmd.sent")
        # type=command&param=switchlight&idx=99&switchcmd=Off
        LOGGER.info("MQTT Publish: domoticz/in/" + '{"type":"command","param":"switchlight","idx":"32","switchcmd":"On"}')
        #LOGGER.info("MQTT Publish: " + dev_name + "/" + cmd_name + "/" + act_name)
        #except:
        #    self.speak_dialog("not.found", {"command": cmd_name, "action": act_name, "module": dev_name})
        
    def stop(self):
        pass
        
def create_skill():
    return mymqttskill()
