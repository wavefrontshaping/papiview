# -*- coding: utf-8 -*-

#from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.metrics import dp,sp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, ReferenceListProperty,\
                            OptionProperty, BoundedNumericProperty, StringProperty, BooleanProperty,\
                            DictProperty
from kivymd.dialog import MDDialog
from kivymd.button import MDFlatButton, BaseButton, BaseFlatButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.material_resources import DEVICE_TYPE


#MDSettingString,MDSettingSpinner,MDSettingsWithTabbedPanel,MDSettingsWithSidebar,MDSettingPassword,MDSettingBool,MDSettingsWithSpinner,MDSettingsWithNoMenu
from kivy.uix.settings import SettingItem, SettingBoolean, SettingOptions, \
                              SettingString, InterfaceWithTabbedPanel, \
                              Settings, SettingSpacer

from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.behaviors import ToggleButtonBehavior



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

class BWThemeManager(Widget):
    foreground_color = ListProperty([0,0,0,1])
    secondary_foreground_color = ListProperty([0.2,0.2,0.2,1])
    background_color = ListProperty([1,1,1,1])
    secondary_background_color = ListProperty([0.8,0.8,0.8,1])
    style = OptionProperty('Light', options=['Light', 'Dark'])

    def on_style(self, *largs):
        if self.style == 'Light':
            self.foreground_color = [0,0,0,1]
            self.secondary_foreground_color = [0.2,0.2,0.2,1]
            self.background_color = [1,1,1,1]
            secondary_background_color = [0.8,0.8,0.8,1]
        elif self.style == 'Dark':
            self.foreground_color = [1,1,1,1]
            self.secondary_foreground_color = [0.8,0.8,0.8,1]
            self.background_color = [0,0,0,1]
            secondary_background_color = [0.25,0.25,0.25,1]

    def flip_colors(self):
        self.style = 'Dark' if self.style == 'Light' else 'Light'

class BWThemableBehavior(object):
    bwtheme_cls = ObjectProperty(None)
    #opposite_colors = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        if self.bwtheme_cls is not None:
            pass
        elif hasattr(App.get_running_app(), 'bwtheme_cls'):
            self.bwtheme_cls = App.get_running_app().bwtheme_cls
        else:
            self.bwtheme_cls = BWThemeManager()
        super(BWThemableBehavior, self).__init__(**kwargs)





class BWTextInput(TextInput):
    text_border_size = dp(12)

class SearchBox(BoxLayout):
    search_field = ObjectProperty()
    def on_search(text):
        pass


class BWFloatModalView(AnchorLayout):

    auto_dismiss = BooleanProperty(True)
    attach_to = ObjectProperty(None)
    background_color = ListProperty([0, 0, 0, .7])
    _window = ObjectProperty(None, allownone=True, rebind=True)

    __events__ = ('on_pre_open', 'on_open', 'on_pre_dismiss', 'on_dismiss')

    def __init__(self, **kwargs):
        self._parent = None
        super(BWFloatModalView, self).__init__(**kwargs)

    def _search_window(self):
        # get window to attach to
        window = None
        if self.attach_to is not None:
            window = self.attach_to.get_parent_window()
            if not window:
                window = self.attach_to.get_root_window()
        if not window:
            from kivy.core.window import Window
            window = Window
        return window

    def open(self, *largs, **kwargs):
        if self._window is not None:
            Logger.warning('ModalView: you can only open once.')
            return
        # search window
        self._window = self._search_window()
        if not self._window:
            Logger.warning('ModalView: cannot open view, no window found.')
            return
        self.dispatch('on_pre_open')
        self._window.add_widget(self)
        self._window.bind(
            on_resize=self._reposition,
            on_keyboard=self._handle_keyboard)
        self.center = self._window.center
        self.fbind('center', self._reposition)
        self.fbind('size', self._reposition)
        self._reposition()
        self.dispatch('on_open')

    def _reposition(self, *largs, **kwargs):
        pass

    def dismiss(self, *largs, **kwargs):
        '''Close the view if it is open. If you really want to close the
        view, whatever the on_dismiss event returns, you can use the *force*
        argument:
        ::

            view = ModalView()
            view.dismiss(force=True)

        When the view is dismissed, it will be faded out before being
        removed from the parent. If you don't want animation, use::

            view.dismiss(animation=False)

        '''
        if self._window is None:
            return
        self.dispatch('on_pre_dismiss')
        if self.dispatch('on_dismiss') is True:
            if kwargs.get('force', False) is not True:
                return
        self._real_remove_widget()

  
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            if self.auto_dismiss:
                self.dismiss()
                return True
        super(BWFloatModalView, self).on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        super(BWFloatModalView, self).on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
        super(BWFloatModalView, self).on_touch_up(touch)
        return True

    def on__anim_alpha(self, instance, value):
        if value == 0 and self._window is not None:
            self._real_remove_widget()

    def _real_remove_widget(self):
        if self._window is None:
            return
        self._window.remove_widget(self)
        self._window.unbind(
            on_resize=self._align_center,
            on_keyboard=self._handle_keyboard)
        self._window = None

    def on_pre_open(self):
        pass

    def on_open(self):
        pass

    def on_pre_dismiss(self):
        pass

    def on_dismiss(self):
        pass

    def _handle_keyboard(self, window, key, *largs):
        if key == 27 and self.auto_dismiss:
            self.dismiss()
            return True


