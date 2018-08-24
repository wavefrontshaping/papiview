from kivy.utils import platform
if platform == 'android':
    from jnius import cast
    from jnius import autoclass
import urlparse
import mimetypes
import webbrowser

class AndroidBrowser(object):
    def open(self, url, new=0, autoraise=True):
        open_url(url)
    def open_new(self, url):
        open_url(url)
    def open_new_tab(self, url):
        open_url(url)


webbrowser.register('android', AndroidBrowser, None, -1)


def open_url(url):
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    browserIntent = Intent()
    browserIntent.setAction(Intent.ACTION_VIEW)
    browserIntent.setData(Uri.parse(url))
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    currentActivity.startActivity(browserIntent)
