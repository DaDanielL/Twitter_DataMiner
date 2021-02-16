#import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.uix.carousel import Carousel
from kivy.config import Config
from kivy.uix.scrollview import ScrollView

import time
import webbrowser
import os
import pandas as pd 

from tweet_streamer import Twitter
from data_analyzer import DataAnalyzer



class DataPanel(ScrollView):
    def __init__(self, **kwargs):
        super(DataPanel, self).__init__(**kwargs)
        self.size_hint = (1, 0.75)


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
                   title_font='font/WhitneyBold.ttf')
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
                kw = self.searchFilter.text.split(',')
                if kw == ['']:
                    Twitter.start_stream(True)
                else:
                    Twitter.start_stream(True, kw)
                self.manager.current = 'streaming'

        except AttributeError:
            self.get_auth()


class AuthPopup(FloatLayout):
    pass


class Streaming(Screen):
    numTweet = ObjectProperty(None)
    posii = ObjectProperty(None)

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

        self.Dm = DataAnalyzer('data/tweets.json')
        self.Dm.create_dataframe()
        self.Dm.sentiment_analysis()
        self.Dm.create_csv()
        self.Dm.create_graphs()


class DataDisplay(Screen):
    pos_wc = ObjectProperty(None)
    neg_wc = ObjectProperty(None)
    pie_chart = ObjectProperty(None)
    line_chart = ObjectProperty(None)

    def on_enter(self):
        if os.path.exists('graphs/pos.png'):
            self.pos_wc.source = 'graphs/pos.png'
        else:
            self.pos_wc.source = 'graphs/graphNotFound.png'
        if os.path.exists('graphs/neg.png'):
            self.neg_wc.source = 'graphs/neg.png'
        else:
            self.neg_wc.source = 'graphs/graphNotFound.png'
        if os.path.exists('graphs/pie.png'):
            self.pie_chart.source = 'graphs/pie.png'
        else:
            self.pie_chart.source = 'graphs/graphNotFound.png'
        if os.path.exists('graphs/line.png'):
            self.line_chart.source = 'graphs/line.png'
        else:
            self.line_chart.source = 'graphs/graphNotFound.png'




class TSApp(App):
    def on_stop(self):
        try:
            f = open('data/tweets.json','r+')
            f.seek(0)
            f.truncate()
            Twitter.start_stream(False)
        except: 
            pass

    def build(self):
        kv_file = Builder.load_file('app.kv')
        return kv_file


if __name__ == '__main__':
    LabelBase.register(name='Title', fn_regular="font/Uni Sans Heavy.ttf")
    LabelBase.register(name='Header', fn_regular="font/PontanoSans-Regular.ttf")
    LabelBase.register(name='normal', fn_regular="font/WhitneyBold.ttf")

    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    Factory.register('HoverBehavior', HoverBehavior)
    
    TSApp().run()

