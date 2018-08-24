# -*- coding: utf-8 -*-



from __future__ import print_function



from kivy.config import ConfigParser, Config
Config.set('kivy','log_dir', 'logs')
Config.set('kivy','log_name', 'kivy_%y-%m-%d_%_.txt')
#Config.setdefaults('kivy', {
#            'log_enable': 1,
#            'log_level': 'info',
#            'log_dir':'./',
#            'log_name':'log',
#})

from kivy.app import App
__version__ = '0.1.2'

from kivy import kivy_home_dir

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
#from kivy.uix.settings import Settings
#,ContentPanel

from kivy.resources import resource_add_path
from kivymd.card import MDSeparator
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform



from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton, MDRaisedButton#, BaseRectangularButton, BaseFlatButton, BasePressedButton, BaseRoundButton
from kivymd.spinner import MDSpinner
#from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import OneLineListItem#ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
#from kivymd.snackbar import Snackbar
#from kivymd.theming import ThemeManager
#from kivymd.time_picker import MDTimePicker
from kivymd.progressbar import MDProgressBar 
from kivymd.theming import ThemableBehavior, ThemeManager
#import kivymd.list

from kivy.logger import Logger, LoggerHistory

from kivy.uix.settings import SettingsWithSidebar,SettingsWithNoMenu
from mdsettings import MDSettingString,MDSettingSpinner,MDSettingsWithTabbedPanel,MDSettingsWithSidebar,MDSettingPassword,MDSettingBool,MDSettingsWithSpinner,MDSettingsWithNoMenu
from kivy.uix.settings import SettingString, SettingItem

from kivymd.backgroundcolorbehavior import (BackgroundColorBehavior,
                                            SpecificBackgroundColorBehavior)



from paper_list import PaperListItem


import unidecode
import re
import os


#import threading




#%%


main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem
#:import Settings kivy.uix.settings
##:import SettingsString kivy.uix.settings.SettingsString
##:import SettingsItem kivy.uix.settings.SettingsItem 

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "Menu"
        NavigationDrawerIconButton:
            id: lib_medu_btn
            icon: 'library-books'
            text: "Library"
            on_release: app.root.ids.scr_mngr.current = 'library'
        NavigationDrawerIconButton:
            id: setting_menu_btn
            icon: 'settings'
            text: "Settings"
            on_release: app.select_settings_scr()
        NavigationDrawerIconButton:
            id: info_menu_btn
            icon: 'help-circle-outline'
            text: "Information"
            on_release: app.root.ids.scr_mngr.current = 'information'
        NavigationDrawerIconButton:
            id: logs_menu_btn
            icon: 'code-brackets'#'developer-board'
            text: "Logs"
            on_release: app.root.ids.scr_mngr.current = 'logs'


    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'Papiview'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            #background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['eraser', lambda x: app.clear_cache()],\
                                 ['refresh', lambda x: app.load_library()],\
                                 ['download', lambda x: app.load_offline()]]
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'library'
                MDTabbedPanel:
                    id: tab_panel
                    tab_display_mode:'text' 

                    MDTab:
                        id: lib_tab
                        name: 'library'
                        text: "Library" # Why are these not set!!!
                        #icon: "playlist-play"
                        #md_bg_color: app.theme_cls.bg_dark
                        ScrollView:
                            do_scroll_x: False
                            MDList:
                                background_color: app.theme_cls.bg_dark
                                id: ml
                    MDTab:
                        id: details_tab
                        name: 'details'
                        text: 'Details'
                        #icon: "movie"
                        JournalDetails:
                            id: journal_details


                    
                            
            Screen:
                name: 'settings'
                id: settings_screen
                BoxLayout:
                    id:settings_box
                    title: 'Settings'

            Screen:
                name: 'information'
                id: information_screen
                ScrollView:
                    GridLayout:
                        id:information_box
                        title: 'Information'
                        cols: 1
                        size_hint: 1.,None    
                        height: self.minimum_height                  
                        padding: dp(16)
                        MDLabel:
                            id: info_title
                            size_hint: 1.,None 
                            height: self.texture_size[1]
                            theme_text_color: 'Primary'
                            text: self.parent.title
                            font_style: 'Title'
                            padding: 0,dp(4)
                        MDLabel:
                            size_hint: 1.,None 
                            height: self.texture_size[1]
                            id: info_content
                            font_style: 'Subhead'#'Body1'
                            theme_text_color: 'Primary'
                            markup: True
                            halign: 'justify'
                            padding: 0,dp(4)
                            text: 'test [color=ff3333]Hello[/color]'
                            on_ref_press:
                                from android_interactions import open_url
                                #import webbrowser
                                open_url(args[1])
                                #webbrowser.open(args[1])

            Screen:
                name: 'logs'
                id: logs_screen
                GridLayout:
                    cols: 1
                    padding: dp(16)
                    ScrollView:
                        GridLayout:
                            id:information_box
                            title: 'Logs'
                            cols: 1
                            size_hint: 1.,None    
                            height: self.minimum_height                  
                            
                            MDLabel:
                                #id: logs_title
                                size_hint: 1.,None 
                                height: self.texture_size[1]
                                theme_text_color: 'Primary'
                                text: self.parent.title
                                font_style: 'Title'
                                padding: 0,dp(4)
                            MDLabel:
                                size_hint: 1.,None 
                                height: self.texture_size[1]
                                id: logs_content
                                font_style: 'Subhead'#'Body1'
                                theme_text_color: 'Primary'
                                markup: True
    #                            shorten: True 
    #                            shorten_from: 'right'
                                text: 'test [color=ff3333]Hello[/color]'   
                                padding: 0,dp(4) 
                    AnchorLayout:
                        #cols: 1
                        anchor_x: 'center'
                        anchor_y: 'center'
                        size_hint: 1,None
                        height: dp(54)
                        MDRaisedButton:
                            #size_hint: None,None
                            padding: dp(16)
                            text: 'Refresh'
                            on_release:
                                app.load_logs()

        
