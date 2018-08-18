#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 19:46:36 2018

@author: spopoff
"""

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.settings import SettingString,SettingItem,SettingTitle,SettingsPanel,InterfaceWithTabbedPanel,InterfaceWithSidebar,InterfaceWithTabbedPanel,SettingsWithNoMenu,Settings,InterfaceWithNoMenu,InterfaceWithSpinner,ContentPanel
from kivymd.label import MDLabel
from kivy.properties import ObjectProperty,ListProperty,StringProperty,BooleanProperty
from kivymd.backgroundcolorbehavior import (BackgroundColorBehavior,
                                            SpecificBackgroundColorBehavior)
from kivymd.theming import ThemableBehavior
from kivy.uix.spinner import Spinner

from kivy.compat import string_types, text_type
from kivy.uix.dropdown import DropDown
from kivymd.bottomsheet import MDListBottomSheet
from kivymd.button import MDIconButton, MDRaisedButton



Builder.load_string('''

<-SettingItem>:
    size_hint: .25, None
    height: dp(70)
    content: content
    canvas:
        Color:
            rgba: 47 / 255., 167 / 255., 212 / 255., self.selected_alpha
        Rectangle:
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgb: .2, .2, .2
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

    BoxLayout:
        pos: root.pos[0],root.pos[1]
        id: content      

<-SettingsPanel>:
    spacing: 5
    padding: dp(24)
    size_hint_y: None
    height: self.minimum_height
    md_bg_color: app.theme_cls.primary_color

    MDLabel:
        
        size_hint_y: None
        text: root.title
        font_style: 'Title'
        theme_text_color: 'Primary'
        height: max(50, self.texture_size[1] + 20)
        color: (.9, .9, .9, 1)
        
        

        canvas.after:
            Color:
                rgb: .2, .2, .2
            Rectangle:
                pos: self.x, self.y - 2
                size: self.width, 1 
 
<MDSettingBool>:
    BoxLayout:
        pos: root.pos
        size: root.width, root.height
        MDLabel:
            font_style: 'Subhead'
            theme_text_color: 'Primary'
            text: u'{0}'.format(root.title or '')  
            size_hint_x:0.95
        MDCheckbox:
            text: 'Boolean'
            size_hint_x:0.05
            id: switch     
            align:  'right'
            pos: root.pos
            active: bool(root.values.index(root.value)) if root.value in root.values else False
            on_active: root.value = root.values[int(args[1])]

#<MyMDSpinner@Spinner>:
#    canvas:
#        Color: 
#            rgb: (1,1,1)





<MDSettingString>:
    MDTextField:
        id: textinput
        text: root.value or ''
        pos: root.pos
        font_size: '16sp'  
        hint_text: u'{0}'.format(root.title or '')      
        helper_text:u'{0}'.format(root.desc or '')  
        helper_text_mode: "on_focus" 
        on_text_validate: 
            root._validate()

#<MDSettingPassword>:
#    MDTextField:
#        id: textinput
#        password: True
#        text: root.value or ''
#        pos: root.pos
#        font_size: '16sp'  
#        hint_text: u'{0}'.format(root.title or '')      
#        helper_text:u'{0}'.format(root.desc or '')  
#        helper_text_mode: "on_focus" 
#        on_text_validate: 
#            root._validate()   

<SpinnerOption>:
    size_hint_y: None
    height: '48dp'

<MDSettingSpinner>:
    BoxLayout:
        pos: root.pos
        size: root.width, root.height
        MDLabel:
            font_style: 'Subhead'
            theme_text_color: 'Primary'
            text: u'{0}'.format(root.title or '')  
            size_hint_x:0.95
        MDRaisedButton:
            font_style: 'Subhead'
            theme_text_color: 'Primary'
            text: u'{0}'.format(root.value or '')  
            size_hint_x:0.95
            size_hint: None, None
            size: 4 * dp(48), dp(48)
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            on_release: root._open()        
        #Spinner:
        #    text: 'Home'
        #    values: ('Home', 'Work', 'Other', 'Not defined')
        #    size_hint_y: None
        #    height: '48dp'
        #MDLabel:
        #    id: select_label
        #    font_style: 'Subhead'
        #    theme_text_color: 'Primary'
        #    text: u'{0}'.format(root.select_item  or '')  
        #    size_hint_x:0.95
        DropDown:
            id: dropdown
            on_parent: self.dismiss()
            on_select: select_label.text = '{}'.format(args[1])

<-MenuSpinner>:
    orientation: 'horizontal'
    size_hint_y: None
    height: '50dp'
    spinner: spinner
    spinner_text: spinner.text
    close_button: button
    Spinner:
        id: spinner
    MDRaisedButton:
        text: 'Close'
        id: button
        size_hint_x: None
        height: min(dp(200), root.height) 
        width: min(dp(200), 0.4*root.width)
        font_size: '15sp'

<InterfaceWithTabbedPanel>:
    md_bg_color: app.theme_cls.primary_color

<SettingsPanel>:
    md_bg_color: app.theme_cls.primary_color

#self.root.theme_cls.bg_dark
           
''')
#     bool(root.values.index(root.value)) if root.value in root.values else False
class MDSettingBool(SettingItem):
    values = ListProperty(['0', '1'])

class SpinnerOption(MDLabel):
    '''Special button used in the :class:`Spinner` dropdown list. By default,
    this is just a :class:`~kivy.uix.button.Button` with a size_hint_y of None
    and a height of :meth:`48dp <kivy.metrics.dp>`.
    '''
    pass



class MDSettingSpinner(BackgroundColorBehavior,SettingItem):
    items =  StringProperty('')   
    #select_item =  StringProperty('<Not set>') 
    #items = '{0}'.format(values).split(',')
    values = ListProperty()
    

    def __init__(self, **kwargs):
        #self._dropdown = None
        super(MDSettingSpinner, self).__init__(**kwargs)
        self.values = '{0}'.format(self.items).split(',')
        self.value = self.values[0]
        #build_dropdown = self._build_dropdown
        #self.ids.con_type.bind(on_release=lambda: self._open())
        #build_dropdown()

    def _update(self,value):
        self.value = value.text

    
    def _open(self):
        print(self.value)

        bs = MDListBottomSheet()
        for val in self.values:
            bs.add_item(val, lambda x: self._update(x))
        bs.open()


    def on_value(self,*args):
        value = self.value.strip()
        self.panel.set_value(self.section, self.key, value)

   #def _build_dropdown(self, *largs):
    #    pass    
    #self.select_label.bind(on_release=lambda: dropdown.open())
        #for item in ['aaa','bbb']#self.items:
            #label = MDLabel(text=item, size_hint_y=None, height=44)
    #        label.bind(on_release=lambda label: dropdown.select(label.text))
            #self.ids.dropdown.add_widget(label)
        
        
    #def _build_dropdown(self, *largs):
        #if self._dropdown:
        #    self._dropdown.unbind(on_select=self._on_dropdown_select)
        #    self._dropdown.unbind(on_dismiss=self._close_dropdown)
        #    self._dropdown.dismiss()
        #    self._dropdown = None
        #cls = self.dropdown_cls
        #if isinstance(cls, string_types):
        #    cls = Factory.get(cls)
        #self._dropdown = cls()
        #self._dropdown.bind(on_select=self._on_dropdown_select)
        #self._dropdown.bind(on_dismiss=self._close_dropdown)
        #self._update_dropdown()

#    def _update_dropdown_size(self, *largs):
#        if not self.sync_height:
#            return
#        dp = self._dropdown
#        if not dp:
#            return

#        container = dp.container
#        if not container:
#            return
#        h = self.height
#        for item in container.children[:]:
#            item.height = h

#    def _update_dropdown(self, *largs):
#        dp = self._dropdown
#        cls = self.option_cls
#        self.values = '{0}'.format(self.items).split(',')
#        values = self.values
#        text_autoupdate = self.text_autoupdate
#        if isinstance(cls, string_types):
#            cls = Factory.get(cls)
#        dp.clear_widgets()
#        for value in values:
#            item = cls(text=value)
#            item.height = self.height if self.sync_height else item.height
#            item.bind(on_release=lambda option: dp.select(option.text))
#            dp.add_widget(item)
#        if text_autoupdate:
#            if values:
#                if not self.text or self.text not in values:
#                    self.text = values[0]
#            else:
#                self.text = ''

#    def _toggle_dropdown(self, *largs):
#        if self.values:
#            self.is_open = not self.is_open

#    def _close_dropdown(self, *largs):
#        self.is_open = False

#    def _on_dropdown_select(self, instance, data, *largs):
#        self.text = data
#        self.is_open = False

#    def on_is_open(self, instance, value):
#        if value:
#            self._dropdown.open(self)
#        else:
#            if self._dropdown.attach_to:
#                self._dropdown.dismiss()


#class MDSettingSpinner(BackgroundColorBehavior,SettingItem):
#    values =  StringProperty('<No title set>')    
#    items = '{0}'.format(values).split(',')
#
#    def __init__(self, **kwargs):
#        super(MDSettingSpinner, self).__init__(**kwargs)
#        self.select_label.bind(on_release=lambda: dropdown.open())
#        for item in ['aaa','bbb']#self.items:
#            label = MDLabel(text=item, size_hint_y=None, height=44)
#            label.bind(on_release=lambda label: dropdown.select(label.text))
#            self.ids.dropdown.add_widget(label)
#    
#    def on_touch_up(self, touch):
#        pass#self.ids.dropdown.open()
    
    
class MDSettingString(BackgroundColorBehavior,SettingItem):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return
        #touch.grab(self)
        #self.selected_alpha = 1
        return super(SettingItem, self).on_touch_down(touch)
    def on_touch_up(self, touch):
        pass
    
    def _validate(self):
        value = self.ids.textinput.text.strip()
        self.value = value
        if not self.section or not self.key:
            return
        # get current value in config
        #panel = self.panel
        if not isinstance(value, string_types):
            value = str(value)
        self.panel.set_value(self.section, self.key, value)

class MDSettingPassword(MDSettingString):
    def __init__(self, **kwargs):
        super(MDSettingPassword, self).__init__(**kwargs)
        self.ids.textinput.password = True
    #def on_touch_down(self, touch):
    #    if not self.collide_point(*touch.pos):
    #        return
    #    if self.disabled:
    #        return
    #    #touch.grab(self)
    #    #self.selected_alpha = 1
    #    return super(SettingItem, self).on_touch_down(touch)
    #def on_touch_up(self, touch):
    #    pass
   # 
   # def _validate(self):
   #     value = self.ids.textinput.text.strip()
   #     self.value = value
        
class MDSettings(ThemableBehavior,BackgroundColorBehavior,Settings):
    pass

#class MDContentPanel(ThemableBehavior,BackgroundColorBehavior,ContentPanel):
#    pass

class MDSettingsWithSidebar(MDSettings):
    '''A settings widget that displays settings panels with a sidebar to
    switch between them. This is the default behaviour of
    :class:`Settings`, and this widget is a trivial wrapper subclass.

    '''

class MDSettingsWithSpinner(MDSettings):
    '''A settings widget that displays one settings panel at a time with a
    spinner at the top to switch between them.

    '''
    def __init__(self, *args, **kwargs):
        self.interface_cls = InterfaceWithSpinner
        super(MDSettingsWithSpinner, self).__init__(*args, **kwargs)

class MDSettingsWithTabbedPanel(MDSettings):
    '''A settings widget that displays settings panels as pages in a
    :class:`~kivy.uix.tabbedpanel.TabbedPanel`.
    '''

    __events__ = ('on_close', )

    def __init__(self, *args, **kwargs):
        self.interface_cls = InterfaceWithTabbedPanel
        super(MDSettingsWithTabbedPanel, self).__init__(*args, **kwargs)

    def on_close(self, *args):
        pass

class MDSettingsWithNoMenu(MDSettings):
    '''A settings widget that displays a single settings panel with *no*
    Close button. It will not accept more than one Settings panel. It
    is intended for use in programs with few enough settings that a
    full panel switcher is not useful.

    .. warning::

        This Settings panel does *not* provide a Close
        button, and so it is impossible to leave the settings screen
        unless you also add other behaviour or override
        :meth:`~kivy.app.App.display_settings` and
        :meth:`~kivy.app.App.close_settings`.

    '''
    def __init__(self, *args, **kwargs):
        self.interface_cls = MDInterfaceWithNoMenu
        super(MDSettingsWithNoMenu, self).__init__(*args, **kwargs)
        
class MDInterfaceWithNoMenu(ContentPanel):
    '''The interface widget used by :class:`SettingsWithNoMenu`. It
    stores and displays a single settings panel.

    This widget is considered internal and is not documented. See the
    :class:`ContentPanel` for information on defining your own content
    widget.

    '''
    def add_widget(self, widget):
        if self.container is not None and len(self.container.children) > 0:
            raise Exception(
                'ContentNoMenu cannot accept more than one settings panel')
        super(MDInterfaceWithNoMenu, self).add_widget(widget)


#class MDSettingsWithNoMenu(ThemableBehavior,BackgroundColorBehavior,SettingsWithNoMenu):
#    pass
