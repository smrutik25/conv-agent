from furhat_remote_api import FurhatRemoteAPI
from threading import Thread, Event
import time
stop_event = Event()

#TODO: Add log to json file which will call the short term (furhat speak BOT:, furhat listen USER: and send it to STM)
# for bot dialogue, keep adding to bot, once user dialogue comes and is coherent, send it to STM. Delete file from local everytime to avoid duplicate
class FurhatConnection:
    def __init__(self):
        self.furhat = FurhatRemoteAPI("localhost")
        self.furhat.set_voice(name='Matthew')
        self.furhat.set_face(mask="adult", character="Alex")
        self.dialogue = {"BOT":"","USER":""}

    
    def furhat_hear(self):
        result = Status()
        # TODO: add timeout
        while not result.message:
            result = self.furhat.listen()
            if stop_event.is_set():
                break

        # TODO: should ask LLM is sentence is coherent (with context?) else ask again??
        return result
    
    def furhat_listen(self, time_out = 5, context = None):
         listen_thread = Thread(target=self.furhat_hear)
         listen_thread.join(timeout=time_out)
         stop_event.set()

    def furhat_speak(self, speech):
        self.furhat.say(text=speech)


class Status:
    def __init__(self):
        self.message = ''
        self.success = ''

if __name__ == "__main__":
    furhat = FurhatConnection()
    furhat.furhat_speak("Hi there. How are you doing today?")
    furhat.furhat_listen()