<DetailSpacer>:
    size_hint_y: None
    height: 20
    canvas:
        Color:
            rgb: .5, .5, .5
        Rectangle:
            pos: self.x, self.center_y
            size: self.width, 1   

<File>:
    MDLabel:
        size_hint_y: None
        theme_text_color: 'Primary'
        text: root.filename or ''
               
                
<JournalDetails>:
    details_content: details_content
    ScrollView:
        do_scroll_x: False
#        size_hint: (1, None)
        #size: (Window.width, Window.height)
        
        GridLayout:
            id: details_content
            size_hint_y: None
            cols: 1
            padding: dp(20)
#            orientation: 'vertical'
#            pos: root.pos[0]+dp(200),root.pos[1]+dp(20)
#            minimum_height: self.height
            height: 1.2*self.minimum_height
            #minimum_height: self.setter('height')
            #size: root.width, root.height
            MDLabel:
                id: title
                size_hint_y: None
                text_size: self.width, None
                height: self.texture_size[1]
                font_style: 'Headline'
                theme_text_color: 'Primary'
                text: 'Title'
    
            DetailSpacer:
            MDLabel:
                id: authors
                size_hint_y: None
                text_size: self.width, None
                height: self.texture_size[1]
                font_style: 'Subhead'
                theme_text_color: 'Primary'
                text: 'Authors'

            MDLabel:
                id: details
                size_hint_y: None
                text_size: self.width, None
                height: self.texture_size[1]
                font_style: 'Subhead'
                theme_text_color: 'Primary'
                text: 'Journal and article information'
    
            DetailSpacer:
            MDLabel:
                id: abstract
                size_hint_y: Nonec
                text_size: self.width, None
                height: self.texture_size[1]
                font_style: 'Subhead'
                theme_text_color: 'Primary'
                text: 'Abstract'
                size_hint_y: None
                
            DetailSpacer:
            MDList:
                id: files_layout
                size_hint_y: None

            


            
