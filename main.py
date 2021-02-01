#import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.uix.carousel import Carousel

import time
import webbrowser
import os

from tweet_streamer import Twitter


class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget 
    """

    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)


    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)


    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')


    def on_enter(self):
        pass


    def on_leave(self):
        pass


class DataCarousel(Carousel):

    def __init__(self, **kwargs):
        super(DataCarousel, self).__init__(**kwargs)
        self.direction = 'right'
        self.loop = True
        self.anim_move_duration = 0.7
        self.min_move = 0.2
        
        Clock.schedule_interval(self.load_next, 5)
    


class HoverButton(Button,HoverBehavior):
    
    def on_enter(self, *arg):
        self.bg = self.background_normal
        self.background_normal=self.background_down

    def on_leave(self, *arg):
        self.background_normal=self.bg
        

class sm(ScreenManager):
    pass


class MainMenu(Screen):
    pass


class BeforeStreaming(Screen):

    searchFilter = ObjectProperty(None)
    status = ObjectProperty(None)


    def change_authStatus(self):
        if self.validAuth == True:
            self.status.text = 'Authentication: Success'
            self.status.color = [0,1,0,1]
        elif self.validAuth == False:
            self.status.text = 'Authentication: Failed'
            self.status.color = [1,0,0,1]


    def get_auth(self):
        Twitter.get_auth()
        content = AuthPopup()
        self.popup = Popup(title='Authentication', content=content, 
                   size_hint=(None,None),size=(300,200), 
                   title_font='WhitneyBold.ttf')
        self.popup.open()


    def set_auth(self, pin):
        try:
            Twitter.set_auth(pin)
            self.validAuth = True
        except:
            self.validAuth = False


    def close(self):
        self.popup.dismiss()


    def start_stream(self):

        try:
            if self.validAuth == False:
                self.get_auth()
            else: 
                searchList = self.searchFilter.text.split(',')
                if searchList == ['']:
                    Twitter.start_stream(True)
                else:
                    Twitter.start_stream(True, searchList)
                self.manager.current = 'streaming'

        except AttributeError:
            self.get_auth()


class AuthPopup(FloatLayout):
    pass


class Streaming(Screen):
    numTweet = ObjectProperty(None)

    def on_enter(self):
        self.event = Clock.schedule_interval(self.update_counter, 0.5)
    
    def update_counter(self, dt):
        try:
            self.numTweet.text = str(Twitter.numTweet) + ' tweets collected'
        except AttributeError:
            pass
    
    def on_leave(self):
        Clock.unschedule(self.event)
        Twitter.start_stream(False)


class DataDisplay(Screen):
    pass


class TSApp(App):
    def on_stop(self):
        try:
            Twitter.start_stream(False)
            os.remove('tweets.json')
        except: 
            pass

    def build(self):
        kv_file = Builder.load_file('app.kv')
        return kv_file


if __name__ == '__main__':
    LabelBase.register(name='Title', fn_regular="Uni Sans Heavy.ttf")
    LabelBase.register(name='Header', fn_regular="PontanoSans-Regular.ttf")
    LabelBase.register(name='normal', fn_regular="WhitneyBold.ttf")

    Factory.register('HoverBehavior', HoverBehavior)

    TSApp().run()