class SubMenu(BWThemableBehavior,BWFloatModalView):
    #color = ListProperty([1,1,1,1])
    border_size = NumericProperty(1.5)
    border_color = ListProperty()
    attach_to = ObjectProperty(allownone=True)
    _anchor_pos = ListProperty([0,0])
    _anchor_size = ListProperty([0,0])
    '''(internal) Property that will be set to the widget to which the
    drop down list is attached.'''
    action_items = ListProperty()
    content = ObjectProperty(None)
    max_height = NumericProperty()
    
    def on_action_items(self, instance, value):
            self.update_action_menu(value)
            #action_bar.clear_widgets()
    
    def update_action_menu(self, action_items):
        self.content.clear_widgets()
        new_height = 0
        new_width = 0
        for item in action_items:
            new_height += item.height
            new_width = max(0,item.width)
            self.content.add_widget(item)
        self.content.height = new_height+self.padding[1]+self.padding[3]
        self.content.width = new_width
        self.width = new_width        

    def attach(self,widget):
        self.attach_to = widget;

    def _reposition(self, *largs):
        # calculate the coordinate of the attached widget in the window
        # coordinate system
        widget = self.attach_to
        win = Window
        if not widget or not win:
            return
        wx, wy = widget.to_window(*widget.pos)
        #ww, wh = widget.to_window(*widget.size)
        wright, wtop = widget.to_window(widget.right, widget.top)



#        # set width and x
#        if self.auto_width:
#            self.width = wright - wx

        # ensure the dropdown list doesn't get out on the X axis, with a
        # preference to 0 in case the list is too wide.
        x = wx
        if x + self.width > win.width:
            x = win.width - self.width
        if x < 0:
            x = 0
        self.pos[0] = x
#        self.pos_hint['x'] = x / win.width 

        # determine if we display the menu upper or lower to the widget
#        if self.max_height is not None:
#            height = min(self.max_height, self.content.minimum_height)
#        else:
#            height = self.content.minimum_height
        height = self.content.height



        h_bottom = wy - height #space below the widget attached to
        h_top = win.height - (wtop + height) #space above the widget attached to
        if h_bottom > 0: # draw window below the widget
            self.top = wy
            self.height = height
            #self.y = wy-height
        elif h_top > 0: # draw window below the widget
            print('draw above\n'*40)
            self.y = wtop
            self.height = height



        self._anchor_pos[0] = wx
        self._anchor_pos[1] = wy
        self._anchor_size[0] = widget.width
        self._anchor_size[1] = widget.height

    def dismiss(self, *largs):
        '''Remove the dropdown widget from the window and detach it from
        the attached widget.
        '''
        Clock.schedule_once(lambda dt: self._real_dismiss(),
                            0.05)

    def _real_dismiss(self):
        if self.parent:
            self.parent.remove_widget(self)
        if self.attach_to:
            self.attach_to.unbind(pos=self._reposition, size=self._reposition)
            self.attach_to = None
        self.dispatch('on_dismiss')