<-MDTabbedPanel>:
    id: panel
    orientation: 'vertical' if panel.tab_orientation in ['top','bottom'] else 'horizontal'
    BoxLayout:
        id: scroll_view
        size_hint_y: None
        #height: dp(48)
        height: panel._tab_display_height[panel.tab_display_mode]
        
        MDTabBar:
            id: tab_bar
            size_hint_y: None
            size_hint_x: 0.55
            #height: root.height
            height: panel._tab_display_height[panel.tab_display_mode]
            md_bg_color: panel.tab_color or panel.theme_cls.primary_color
            canvas:
                # Draw bottom border
                Color:
                    rgba: (panel.tab_border_color or panel.tab_color or panel.theme_cls.primary_dark)
                Rectangle:
                    size: (self.width,dp(2))
        MDBoxLayout:   
            id: box
            size_hint_x: 0.45
            md_bg_color: panel.tab_color or panel.theme_cls.primary_color
            MDIcon:
                color: 1,0.,0.,1
                id: icon_search
                size_hint_x: None
                theme_text_color: 'Primary'
                icon: 'magnify' 
                width:dp(30)
                halign: 'right'      
            MDSearchInput:
                #size_hint_x: 1
                width: box.width-icon_search.width
                id: search_input
                padding: dp(12)#dp(15)
                on_text: root._filter_search(self.text)


    ScreenManager:
        id: tab_manager
        current: root.current
        screens: root.tabs
        transition: sm.SlideTransition()

<MDIcon@MDLabel>:
    icon: 'magnify'
    font_style: 'Icon'
    text: u"{}".format(md_icons[self.icon])
    theme_text_color: root.theme_text_color
    text_color: root.text_color
    #disabled: root.disabled
    valign: 'middle'
    halign: 'center'
    #opposite_colors: root.opposite_colors 


   
    
<DetailLabel>:
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
    font_style: 'Subhead'
    theme_text_color: 'Primary'
    
<ProgressDialog>:
    size_hint: (.8, None)
    height: dp(250)
    auto_dismiss: True
    GridLayout:
        size_hint_y: None
        cols: 1
        MDProgressBar:
            id: progress_bar
        MDLabel:
            font_style: 'Subhead'
            theme_text_color: 'Primary'
            text: root.info

<LoadingDialog>:
    size_hint: (.8, None)
    height: dp(200)
    auto_dismiss: True
    GridLayout:
        size_hint_y: None
        cols: 1
        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            active: True
        MDLabel:
            font_style: 'Subhead'
            theme_text_color: 'Primary'
            text: root.info

#<Spinner>
#    size_hint: None, None
#    size: dp(46), dp(46)
#    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
#    active: True if chkbox.active else False

#<SettingPassword>:
#	PasswordLabel:
#		text: '(set)' if root.value else '(unset)'
#		pos: root.pos
#		font_size: '15sp'

 
<MDSearchInput@TextInput>:
    font_size: '15dp'
    background_color: app.theme_cls.primary_color
    foreground_color: 1,1,1,1
    background_normal: 'art/textinput.png'
    background_active: 'art/textinput.png'
    cursor_color: 1.,0.25,0.5,1.
    canvas.after:
        Color:
            rgba: .8, .8, .8, .7
        Rectangle:
            pos: self.x+self.padding[0], self.y+9
            size: self.width-2*self.padding[0], 2.5  
 
<SearchInput@TextInput>:
    font_size: '14dp'
    background_color: 1,1,1,1
    foreground_color: 1,1,1,1
    background_normal: 'art/textinput.png'
    background_active: 'art/textinput.png'
    cursor_color: get_color_from_hex('#000000')
    canvas.before:
        Color:
            rgba: get_color_from_hex('#000000')
    canvas.after:
        Color:
            rgb: 1,1,1,1#get_color_from_hex('#0f192e')
        Ellipse:
            angle_start:180
            angle_end:360
            pos:(self.pos[0] - self.size[1]/2.0, self.pos[1])
            size: (self.size[1], self.size[1])
        Ellipse:
            angle_start:360
            angle_end:540
            pos: (self.size[0] + self.pos[0] - self.size[1]/2.0, self.pos[1])
            size: (self.size[1], self.size[1])
        Color:
            rgba: get_color_from_hex('#3f92db')
        Line:
            points: self.pos[0] , self.pos[1], self.pos[0] + self.size[0], self.pos[1]
        Line:
            points: self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]
        Line:
            ellipse: self.pos[0] - self.size[1]/2.0, self.pos[1], self.size[1], self.size[1], 180, 360
        Line:
            ellipse: self.size[0] + self.pos[0] - self.size[1]/2.0, self.pos[1], self.size[1], self.size[1], 360, 540

           
<MDTextInput@TextInput>:
    canvas:
        Color: 
            rgb: (1,1,1)
    

