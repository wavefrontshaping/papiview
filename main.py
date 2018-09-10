# -*- coding: utf-8 -*-



from __future__ import print_function



from kivy.config import ConfigParser, Config
Config.set('kivy','log_dir', 'logs')
Config.set('kivy','log_name', 'kivy_%y-%m-%d_%_.txt')
Config.add_section('global')
Config.set('global','ui_style','ereader')

UI_STYLE = Config.get('global','ui_style') 
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
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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
#from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import OneLineListItem#ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
#from kivymd.snackbar import Snackbar
#from kivymd.theming import ThemeManager
#from kivymd.time_picker import MDTimePicker
from kivymd.progressbar import MDProgressBar 

#import kivymd.list

from kivy.logger import Logger, LoggerHistory



from kivy.uix.settings import SettingString, SettingItem

from kivymd.backgroundcolorbehavior import (BackgroundColorBehavior,
                                            SpecificBackgroundColorBehavior)






import unidecode
import re
import os

if UI_STYLE == 'md':
    from kivymd.theming import ThemableBehavior, ThemeManager
    from ui.main_md import MDBoxLayout, MDFloatLayout
    from ui.main_md import PapDialog, PapPopup, ProgressDialog, DetailLabel
    from ui.main_md import SETTINGS_CLS
    from paper_list import PaperListItem, ListItem
    from mdsettings import MDSettingString,MDSettingSpinner,MDSettingsWithTabbedPanel,\
                           MDSettingsWithSidebar,MDSettingPassword,MDSettingBool,\
                           MDSettingsWithSpinner,MDSettingsWithNoMenu
    
elif UI_STYLE == 'ereader':
    from ui.main_ereader import PapDialog, PapPopup, YNPopup, PaperListItem, ListItem#, ProgressDialog
    from kivy.uix.settings import SettingsWithSidebar,SettingsWithNoMenu, SettingBoolean, SettingString, SettingOptions
    from ui.main_ereader import SETTINGS_CLS, DetailLabel
    from ui.main_ereader import BWThemeManager #as ThemeManager
    from ui.main_ereader import BWSettingString,BWSettingOptions,\
                                BWSettingPassword,BWSettingBoolean


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

#class MDPopup(MDDialog):
#    pass

#class YNPopup(PapPopup):
#    def __init__(self, **kwargs):
#        super(YNPopup, self).__init__(**kwargs)
#        self.add_action_button("No",
#                                      action=lambda *x: self.on_no(x))
#        self.add_action_button("Yes",
#                                      action=lambda *x: self.on_yes(x))
#        # when width of action_area changes, it calls the setter function for self.width
#        

#        #self._action_area.bind(width= lambda x,y: self.setter('width')(x,y+self.add_width))
#        self.width=dp(400)

#        #self.ids.text.bind(width= lambda x,y: self.setter('height')(x,y))
#        #self._action_area.bind(height= lambda x,y: self.setter('height')(x+dp(800),y+dp(800)))
#    def _on_yes(self):
#        self.on(yes)
#        self.dismiss()

#    def on_yes(self):
#        pass

#    def on_no(self,*args):
#        self.dismiss()
        

class ExitPopup(PapPopup):

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


class LoadingDialog(PapDialog):
    info = StringProperty('')
    def stop(self):
        pass
    def __init__(self,**kwargs):
        super(LoadingDialog, self).__init__(**kwargs)
        self.add_action_button("Cancel", action=lambda x: self.stop())
        


        
        






class File(BoxLayout):
    filename = ' '
    def __init__(self, **kwargs):
        super(File, self).__init__(**kwargs)
#        self.filename = 'no file'
#    pass





class ProgressDialog(PapDialog):
    progress_bar = ObjectProperty()
    max_value = NumericProperty()
    progress_value = NumericProperty()
    info = StringProperty('None')
#    def stop(self):
#        pass
    def __init__(self,**kwargs):
        super(ProgressDialog, self).__init__(**kwargs)
        self.add_action_button("Cancel", action=lambda x: self.dismiss())

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
        details.append('[u]%s[/u]' % Doc('journal') if Doc('journal') else 'arxiv' if 'eprint' in document.keys() else '')
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



#class HackedDemoNavDrawer(MDNavigationDrawer):
#    # DO NOT USE
#    def add_widget(self, widget, index=0):
#        if issubclass(widget.__class__, BaseListItem):
#            self._list.add_widget(widget, index)
#            if len(self._list.children) == 1:
#                widget._active = True
#                self.active_item = widget
#            # widget.bind(on_release=lambda x: self.panel.toggle_state())
#            widget.bind(on_release=lambda x: x._set_active(True, list=self))
#        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
#            self._header_container.add_widget(widget)
#        else:
#            super(MDNavigationDrawer, self).add_widget(widget, index)
         