#        self.draw_border()

    def open(self,**kwargs):
        
        self.attach_to.bind(pos=self._reposition, size=self._reposition)
        self._reposition()
        super(SubMenu, self).open(**kwargs)

class BWToolbar(BWThemableBehavior,BoxLayout):
    left_action_items = ListProperty()
    right_action_items = ListProperty()
    left_actions = ObjectProperty()
    right_action = ObjectProperty()
    title = StringProperty()
    #background_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(BWToolbar, self).__init__(**kwargs)
        #self.bind(specific_text_color=self.update_action_bar_text_colors)
        Clock.schedule_once(
            lambda x: self.on_left_action_items(0, self.left_action_items))
        Clock.schedule_once(
            lambda x: self.on_right_action_items(0,
                                                 self.right_action_items))

    def on_left_action_items(self, instance, value):
        self.update_action_bar(self.ids['left_actions'], value)

    def on_right_action_items(self, instance, value):
        self.update_action_bar(self.ids['right_actions'], value)

    def update_action_bar(self, action_bar, action_bar_items):
        action_bar.clear_widgets()
        new_width = 0
        id_dic = {}
        for item in action_bar_items:
            new_width += dp(48)+dp(12)
            new_btn = IconButton(icon=item[1],
                                 on_release=item[2])
            id_dic[item[0]]= new_btn           
            action_bar.add_widget(new_btn)
        action_bar.items = id_dic
        action_bar.width = new_width




    
    

class BWButtonBehavior(BWThemableBehavior,ButtonBehavior):
    #button_color_up = ListProperty([1,1,1,1])
    #button_color_down = ListProperty([0,0,0,1])
    #text_color_down = ListProperty([0,0,0,1])
    #text_color_up = ListProperty([0,0,0,1])
    _current_button_color = ListProperty([0,0,0,0])
    _current_text_color = ListProperty([0,0,0,0])
    border_color = ListProperty()
    border_size = NumericProperty(dp(1.3))



class BWBorderButton(BWButtonBehavior,AnchorLayout):#Behavior,Label):
    border = ListProperty([16, 16, 16, 16])
    text = StringProperty('')

class BWButton(BWBorderButton):
    pass

class BWToggleButton(ToggleButtonBehavior,BWButton):
    pass

class IconLabel(Label):
    icon = StringProperty()

class BWLabel(BWThemableBehavior,Label):

    font_style = OptionProperty(
        'Body', options=['Body', 'BodyBold', 'BodyItalic', 'Headline','Subhead',
                          'Title', 'BigTitle', 'Button', 'Icon'])
    # Font,  Mobile size, Desktop size (None if same as Mobile)
    _font_styles = DictProperty({'Body': ['Roboto', False, 16, None],
                                 'BodyBold': ['Roboto', True, 16, None],
                                 'BodyItalic': ['Roboto', False, 16, None],
#                                 'Caption': ['Roboto', 12, None],
                                 'Subhead': ['Roboto', True, 18, None],
                                 'Title': ['Roboto', True, 22, None],
                                 'BigTitle': ['Roboto', True, 25, None],
                                 'Headline': ['Roboto', True, 20, None],
#                                 'Display1': ['Roboto', 34, None],
#                                 'Display2': ['Roboto',  45, None],
#                                 'Display3': ['Roboto', 56, None],
#                                 'Display4': ['RobotoLight', 112, None],
                                 'Button': ['Roboto', True, 16, None],
                                 'Icon': ['fonts/materialdesignicons-webfont.ttf', False, 24, None]})


    def __init__(self, **kwargs):
        super(BWLabel, self).__init__(**kwargs)
        self.on_font_style(None, self.font_style)

    def on_font_style(self, instance, style):
        info = self._font_styles[style]
        self.font_name = info[0]
        self.bold = info[1]
        if DEVICE_TYPE == 'desktop' and info[3] is not None:
            self.font_size = sp(info[3])
        else:
            self.font_size = sp(info[2])