<MDPopup@MDDialog>:
    text: ''
    minimum_width: dp(350)
    id: popup_dialog
    size_hint: (None,None)
    #width: self._action_area.width #+ dp(00)
    #width: dp(184)
    height: dp(200)
    #texture_size: content.size
    MDLabel:
        id: text
        size: self.texture_size
        font_style: 'Body1'
        theme_text_color: 'Secondary'
        text: root.text
        size_hint_y: None
        valign: 'top'
        texture_size: self.size


        
'''



def get_info(dic,key,default = ''):
        return u'{0}'.format(clean_text(dic[key])) if key in dic.keys() else default

def clean_text(text):
       return re.sub(r'\s+',' ',text)
    #return text.replace('\n',' ').replace('\t',' ')

#class MDIcon(BaseRoundButton, BaseFlatButton, BasePressedButton):
#    icon = StringProperty('checkbox-blank-circle')


#class ExitPopup(MDDialog):
#    text = StringProperty('')        
#    def __init__(self, **kwargs):
#        super(ExitPopup, self).__init__(**kwargs)
#        self.text = 'Do you want to quit?'
#        self.ids.dialog.add_action_button("Close me!",
#                                      action=lambda *x: self.dismiss_callback())
#        self.open()
#
#    def dismiss_callback(self):
#        self.dialog.dismiss()
#        App.get_running_app().Exit()

class MDPopup(MDDialog):
    pass

class YNPopup(MDPopup):
    def __init__(self, **kwargs):
        super(YNPopup, self).__init__(**kwargs)
        self.add_action_button("No",
                                      action=lambda *x: self.on_no(x))
        self.add_action_button("Yes",
                                      action=lambda *x: self.on_yes(x))

    def _on_yes(self):
        self.on(yes)
        self.dismiss()

    def on_yes(self):
        pass

    def on_no(self,*args):
        self.dismiss()
        

class ExitPopup(MDPopup):

    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)
        self.text = 'Do you want to quit?'
        self.title = "Close Application"
        self.add_action_button("Back",
                               action=lambda *x: self.dismiss_callback())
        self.add_action_button("Quit",
                               action=lambda *x: self.quit_callback())
        self._action_area.bind(width= lambda x,y: self.setter('width')(x,y+dp(100)))

        self.open()

    def dismiss_callback(self):
        self.dismiss()

    def quit_callback(self):
        App.get_running_app().stop()


class LoadingDialog(MDDialog):
    info = StringProperty('')
    def stop(self):
        pass
    def __init__(self,**kwargs):
        super(LoadingDialog, self).__init__(**kwargs)
        self.add_action_button("Cancel", action=lambda x: self.stop())
        

class ProgressDialog(MDDialog):
    info = StringProperty('None')
    def stop(self):
        pass
    def __init__(self,**kwargs):
        super(ProgressDialog, self).__init__(**kwargs)
        self.add_action_button("Cancel", action=lambda x: self.stop())
        
        

class DetailLabel(MDLabel):
    pass

class MDBoxLayout(ThemableBehavior,BackgroundColorBehavior,BoxLayout):
    pass

class MDFloatLayout(ThemableBehavior,BackgroundColorBehavior,FloatLayout):
    pass


class File(BoxLayout):
    filename = ' '
    def __init__(self, **kwargs):
        super(File, self).__init__(**kwargs)
#        self.filename = 'no file'
#    pass

class DetailSpacer(Widget):
    # Internal class, not documented.
    pass

class ListItem(OneLineListItem):
    def refresh_detail(self,ind):
        pass
    def on_release(self):
        pass



class JournalDetails(FloatLayout):
#    details_content = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(JournalDetails, self).__init__(**kwargs)
        self.document = None
#        self.details_content.bind(minimum_height=self.details_content.setter('height'))
    def openFile(self,folder,file_name):
        pass
    def openUrl(self,url):
        pass
    
    def updateDetails(self,document,folder): 
        def Doc(key,default=''):
            return get_info(document,key,default = default)


        self.ids.title.text = '{0}'.format(document['title']) \
            if 'title' in document.keys() else 'No document title'
        self.ids.authors.text = ''
        if 'author' in document.keys():
            self.ids.authors.text = u'{0}'.format(clean_text(document['author']))

        
    
        self.ids.abstract.text = Doc('abstract','No abstract')

        details = []
        details.append(Doc('journal') if Doc('journal') else 'arxiv' if 'eprint' in document.keys() else '')
        details.append('Vol. '+ Doc('volume','0')) 
        details.append('Issue '+ Doc('number','0'))
        if 'pages' in document.keys():
            details.append('pp. '+ Doc('pages', 'NA'))
        self.ids.details.text = ', '.join(details)+' (%s)' % Doc('year', '0000')

        #self.ids.abstract.text = 
            #u'{0}'.format(clean_text(document['abstract'])) \
            #if 'abstract' in document.keys() else 'No abstract'

        self.ids.files_layout.clear_widgets()
        
        if 'files' in document.keys():
            title_label = DetailLabel(text='Files:')
            self.ids.files_layout.add_widget(title_label)
#            if not isinstance(document['file'],list):
#                file_list = [document['files']]
#            else:
            
            file_list = document['files']
            
            for file_name in file_list:
#                new_file = File(filename=file_name)
                
                new_file = ListItem(text = file_name)
                new_file.on_release = lambda : self.openFile(folder,file_name)
                self.ids.files_layout.add_widget(new_file)
           
        if 'url' in document.keys():
            title_label = DetailLabel(text='Link:')
            self.ids.files_layout.add_widget(title_label)
            url = document['url']
#            for url in url_list:
            
#                new_file = File(filename=file_name)
                
            new_file = ListItem(text = url)
            new_file.on_release = lambda : self.openUrl(url)
            self.ids.files_layout.add_widget(new_file)



class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)
         

class Papiview(App):
    use_kivy_settings = False
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Papiview"
    settings_cls = MDSettingsWithNoMenu
    app_version = StringProperty(__version__)
    #MDSettingsWithSidebar
    #MDSettingsWithTabbedPanel
    #MDSettingsWithSpinner
    #MDSettingsWithNoMenu


    
    def show_error_dialog(self,title,message):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=message,
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title=title,
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()
    

        
    def build(self):
#        config = self.config
        main_widget = Builder.load_string(main_widget_kv)
        #main_widget = Builder.load_file('papiview.kv')
        self.theme_cls.theme_style = 'Dark'

#        self.bottom_navigation_remove_mobile(main_widget)
        self.doc_list = []
#        self.dir_list = []
        self.loader = None
        self.progress_dialog = None
        list
        
        
        return main_widget
    


    def build_config(self, config):
#        SettingBoolean(values=['1','2'])
        config.setdefaults('webdav', {
            'host': '',
            'username': '',
            'password': '',
            'path':"",
            'https':'1'
        })
        config.setdefaults('sftp', {
            'host': '',
            'username': '',
            'password': '',
            'path':"",
        })
        config.setdefaults('global', {
            'connection_type': 'webdav'
        })

    def post_build_init(self, *args):
        #if platform == 'android':
            #import android
            #android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.key_handler)
        
        self.load_info()
        self.load_logs()
    
    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        '''
        Handles keybaord/hardware buttons interactions
        '''
        # Escape or android back button
        if keycode1 in [27, 1001]:
            self.go_back()
            return True
        return False

    def get_application_config(self, defaultpath=''):
        return os.path.join(self.user_data_dir,"config.ini")


        
        
    def display_settings(self,settings):
        self.root.ids.settings_screen.add_widget(settings)
#        if settings not in self.root.ids.settings_panel.children:
            #self.root.ids.settings_panel
            #self._app_window.add_widget(settings)
#            return True
#        return False
        
        
    def build_settings(self,settings):
        settings.register_type('mdstring', MDSettingString)
        settings.register_type('mdbool', MDSettingBool)
        settings.register_type('mdpassword', MDSettingPassword)
        settings.register_type('mdspinner', MDSettingSpinner)
        settings.add_json_panel('Global', self.config, 'settings.json')   
        settings.add_json_panel('Webdav', self.config, 'webdav.json')     
        settings.add_json_panel('SFTP', self.config, 'sftp.json')  
        self.settings = settings
        self.settings.md_bg_color = self.root.theme_cls.bg_dark
        settings.on_config_change = self.on_config_change
     
    
    

    def refresh_details(self,ind):
        '''
        Update the content of the detail panel with the information of the currently
        selected document.
        '''
        document = self.filt_doc_list[ind]
        #print(document.keys())
        folder = document.get_main_folder_name()

        #folder = self.dir_list[ind]
        # switch to the details tab
        self.root.ids.details_tab.on_tab_press()
        # clear previous details
#        self.root.ids.details_tab.clear_widgets()
        self.root.ids.journal_details.openFile = lambda x,y: Clock.schedule_once(lambda z: self.open_file(x,y),1.)
        #self.root.ids.journal_details.openFile = lambda x,y: Clock.schedule_once(lambda z: self.loader.open_file(x,y),1.)
        self.root.ids.journal_details.openUrl = lambda x: Clock.schedule_once(lambda z: self.loader.open_url(x),1.)
        self.root.ids.journal_details.updateDetails(document,folder)
# 

    def open_file(self,paper_dir,file_name):
        self.connect_loader()
        self.loader.open_file(paper_dir,file_name)
#
    def go_back(self):
        if self.root.ids.scr_mngr.current == 'library' and self.root.ids.tab_panel.ids.tab_manager.current == 'library':
            ExitPopup()            
            #app.Exit()
        elif self.root.ids.scr_mngr.current == 'library':
            self.root.ids.lib_tab.on_tab_press()
        else:
            self.root.ids.scr_mngr.current = 'library'
            
            ## Manually set all button in the menu to not active except the first one
            ## i.e. go back selecting the library button
            for c in  self.root.ids.nav_drawer._list.children:
                c._active = True if c.text == 'Library' else False  
 

    def select_settings_scr(self):
        self.root.ids.scr_mngr.current = 'settings'
       
    def save_settings(self):
        self.init_loader()

    def load_logs(self):
        #self.root.ids.info_title.text = 'Papiview %s' % str(self.app_version) 
        
#        log_dir = Config.get('kivy', 'log_dir')
#        log_name = Config.get('kivy', 'log_name')
#        _dir = kivy_home_dir
#        if log_dir and os.path.isabs(log_dir):
#            _dir = log_dir
#        else:
#            _dir = os.path.join(_dir, log_dir) 
#        log_path = os.path.join(_dir, log_name)

#        print('log_path '*40)
#        print(log_path)

#        try: 
#            with open('log.txt', 'r') as infofile:
#                self.root.ids.logs_content.text = infofile.read() 
#        except EnvironmentError:
#            self.root.ids.logs_content.text = 'Empty'
#            print(Config.get('kivy', 'log_enable'))
        
        print(LoggerHistory.history)
        self.root.ids.logs_content.text = '\n'.join([l.msg for l in LoggerHistory.history])

    def load_info(self):
        self.root.ids.info_title.text = 'Papiview %s' % str(self.app_version)
        with open('info.md', 'r') as infofile:
            self.root.ids.info_content.text = infofile.read() 
        
        
    def init_loader(self):
        from loader import Loader

        self.loader = Loader(self,root_dir=self.user_data_dir)

    def connect_loader(self):
        protocol = self.config.get('global','connection_type')
        if protocol == 'webdav':
            options = {
             'host': self.config.get('webdav','host'),
             'username': self.config.get('webdav','username'),
             'password': self.config.get('webdav','password'),
             'protocol': 'https' if self.config.get('webdav','https') == '1' else 'http',
             'path': self.config.get('webdav','path'),
            }
        elif protocol == 'sftp':
            options = {
             'host': self.config.get('sftp','host'),
             'username': self.config.get('sftp','username'),
             'password': self.config.get('sftp','password'),
             'path': self.config.get('sftp','path'),
            }
        self.loader.connect(protocol,options)
        
     
    def _load_library(self,offline):
        self.init_loader()
        self.connect_loader()
        self.refresh_cache(download_all=offline)    

        
        
    def load_library(self,offline=False):
        
        Clock.schedule_once(lambda x: self._load_library(offline = offline),0.5)

    def _load_offline(self):
        popup = YNPopup()
        popup.text = "Do you want to donwload all the documents for offline use?\nThis may take a while"
        popup.on_yes = lambda x: self.load_library(offline = True)
        #popup.on_yes = lambda x: self.download_all_documents()
        popup.open()

    def load_offline(self):
        Clock.schedule_once(lambda x: self._load_offline(),0.5)

    def download_all_documents(self):
        self.connect_loader()
        for doc in self.doc_list:
            paper_dir = doc.get_main_folder_name()
            if 'files' in doc.keys():              
                file_list = doc['files']
                for file_name in file_list:
                    self.loader.download_file(paper_dir,file_name)
                    
        
        
    def refresh_cache(self,download_all=False):
        
        self.open_progress_dialog("Loading library")
        if not self.loader:
            self.init_loader()
        if not self.loader.load_remote_to_cache(self.progress_dialog,end_action = self.load_library_from_cache, download_all=download_all):
            self.loader.abord = True
            self.progress_dialog.dismiss()
        self.doc_list=[]
        self.filt_doc_list=[]

    def clear_cache(self):
        self.loader.clear_cache() 
        self.doc_list=[]
        self.filt_doc_list=[]
        self.refresh_list()
       
    def filter_doc_list(self,search):
        self.filt_doc_list = [doc for doc in self.doc_list if \
                     search.lower() in unidecode.unidecode(doc['title']).lower() \
                     or search.lower() in unidecode.unidecode(doc['author']).lower() \
                     or search.lower() in unidecode.unidecode(doc['year']).lower()]
        self.refresh_list()

    def refresh_list(self):
        self.root.ids.ml.clear_widgets()
        

#        for child in [child for child in self.root.ids.ml.children]:
#            self.root.ids.ml.remove_widget(child)
        for ind,doc in enumerate(self.filt_doc_list):
            second_line = doc['author'].replace('\n',''  )[:160]        
            third_line = doc['journal'] if 'journal' in doc.keys() else ''
            third_line += ' (%s)' % doc['year'] if 'year' in doc.keys() else ''
            new_item =  PaperListItem(file_id = ind,#id = 'doc_'+str(ind),
		                                text = clean_text(doc['title']),
                                        secondary_text = clean_text(second_line),
                                        tertiary_text = clean_text(third_line))
		                               #secondary_text = second_line +   '\n' + third_line)
            new_item.bind(on_release=lambda x: self.refresh_details(x.file_id))
            #new_item.refresh_details = self.refresh_details
            #   self.root.ids.tab_panel.current = 'details_tab'
            #self.root.ids.tab_panel.tab_manager.transition.direction = "right"#self.root.ids.tab_details.on_tab_press()
            self.root.ids.ml.add_widget(new_item)
    
    def load_library_from_cache(self):
        if not self.loader:
            self.init_loader()
        self.doc_list = self.loader.get_documents_from_cache()#get_local_folders()
        self.filt_doc_list = self.doc_list
        self.refresh_list()
        
        return 

    def open_loading_dialog(self,title=''):
#        content = BoxLayout(orientation='vertical',spacing=dp(10),padding = dp(20))
#        content = MDProgressBar(value = 0)
##        content.add_widget(progress)
##        content.bind()
#        #content.bind(texture_size=content.setter('size'))
#        self.progress_bar = MDDialog(title=title,
#                               content=content,
#                               size_hint=(.8, None),
#                               height=dp(200),
#                               auto_dismiss=True)
#        
        def stop():
            self.loader.abord = True
            self.loading_dialog.dismiss()
#
#        self.progress_bar.add_action_button("Cancel",
#                                      action=stop)
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.stop = stop
        self.loading_dialog.open()

    def open_progress_dialog(self,title=''):
#        content = BoxLayout(orientation='vertical',spacing=dp(10),padding = dp(20))
#        content = MDProgressBar(value = 0)
##        content.add_widget(progress)
##        content.bind()
#        #content.bind(texture_size=content.setter('size'))
#        self.progress_bar = MDDialog(title=title,
#                               content=content,
#                               size_hint=(.8, None),
#                               height=dp(200),
#                               auto_dismiss=True)
#        
        def stop():
            self.loader.abord = True
            self.progress_dialog.dismiss()
#
#        self.progress_bar.add_action_button("Cancel",
#                                      action=stop)
        self.progress_dialog = ProgressDialog(title=title)
        self.progress_dialog.stop = stop
        self.progress_dialog.open()
    
    def open_text_link(self,x):
        print(x)
 
      
    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False

    def on_pause(self):
        return True

    def on_start(self):
        self.post_build_init()
        self.open_settings()
        self.root.ids.tab_panel._filter_search = self.filter_doc_list
        self.load_library_from_cache()

    def on_stop(self):
        pass


#class AvatarSampleWidget(ILeftBody, Image):
#    pass


#class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
#    pass


#class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
#    pass


if __name__ == '__main__':
#    resource_add_path("/data/KivyMD/demos/papiview/data")
    Papiview().run()
