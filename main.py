# -*- coding: utf-8 -*-
from __future__ import print_function

from kivy.app import App
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
from kivy.config import ConfigParser
from kivy.resources import resource_add_path
from kivymd.card import MDSeparator
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform


from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton, MDRaisedButton
from kivymd.spinner import MDSpinner
#from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
#from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
#from kivymd.time_picker import MDTimePicker
from kivymd.progressbar import MDProgressBar 
import kivymd.list
import os
from kivy.logger import Logger

#from settings import Settings,SettingsWithNoMenu
from kivy.uix.settings import SettingsWithSidebar,SettingsWithNoMenu
from mdsettings import MDSettingString,MDSettingSpinner,MDSettingsWithTabbedPanel,MDSettingsWithSidebar,MDSettingPassword,MDSettingBool,MDSettingsWithSpinner,MDSettingsWithNoMenu
from kivy.uix.settings import SettingString, SettingItem

from kivymd.backgroundcolorbehavior import (BackgroundColorBehavior,
                                            SpecificBackgroundColorBehavior)
from kivymd.theming import ThemableBehavior

import unidecode
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
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
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
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'Papiview'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['eraser', lambda x: app.clear_cache()],\
                                 ['refresh', lambda x: app.load_library()],\
                                 ['download', lambda x: x]]
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
                        ScrollView:
                            do_scroll_x: False
                            MDList:
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
        height: panel._tab_display_height[panel.tab_display_mode]
        
        MDTabBar:
            id: tab_bar
            size_hint_y: None
            size_hint_x: 0.7
            height: panel._tab_display_height[panel.tab_display_mode]
            md_bg_color: panel.tab_color or panel.theme_cls.primary_color
            canvas:
                # Draw bottom border
                Color:
                    rgba: (panel.tab_border_color or panel.tab_color or panel.theme_cls.primary_dark)
                Rectangle:
                    size: (self.width,dp(2))
        MDBoxLayout:   
            size_hint_x: 0.3
            md_bg_color: panel.theme_cls.bg_dark
            TextInput:
                id: search_input
                padding: dp(15)
                on_text: root._filter_search(self.text)
                text: ''
#        MDIconButton:
#            id: search_btn
#            icon: 'magnify'
    ScreenManager:
        id: tab_manager
        current: root.current
        screens: root.tabs
        transition: sm.SlideTransition()

<PaperItem>:
    file_id: 0
    
<DetailLabel>:
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
    font_style: 'Subhead'
    theme_text_color: 'Primary'
    
<ProgressDialog>:
    size_hint: (.8, None)
    height: dp(200)
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

  

           
<MDTextInput@TextInput>
    canvas:
        Color: 
            rgb: (1,1,1)
    