class DetailLabel(BWLabel):
    pass

class ScrollButtons(AnchorLayout):
    def go_up(*largs):
        pass
    def go_down(*largs):
        pass
#    on_up = ObjectProperty()
#    on_down = ObjectProperty()

class DetailSpacer(BWThemableBehavior,Widget):
    # Internal class, not documented.
    pass

class IconButton(BWButtonBehavior,IconLabel):
    border = BooleanProperty(False)
    icon_size = NumericProperty(48)



class IconMenuItem(BWButtonBehavior,BoxLayout):
    _content_size = NumericProperty(dp(40))
    icon = StringProperty()
    text = StringProperty()
    name = StringProperty()

class ButtonScrollList(FloatLayout):
    content = ObjectProperty()
    progress_bar = ObjectProperty()
    item_list = ListProperty() 
    current_item_index = NumericProperty(0)
    current_display_count = NumericProperty(0)

    def __init__(self,**kwargs):
        super(ButtonScrollList,self).__init__(**kwargs)
        self.bind(pos=self.update_visible_list, size=self.update_visible_list)

    def add_list_element(self,widget):
        self.item_list.append(widget)

    def remove_list_element(self,widget):
        self.item_list.remove(widget) 

    def add_to_visible_list(self,widget):
        self.content.add_wdiget(widget)

    def clear_list(self):
        self.item_list = []
        current_item_index = 0
        current_display_count = 0

    def on_item_list(self, *largs):
        self.update_visible_list()

    def update_visible_list(self,*largs):
        self.content.clear_widgets()
        current_height = 0
        cnt = 0
        first_item_index = self.current_item_index 
        for item in self.item_list[first_item_index:]: 
            print('+'*10)
            print(item.text)       
            if current_height + item.height > self.height:
                break
            cnt+=1
            current_height += item.height+dp(2)
            self.content.add_widget(item)
        self.current_display_count = cnt

    def go_down_in_list(self):
        if self.current_item_index < len(self.item_list)-self.current_display_count:
            self.current_item_index += self.current_display_count
            self.update_visible_list()

    def go_up_in_list(self):
        
        # already on top
        if self.current_item_index == 0:
            return
        current_height = 0
        cnt = 0
        item_list = []
        # add the element in reverse order
        for item in self.item_list[self.current_item_index-1::-1]: 
            if current_height + item.height > self.height-1:
                break
            cnt+=1
            current_height += item.height+dp(2)
            item_list.insert(0,item)
        
        # if it is not enough to fill the screen, try to go forward
        for item in self.item_list[self.current_item_index:]: 
            if current_height + item.height > self.height-1:
                break
            cnt+=1
            current_height += item.height+dp(2)
            item_list.append(item)
        self.current_display_count = cnt
        
        # now update the content
        
        self.content.clear_widgets()
        for item in item_list:
            self.content.add_widget(item)
        self.current_item_index = self.item_list.index(item_list[0])

        
        

#    def add_widget(self, widget, index=0):
#        super(MDList, self).add_widget(widget, index)
#        self.height += widget.height

#    def remove_widget(self, widget):
#        super(MDList, self).remove_widget(widget)
#        self.height -= widget.height

#class PapDialog(ModalView):
#    title = StringProperty('')
#    background_color = ListProperty([1,1,1,1])
#    border_color = ListProperty([0,0,0,1])
#    content = ObjectProperty(None)

##    md_bg_color = ListProperty([0, 0, 0, .2])

#    border_size = NumericProperty(1.3)
#    _container = ObjectProperty()
#    _action_buttons = ListProperty([])
#    _action_area = ObjectProperty()

