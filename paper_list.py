from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, \
    ListProperty, OptionProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.gridlayout import GridLayout
import kivymd.material_resources as m_res
from kivymd.ripplebehavior import RectangularRippleBehavior
from kivymd.theming import ThemableBehavior


from kivymd.list import MDList

Builder.load_string('''
#:import m_res kivymd.material_resources

<PaperListItem>
    size_hint_y: None
    canvas:
        Color:
            rgba: self.theme_cls.divider_color if root.divider is not None else (0, 0, 0, 0)
        Line:
            points: (root.x ,root.y, root.x+self.width, root.y)\
                    if root.divider == 'Full' else\
                    (root.x+root._txt_left_pad, root.y,\
                    root.x+self.width-root._txt_left_pad-root._txt_right_pad,\
                    root.y)
    BoxLayout:
        id: _text_container
        orientation: 'vertical'
        pos: root.pos
        padding: root._txt_left_pad, root._txt_top_pad, root._txt_right_pad, root._txt_bot_pad
        MDLabel:
            id: _lbl_primary
            text: root.text
            font_style: root.font_style
            theme_text_color: root.theme_text_color
            text_color: root.text_color
            size_hint_y: None
            height: self.texture_size[1]
            shorten: True
            shorten_from: 'right'
            strip: True
        MDLabel:
            id: _lbl_secondary
            text: root.secondary_text
            font_style: root.secondary_font_style
            theme_text_color: root.secondary_theme_text_color
            text_color: root.secondary_text_color
            size_hint_y: None
            height: self.texture_size[1]
            shorten: True
            shorten_from: 'right'
            strip: True
        MDLabel:
            id: _lbl_tertiary
            text: root.tertiary_text
            font_style: root.tertiary_font_style
            theme_text_color: root.tertiary_theme_text_color
            text_color: root.tertiary_text_color
            size_hint_y: None
            height: self.texture_size[1]
            shorten: True 
            shorten_from: 'right'
            strip: True
''')

class PaperListItem(ThemableBehavior, RectangularRippleBehavior,
                   ButtonBehavior, FloatLayout):
    
    file_id = NumericProperty(0)

    text = StringProperty()
    '''Text shown in the first line.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults
    to "".
    '''
    
    text_color = ListProperty(None)
    ''' Text color used if theme_text_color is set to 'Custom' '''

    font_style = OptionProperty(
        'Subhead', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
                            'Headline', 'Display1', 'Display2', 'Display3',
                            'Display4', 'Button', 'Icon'])
    
    theme_text_color = StringProperty('Primary',allownone=True)
    ''' Theme text color for primary text '''

    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    '''Text shown in the second and potentially third line.

    The text will wrap into the third line if the ListItem's type is set to
    \'one-line\'. It can be forced into the third line by adding a \\n
    escape sequence.

    :attr:`secondary_text` is a :class:`~kivy.properties.StringProperty` and
    defaults to "".
    '''
    
    secondary_text_color = ListProperty(None)
    tertiary_text_color = ListProperty(None)
    ''' Text color used for secondary text if secondary_theme_text_color 
    is set to 'Custom' '''
    
    secondary_theme_text_color = StringProperty('Secondary',allownone=True)
    tertiary_theme_text_color = StringProperty('Secondary',allownone=True)
    ''' Theme text color for secondary primary text '''
    
    secondary_font_style = OptionProperty(
        'Body1', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
                          'Headline', 'Display1', 'Display2', 'Display3',
                          'Display4', 'Button', 'Icon'])

    tertiary_font_style = OptionProperty(
        'Body1', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
                          'Headline', 'Display1', 'Display2', 'Display3',
                          'Display4', 'Button', 'Icon'])

    divider = OptionProperty('Full', options=['Full', 'Inset', None], allownone=True)

    _txt_left_pad = NumericProperty(dp(16))
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))
    _txt_right_pad = NumericProperty(m_res.HORIZ_MARGINS)
    _num_lines = 3

    def __init__(self, **kwargs):
        super(PaperListItem, self).__init__(**kwargs)
        self.height = dp(88)