class Papiview(App):
    use_kivy_settings = False
    
    previous_date = ObjectProperty()
    title = "Papiview"
    settings_cls = SETTINGS_CLS
    print('--'*50)
    print(SETTINGS_CLS)
    if UI_STYLE == 'md':
        theme_cls = ThemeManager()
    elif UI_STYLE == 'ereader':
        bwtheme_cls = BWThemeManager()
        
#        settings_cls = MDSettingsWithNoMenu 
#    elif UI_STYLE == 'ereader':  
#        settings_cls = MDSettingsWithTabbedPanel
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
        self.dialog = PapDialog(title=title,
                               content=content,
                               size_hint=(.8, None),
                               height=dp(350),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()
    

        
    def build(self):
#        config = self.config
        #main_widget = Builder.load_string(main_widget_kv)
        self.ui_style = Config.get('global','ui_style')
        if UI_STYLE == 'md':
            main_widget = Builder.load_file('ui/main_md.kv')
            self.theme_cls.theme_style = 'Dark'
        elif UI_STYLE == 'ereader':
            main_widget = Builder.load_file('ui/main_ereader.kv')
            self.bwtheme_cls.style = 'Light'
#            self.theme_cls.theme_style = 'Light'
#            self.theme_cls.primary_palette = 'Grey'
#            self.theme_cls.primary_hue = '400'
#            self.theme_cls.primary_dark_hue = '900'
#            self.theme_cls.primary_light_hue = '200'
            #self.theme_cls.main_background_color = 
        #main_widget = Builder.load_file('papiview.kv')
        

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
            'connection_type': 'webdav',
            'max_dl_thread': '5',
            'max_dl_retries': '3'
        })

    def post_build_init(self, *args):
        #if platform == 'android':
            #import android
            #android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.key_handler)
        
        self.load_info()
        self.load_logs()

#        from kivy.uix.button import Button
#        for i in range(25):
#            btn = Button(text='truc %g' % i,size_hint_y=None,height=dp(60))
#            self.root.ids.test_list.add_list_element(btn)  
#        self.root.ids.test_list.update_visible_list()
    
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


    def select_screen(self,x):
        
#        print(x.name)
#        if x.name == 'settings':
#            self.root.ids.settings_screen.add_widget(settings)
#        else:
        self.root.ids.scr_mngr.current = x.name
        x.parent.parent.dismiss()        
        
    def display_settings(self,settings):
        self.root.ids.settings_screen.add_widget(settings)
        #self._app_window.add_widget(settings)
#        if settings not in self.root.ids.settings_panel.children:
            #self.root.ids.settings_panel
            #self._app_window.add_widget(settings)
#            return True
#        return False
        
        
    def build_settings(self,settings):

        if UI_STYLE == 'md':
            settings.register_type('mdstring', MDSettingString)
            settings.register_type('mdbool', MDSettingBool)
            settings.register_type('mdpassword', MDSettingPassword)
            settings.register_type('mdspinner', MDSettingSpinner)
        elif UI_STYLE == 'ereader':
            settings.register_type('mdstring', BWSettingString)
            settings.register_type('mdbool', BWSettingBoolean)
            settings.register_type('mdpassword', BWSettingPassword)
            settings.register_type('mdspinner', BWSettingOptions)

        settings.add_json_panel('Global', self.config, 'settings.json')   
        settings.add_json_panel('Webdav', self.config, 'webdav.json')     
        settings.add_json_panel('SFTP', self.config, 'sftp.json')  
        self.settings = settings
        #self.settings.md_bg_color = self.root.theme_cls.bg_dark
        settings.on_config_change = self.on_config_change
     
    
    

    def refresh_details(self,ind):
        '''
        Update the content of the detail panel with the information of the currently
        selected document.
        '''
        document = self.filt_doc_list[ind]
        folder = document.get_main_folder_name()
        
        if self.ui_style == 'md':
            self.root.ids.details_tab.on_release()
        elif self.ui_style == 'ereader':
            self.root.ids.scr_mngr.current = 'details'

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

    def go_back(self):

        if UI_STYLE == 'ereader':
            if self.root.ids.scr_mngr.current == 'library':
                ExitPopup()         
            else:
                self.root.ids.scr_mngr.current = 'library'


#    def go_back(self):
#        if self.root.ids.scr_mngr.current == 'library' and self.root.ids.tab_panel.ids.tab_manager.current == 'library':
#            ExitPopup()         
##            exit_popup.bind() 
##self._action_area.bind(width= lambda x,y: self.setter('width')(x,y+dp(100)))
#            #app.Exit()
#        elif self.root.ids.scr_mngr.current == 'library':
#            self.root.ids.lib_tab.on_tab_press()
#        else:
#            self.root.ids.scr_mngr.current = 'library'
#            
#            ## Manually set all button in the menu to not active except the first one
#            ## i.e. go back selecting the library button
#            for c in  self.root.ids.nav_drawer._list.children:
#                c._active = True if c.text == 'Library' else False  
 

    def select_settings_scr(self):
        self.root.ids.scr_mngr.current = 'settings'
       
    def save_settings(self):
        self.init_loader()

    def load_logs(self):
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
        popup.title = 'Offline download'
        popup.text = "Donwload documents for offline use?\nThis may take a while"
        def action(x):
            self.load_library(offline = True)
            Clock.schedule_once(lambda x: popup.dismiss(),1.)            
        popup.on_yes = action
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
#         def stop():
#            self.loader.abord = True
#            self.progress_dialog.dismiss()
##
##        self.progress_bar.add_action_button("Cancel",
##                                      action=stop)
#        self.progress_dialog = ProgressDialog(title=title)
#        self.progress_dialog.stop = stop
#        self.progress_dialog.open()       
#        self.open_progress_dialog("Loading library")
        progress_dialog = ProgressDialog(title='Loading library')
        progress_dialog.bind(on_dismiss=lambda x: self.loader.trigger_abord())
        progress_dialog.open()

        if not self.loader:
            self.init_loader()