#    def __init__(self, **kwargs):
#        super(PapDialog, self).__init__(**kwargs)
#        self.bind(_action_buttons=self._update_action_buttons)#,
##                  auto_dismiss=lambda *x: setattr(self.shadow, 'on_release',
##                                                  self.shadow.dismiss if self.auto_dismiss else None))
#        

#    def add_action_button(self, text, action=None):
#        """Add an :class:`FlatButton` to the right of the action area.

#        :param icon: Unicode character for the icon
#        :type icon: str or None
#        :param action: Function set to trigger when on_release fires
#        :type action: function or None
#        """
#        button = BWBorderButton(text=text,
#                              size_hint=(None, None),
#                              height=dp(36))
#        if action:
#            button.bind(on_release=action)
#            print('ok '*500)
#        self._action_buttons.append(button)

#    def _update_action_buttons(self, *args):
#        self._action_area.clear_widgets()
#        for btn in self._action_buttons:
#            btn.content.texture_update()
#            btn.content.width = btn.content.texture_size[0] + dp(16)
#            self._action_area.add_widget(btn)

#    def on_content(self, instance, value):
#        if self._container:
#            self._container.clear_widgets()
#            self._container.add_widget(value)

#    def on__container(self, instance, value):
#        if value is None or self.content is None:
#            return
#        self._container.clear_widgets()
#        self._container.add_widget(self.content)
class PapDialog(BWThemableBehavior,ModalView):
    title = StringProperty('')
    #background_color = ListProperty([1,1,1,1])
    border_color = ListProperty()
    content = ObjectProperty(None)

#    md_bg_color = ListProperty([0, 0, 0, .2])

    border_size = NumericProperty(1.3)
    _container = ObjectProperty()
    _action_buttons = ListProperty([])
    _action_area = ObjectProperty()

    def __init__(self, **kwargs):
        super(PapDialog, self).__init__(**kwargs)
        self.bind(_action_buttons=self._update_action_buttons)#,
#                  auto_dismiss=lambda *x: setattr(self.shadow, 'on_release',
#                                                  self.shadow.dismiss if self.auto_dismiss else None))
        

    def add_action_button(self, text, action=None):
        """Add an :class:`FlatButton` to the right of the action area.

        :param icon: Unicode character for the icon
        :type icon: str or None
        :param action: Function set to trigger when on_release fires
        :type action: function or None
        """
        button = BWBorderButton(text=text,
                              size_hint=(None, None),
                              height=dp(36))
        if action:
            button.bind(on_release=action)
        self._action_buttons.append(button)

    def _update_action_buttons(self, *args):
        self._action_area.clear_widgets()
        for btn in self._action_buttons:
            btn.content.texture_update()
            btn.content.width = btn.content.texture_size[0] + dp(16)
            self._action_area.add_widget(btn)

    def on_content(self, instance, value):
        if self._container:
            self._container.clear_widgets()
            self._container.add_widget(value)

    def on__container(self, instance, value):
        if value is None or self.content is None:
            return
        self._container.clear_widgets()
        self._container.add_widget(self.content)

class PapPopup(PapDialog):
    pass


class YNPopup(PapPopup):
    def __init__(self, **kwargs):
        super(YNPopup, self).__init__(**kwargs)
        self.add_action_button("No",
                                      action=lambda *x: self.on_no())
        self.add_action_button("Yes",
                                      action=lambda *x: self._on_yes())
        # when width of action_area changes, it calls the setter function for self.width
        

        #self._action_area.bind(width= lambda x,y: self.setter('width')(x,y+self.add_width))
        self.width=dp(400)

        #self.ids.text.bind(width= lambda x,y: self.setter('height')(x,y))
        #self._action_area.bind(height= lambda x,y: self.setter('height')(x+dp(800),y+dp(800)))
    def _on_yes(self,*args):
        self.on_yes(self)
        #print('shit '*10)
        self.dismiss()

    def on_yes(self):
        pass

    def on_no(self,*args):
        self.dismiss()


