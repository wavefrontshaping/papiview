# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

from mdsettings import MDSettingsWithNoMenu

SETTINGS_CLS = MDSettingsWithNoMenu


#Builder.load_string('''
#    
##<-Popup>:
##    _container: container
##    GridLayout:
##        padding: '12dp'
##        cols: 1
##        size_hint: None, None
##        pos: root.pos
##        size: root.size
##        
##
##        Label:
##            text: 'Test'#root.title
##            color: root.title_color
##            size_hint_y: None
##            height: self.texture_size[1] + dp(16)
##            text_size: self.width - dp(16), None
##            font_size: root.title_size
##            font_name: root.title_font
##            halign: root.title_align
##
##        BoxLayout:
##            id: container

#<ModalView>:
#    canvas:
#        Color:
#            rgba: root.background_color[:3] + [root.background_color[-1] * self._anim_alpha]
#        Rectangle:
#            size: self._window.size if self._window else (0, 0)

#        Color:
#            rgb: 1, 0, 0



#<MDPopup@Popup>:
#    #background: 'art/whitess.png'    
#    background_color: (1,0,0,1)
#    #background_normal: None
#    canvas:
#        Color:
#            rgba: (0,0,1,1)
#        Rectangle:
#            pos: self.x, self.y
#            size: dp(100), dp(100)
#    text: ''
#    add_width: dp(200)
#    minimum_width: dp(500)
#    id: popup_dialog
#    size_hint: (None,None)
#    height: dp(200)
#    pos_hint: {'center_x': .5, 'center_y': .5}
#    background_color: (1,1,1,0)
#    Label:
#        id: text
#        font_size: '17dp'
#        font_style: 'Body1'
#        #halign: 'justify'
#        text: root.text
#        size_hint: None,None
#        valign: 'middle'
#        #texture_size: self.size
#        text_size: root.width-dp(50), None
#        width: self.texture_size[0]
#        
#''')
class ListItem(OneLineListItem):
    def refresh_detail(self,ind):
        pass
    def on_release(self):
        pass

class DetailSpacer(Widget):
    # Internal class, not documented.
    pass

class MDDialog(Popup):
    pass

class MDBoxLayout(ThemableBehavior,BackgroundColorBehavior,BoxLayout):
    pass

class MDFloatLayout(ThemableBehavior,BackgroundColorBehavior,FloatLayout):
    pass

class DetailLabel(MDLabel):
    pass

#class Papiview(Widget):
#    pass

class MDPopup(MDDialog):
    pass