#        ret = 
        Clock.schedule_once(lambda dt: self.loader.load_remote_to_cache(progress_dialog,
                                                end_action = self.load_library_from_cache,
                                                download_all=download_all,
                                                thread_count = self.config.getint('global','max_dl_thread'),
                                                max_tries = self.config.getint('global', 'max_dl_retries'))
                            )
#        if not ret:
#            self.loader.abord = True
#            self.progress_dialog.dismiss()
        self.doc_list=[]
        self.filt_doc_list=[]

    def clear_cache(self):
        self.loader.clear_cache() 
        self.doc_list=[]
        self.filt_doc_list=[]
        self.refresh_list()
       
    def filter_doc_list(self,search):
        print('++'*15)
        print(search)
        self.filt_doc_list = [doc for doc in self.doc_list if \
                     search.lower() in unidecode.unidecode(doc['title']).lower() \
                     or search.lower() in unidecode.unidecode(doc['author']).lower() \
                     or search.lower() in unidecode.unidecode(doc['year']).lower()]
        print(self.filt_doc_list)
        self.refresh_list()

    def refresh_list(self):
        
#        self.root.ids.article_list.clear_widgets()
        widget_list = self.root.ids.article_list
        if Config.get('global','ui_style') == 'md':
            widget_list.clear_widgets()
            #self.root.ids.article_list.clear_widgets()
        elif Config.get('global','ui_style') == 'ereader':   
            widget_list.clear_list()
            #self.root.ids.article_list.content.clear_widgets()
#            self.root.ids.article_list.content.clear_widgets()#, ProgressDialog
        
        
        print([x['title'] for x in self.filt_doc_list])
#        for child in [child for child in self.root.ids.ml.children]:
#            self.root.ids.ml.remove_widget(child)
        for ind,doc in enumerate(self.filt_doc_list):
            second_line = doc['author'].replace('\n',''  )[:160]        
            third_line = '[u]%s[/u]' % doc['journal'] if 'journal' in doc.keys() else ''
            third_line += ' (%s)' % doc['year'] if 'year' in doc.keys() else ''
            new_item =  PaperListItem(file_id = ind,#id = 'doc_'+str(ind),
		                                text = clean_text(doc['title']),
                                        secondary_text = clean_text(second_line),
                                        tertiary_text = clean_text(third_line))
		                               #secondary_text = second_line +   '\n' + third_line)
            new_item.bind(on_release=lambda x: self.refresh_details(x.file_id))
            print(new_item.text)
            #new_item.refresh_details = self.refresh_details
            #   self.root.ids.tab_panel.current = 'details_tab'
            #self.root.ids.tab_panel.tab_manager.transition.direction = "right"#self.root.ids.tab_details.on_tab_press()
            if Config.get('global','ui_style') == 'md':
                widget_list.add_widget(new_item)
            elif Config.get('global','ui_style') == 'ereader':
                widget_list.add_list_element(new_item)#, ProgressDialog
        Clock.schedule_once(widget_list.update_visible_list,0.5)
            #self.root.ids.ml.add_widget(new_item)
        
        print('ff'*120)
        print(widget_list.item_list)

    def load_library_from_cache(self):
        if not self.loader:
            self.init_loader()
        ## TO ADD: Wait for all the thread to stop when cancel before returning the partial list
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

#    def open_progress_dialog(self,title=''):
##        content = BoxLayout(orientation='vertical',spacing=dp(10),padding = dp(20))
##        content = MDProgressBar(value = 0)
###        content.add_widget(progress)
###        content.bind()
##        #content.bind(texture_size=content.setter('size'))
##        self.progress_bar = MDDialog(title=title,
##                               content=content,
##                               size_hint=(.8, None),
##                               height=dp(200),
##                               auto_dismiss=True)
##        
#        def stop():
#            self.loader.abord = True
#            self.progress_dialog.dismiss()
##
##        self.progress_bar.add_action_button("Cancel",
##                                      action=stop)
#        self.progress_dialog = ProgressDialog(title=title)
#        self.progress_dialog.stop = stop
#        self.progress_dialog.open()
    
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
        if UI_STYLE == 'md':
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