class PapToolbar(BWToolbar):
    def open_search(self):
        self.menu = SubMenu()
        self.menu.attach(self.right_actions.items['search_btn'])
        
        search_box = SearchBox()
        search_box.width = dp(300)


        search_box.on_search = lambda x: App.get_running_app().filter_doc_list(x)
        #search_box.ids.search_field.bind(text = lambda *x: App.get_running_app().filter_doc_list(search_box.input.text))
        #self.menu.width = dp(300)
        #self.menu.bind(width=lambda x,y: search_box.setter('width')(x,y))
        self.menu.action_items = [ search_box]
        
        

        self.menu.open()
        search_box.search_field.focus = True

    def open_menu(self):
        self.menu = SubMenu(padding = [0,0,0,dp(4)])
        self.menu.attach(self.left_actions.items['menu_btn'])
        lib_item = IconMenuItem(text= 'Library', name= 'library', icon= 'library-books')
        lib_item.bind(on_release=lambda x: App.get_running_app().select_screen(x))
        settings_item = IconMenuItem(text= 'Settings', name= 'settings', icon= 'settings')
        settings_item.bind(on_release=lambda x: App.get_running_app().select_screen(x))
        info_item = IconMenuItem(text= 'Information', name= 'information', icon= 'help-circle-outline')
        info_item.bind(on_release=lambda x: App.get_running_app().select_screen(x))        
        log_item = IconMenuItem(text= 'Logs', name= 'logs', icon= 'code-brackets')
        log_item.bind(on_release=lambda x: App.get_running_app().select_screen(x))

        self.menu.action_items = [
            lib_item,
            settings_item,
            info_item,
            log_item]
        #self.menu.width = dp(300)

        self.menu.open()

class ListItem(BWButtonBehavior, BWThemableBehavior, FloatLayout):
    text = StringProperty() 
    divider = OptionProperty('Full', options=['Full', 'Inset', None], allownone=True)
    divide_color = ListProperty([0,0,0,1])
    _txt_left_pad = NumericProperty(dp(16))
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))
    _txt_right_pad = NumericProperty(dp(16))#NumericProperty(m_res.HORIZ_MARGINS)
    _num_lines = 1

    def refresh_detail(self,ind):
        pass
    def on_release(self):
        pass

    def __init__(self, **kwargs):
        super(ListItem, self).__init__(**kwargs)
        self.height = dp(48)   

class PaperListItem(BWButtonBehavior, BWThemableBehavior, FloatLayout):
    
    file_id = NumericProperty(0)

    text = StringProperty()  
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
#    text_color = ListProperty(None)
#    secondary_text_color = ListProperty(None)
#    tertiary_text_color = ListProperty(None)   
    divider = OptionProperty('Full', options=['Full', 'Inset', None], allownone=True)
    divide_color = ListProperty([0,0,0,1])
    _txt_left_pad = NumericProperty(dp(16))
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))
    _txt_right_pad = NumericProperty(dp(16))#NumericProperty(m_res.HORIZ_MARGINS)
    _num_lines = 3

    def __init__(self, **kwargs):
        super(PaperListItem, self).__init__(**kwargs)
        self.height = dp(88)        

#################################
########## SETTINGS #############
#################################

#class ToggleButton(BWBorderButton):
#    pass

class BWSettingSpacer(BWThemableBehavior,SettingSpacer):
    pass

class BWSettingItem(BWThemableBehavior,SettingItem):
    pass



#class BWSettingString(BWThemableBehavior,SettingString):
#    pass



class BWSettingOptions(BWSettingItem):
    options = ListProperty([])
    popup = ObjectProperty(None, allownone=True)

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _set_option(self, instance):
        self.value = instance.text
        self.popup.dismiss()

    def _create_popup(self, instance):
        # create the popup
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = popup = PapDialog(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '400dp'))
        popup.height = len(self.options) * dp(55) + dp(150)
        popup.ids.title_label.font_style = 'Title'
        # add all the options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = BWToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        #content.add_widget(SettingSpacer())
        #btn = BWBorderButton(text='Cancel', size_hint_y=None, height=dp(50))
        #btn.bind(on_release=popup.dismiss)
        #content.add_widget(btn)
        popup.add_action_button("Cancel", popup.dismiss)

        # and open the popup !
        popup.open()

