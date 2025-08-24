import paho.mqtt.client as mqtt
from queue import Queue
import time

class MqttReader:
    def __init__(self, broker="localhost", topic="ping/ping"):
        self.queue = Queue()
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(broker, 1883, 60)
        self.client.subscribe(topic)
        self.client.loop_start()
        self.topic = topic

    def on_message(self, client, userdata, msg):
        try:
            value = int(msg.payload.decode())
            self.queue.put(value)
        except ValueError:
            pass  # ignorer si pas un entier

    def get_messages(self):
        """Retourne tous les messages reçus depuis la dernière lecture"""
        values = []
        while not self.queue.empty():
            values.append(self.queue.get())
        return values
    
    def publish_messages(self, n):
        """Publie un message sur ping/ping"""
        self.client.publish(self.topic, str(n))

    def cycle_publish(self):
        """Publie un message de 0 à 10 toutes les secondes sur ping/ping puis recommence"""
        a = 0
        while True :
            self.client.publish(self.topic, str(a))
            a += 1
            if a > 10 :
                a = 0
            time.sleep(2)
            print(a)
    