#<ExitPopup>:
#    MDLabel:
#        font_style
'''



def get_info(dic,key,default = ''):
        return u'{0}'.format(clean_text(dic[key])) if key in dic.keys() else default

def clean_text(text):
    return text.replace('\n',' ').replace('\t',' ')

class ExitPopup(MDDialog):

    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Are you sure?",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Close Application",
                               content=content,
                               size_hint=(.3, None),
                               height=dp(200))

        self.dialog.add_action_button("Close me!",
                                      action=lambda *x: self.dismiss_callback())
        self.dialog.open()

    def dismiss_callback(self):
        self.dialog.dismiss()
        App.get_running_app().Exit()

#class MDSettingPassword(MDSettingString):    
    #def _create_popup(self, instance):
		#super(MDSettingPassword, self)._create_popup(instance)
		#self.textinput.password = True
    #def add_widget(self, widget, *largs):
    #    if False:
    #        pass		
        #if self.content is None:
	#	super(MDSettingString, self).add_widget(widget, *largs)
        #if False:#self.ids.textinputqq:
        #    pass
        #return self.content.add_widget(widget, *largs)
    

#class Spinner(MDSpinner):
#    def __init__(self,**kwargs):
#        super(Spinner, self).__init__(**kwargs)
     

#class SettingPassword(SettingString):
#	def _create_popup(self, instance):
#		super(SettingPassword, self)._create_popup(instance)
#		self.textinput.password = True

#	def add_widget(self, widget, *largs):
#		if self.content is None:
#			super(SettingString, self).add_widget(widget, *largs)
#		if isinstance(widget, PasswordLabel):
 #           return self.content.add_widget(widget, *largs)


class LoadingDialog(MDDialog):
    info = StringProperty('')
    def stop(self):
        pass
    def __init__(self,**kwargs):
        super(LoadingDialog, self).__init__(**kwargs)
#        self.content ='PP'
        self.add_action_button("Cancel", action=lambda x: self.stop())
        

class ProgressDialog(MDDialog):
    info = StringProperty('None')
    def stop(self):
        pass
    def __init__(self,**kwargs):
        super(ProgressDialog, self).__init__(**kwargs)
#        self.content ='PP'
        self.add_action_button("Cancel", action=lambda x: self.stop())
        
        

class DetailLabel(MDLabel):
    pass

class MDBoxLayout(ThemableBehavior,BackgroundColorBehavior,BoxLayout):
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

class ListItem(kivymd.list.OneLineListItem):
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
        print(document.keys())

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

class PaperItem(kivymd.list.ThreeLineListItem):
    def refresh_detail(self,ind):
        pass
    def on_release(self):
        self.refresh_details(self.file_id)#int(self.id.split('doc_')[1]))

class Papiview(App):
    use_kivy_settings = False
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Papiview"
    settings_cls = MDSettingsWithTabbedPanel
    #SettingsWithSidebar
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
        list
        
        
        return main_widget
    


    def build_config(self, config):
#        SettingBoolean(values=['1','2'])
        config.setdefaults('kivy', {
            'log_enable': 1,
            'log_level': 'info'
        })
        config.setdefaults('webdav', {
            'host': '',
            'username': '',
            'password': '',
            'path':"",
            'https':'0'
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
        self.bind(on_start=self.post_build_init)

        
#    def on_config_change(self, config, section, key, value):
##        if config is self.config:
#            print('>>>> %s' % key, value)

    def post_build_init(self, *args):
        print('post_build1')
        if platform == 'android':
            import android
            #android.map_key(android.KEYCODE_BACK, 1001)
            print('android is here')
        win = Window
        win.bind(on_keyboard=self.key_handler)
    
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
        print(document.keys())
        folder = document.get_main_folder_name()

        #folder = self.dir_list[ind]
        # switch to the details tab
        self.root.ids.details_tab.on_tab_press()
        # clear previous details
#        self.root.ids.details_tab.clear_widgets()
        self.root.ids.journal_details.openFile = lambda x,y: Clock.schedule_once(lambda z: self.loader.open_file(x,y),1.)
        self.root.ids.journal_details.openUrl = lambda x: Clock.schedule_once(lambda z: self.loader.open_url(x),1.)
        self.root.ids.journal_details.updateDetails(document,folder)
# 


#
    def go_back(self):
        print('go back')
        print(self.root.ids.tab_panel.ids.tab_manager.current)
        #print(self.root.ids.tab_panel.tabs)
        #print(self.root.ids.tab_panel.previous_tab)
        if self.root.ids.scr_mngr.current == 'library' and self.root.ids.tab_panel.ids.tab_manager.current == 'library':
            ExitPopup()            
            #app.Exit()
        elif self.root.ids.scr_mngr.current == 'library':
            self.root.ids.lib_tab.on_tab_press()
        else:
            self.root.ids.scr_mngr.current = 'library'
            
            ## Manually set all button in the menu to not active except the first one
            ## i.e. go back selecting the library button
            print(self.root.ids.nav_drawer._list)
            print(self.root.ids.nav_drawer._list.children)
            for c in  self.root.ids.nav_drawer._list.children:
                c._active = True if c.text == 'Library' else False  
                   
            #print(self.root.ids.nav_drawer.ids.lib_menu_btn._active)
            #self.root.ids.lib_menu_btn._active = True
            #self.root.ids.settings_menu_btn._active = True
            #self.root.ids.scr_mngr.current = 'library'
            #self.root.ids.tab_panel.current = 'library'
            

    def select_settings_scr(self):
        self.root.ids.scr_mngr.current = 'settings'
       
    def save_settings(self):
        self.init_loader()
        
        
    def init_loader(self):
        from loader import Loader
        protocol = self.config.get('global','connection_type')
        print('connection_type:')
        print(protocol)
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
        self.loader = Loader(self,protocol,options,root_dir=self.user_data_dir)
     
    def _load_library(self):
        self.init_loader()
        self.refresh_cache()    
        
        
    def load_library(self):
        Clock.schedule_once(lambda x: self._load_library(),0)
        
    def refresh_cache(self):
        
        self.open_progress_dialog("Loading library")
        if not self.loader:
            self.init_loader()
        if not self.loader.load_remote_to_cache(self.progress_dialog,end_action = self.load_library_from_cache):
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
                     or search.lower() in unidecode.unidecode(doc['author']).lower()]
        self.refresh_list()

    def refresh_list(self):
        self.root.ids.ml.clear_widgets()
        

#        for child in [child for child in self.root.ids.ml.children]:
#            self.root.ids.ml.remove_widget(child)
        print(self.filt_doc_list)
        for ind,doc in enumerate(self.filt_doc_list):
            second_line = doc['author'].replace('\n',''  )[:160]        
            third_line = doc['journal'] if 'journal' in doc.keys() else ''
            third_line += ' (%s)' % doc['year'] if 'year' in doc.keys() else ''
            new_item =  PaperItem(file_id = ind,#id = 'doc_'+str(ind),
		                               text = doc['title'].replace('\n',''  ),
		                               secondary_text = second_line +   '\n' + third_line)
            new_item.refresh_details = self.refresh_details
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

 
      
    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False

    def on_pause(self):
        return True

    def on_start(self):
        
        self.open_settings()
#        test = lambda x: print(x)
        self.root.ids.tab_panel._filter_search = self.filter_doc_list
        self.load_library_from_cache()

    def on_stop(self):
        pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
#    resource_add_path("/data/KivyMD/demos/papiview/data")
    Papiview().run()