class BWSettingBoolean(BWSettingItem):
    values = ListProperty(['0', '1'])


class BWSettingString(BWSettingItem):
    password = BooleanProperty(False)
    popup = ObjectProperty(None, allownone=True)
    textinput = ObjectProperty(None)

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, *largs):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def _create_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        popup = PapDialog(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))
        self.popup = popup
        popup.ids.title_label.font_style = 'Title'

        # Description label
        desc_label = BWLabel(text=self.desc, pos_hint = {'x': 0, 'y': 0},size_hint=[None,None], font_style='Body', height=dp(36),halign = 'left')
        desc_label.bind(texture_size= lambda x,y: desc_label.setter('width')(x,y[0]))

        # create the textinput used for numeric input
        self.textinput = textinput = BWTextInput(
            password = self.password,
            text=self.value, pos_hint = {'x': 0, 'y': 0}, font_size = '18dp', multiline=False,
            size_hint_y=None, height='42sp')
        textinput.bind(on_text_validate=self._validate)
        self.textinput = textinput

        
        #self._action_area.bind(width= lambda x,y: self.setter('width')(x,y
        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(desc_label)
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        #content.add_widget(BWSettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        popup.add_action_button("Cancel",
                                      action=lambda *x: self._dismiss())
        popup.add_action_button("Ok",
                                      action=lambda *x: self._validate())
#        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
#        btn = BWButton(text='Ok')
#        btn.bind(on_release=self._validate)
#        btnlayout.add_widget(btn)
#        btn = BWButton(text='Cancel')
#        btn.bind(on_release=self._dismiss)
#        btnlayout.add_widget(btn)
#        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

class BWSettingPassword(BWSettingString):

    def __init__(self,*kargs,**kwargs):
        super(BWSettingPassword,self).__init__(*kargs,**kwargs)
        self.password = True





class BWTabbedPanelHeader(BWToggleButton):
    content = ObjectProperty(None, allownone=True)
    # only allow selecting the tab if not already selected
    def on_touch_down(self, touch):
        if self.state == 'down':
            # dispatch to children, not to self
            for child in self.children:
                child.dispatch('on_touch_down', touch)
            return
        else:
            super(BWTabbedPanelHeader, self).on_touch_down(touch)

    def on_release(self, *largs):
        # Tabbed panel header is a child of tab_strib which has a
        # `tabbed_panel` property
        if self.parent:
            self.parent.tabbed_panel.switch_to(self)
        else:
            # tab removed before we could switch to it. Switch back to
            # previous tab
            self.panel.switch_to(self.panel.current_tab)

class ToggleButton(ToggleButtonBehavior,BWBorderButton):
    pass

class BWInterfaceWithTabbedPanel(BWThemableBehavior,FloatLayout):
    tabbedpanel = ObjectProperty()
    close_button = ObjectProperty()

    __events__ = ('on_close', )

    def add_panel(self, panel, name, uid):
        scrollview = ScrollView()
        scrollview.add_widget(panel)
        if not self.tabbedpanel.default_tab_content:
            self.tabbedpanel.default_tab_text = name
            self.tabbedpanel.default_tab_content = scrollview
        else:
            panelitem = TabbedPanelHeader(pos_hint = {'x': 0, 'y': 0}, text=name,
                                          #background_color = self.bwtheme_cls.background_color,
                                          content=scrollview)
            self.tabbedpanel.add_widget(panelitem)

    def on_close(self, *args):
        pass

class BWSettingsWithTabbedPanel(Settings):
    __events__ = ('on_close', )

    def __init__(self, *args, **kwargs):
        self.interface_cls = BWInterfaceWithTabbedPanel
        super(BWSettingsWithTabbedPanel, self).__init__(*args, **kwargs)

    def on_close(self, *args):
        pass

SETTINGS_CLS = BWSettingsWithTabbedPanel


