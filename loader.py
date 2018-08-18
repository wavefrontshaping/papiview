import easywebdav
#from paramiko import SSHClient,AutoAddPolicy
from papis_utils import Document
import os,sys,shutil
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

#from kivymd.progressbar import MDProgressBar 
#from kivymd.dialog import MDDialog
#from kivy.metrics import dp

#if not sys.platform.startswith('linux'):
if platform == 'android':
    from jnius import cast
    from jnius import autoclass
import urlparse
import mimetypes
import webbrowser
import paramiko


connection_types = ['webdav','sftp']


class AndroidBrowser(object):
    def open(self, url, new=0, autoraise=True):
        open_url(url)
    def open_new(self, url):
        open_url(url)
    def open_new_tab(self, url):
        open_url(url)


webbrowser.register('android', AndroidBrowser, None, -1)



#options = {
# 'webdav_hostname': "https://ownpof.duckdns.org",
# 'webdav_login':    "sebastien",
# 'webdav_password': "",
# 'root': "/remote.php/webdav/Biblio/papers"
#}



class CopyFoldersIter():
    def __init__(self,folders,local_folder,client):
        self.client = client
        self.local_folder = local_folder
        self.folders_iter = folders.__iter__()
        self.count = 0
        self.busy = None
#        self.current_folder = folders[0]
    
    def __next__(self):
        self.count+=1
        current_folder = self.folders_iter.next()
        yaml_path = os.path.join(current_folder,"info.yaml")
        if not os.path.exists(os.path.join(self.local_folder,current_folder)):
            os.makedirs(os.path.join(self.local_folder,current_folder))
        local_yaml_path = os.path.join(self.local_folder,current_folder,"info.yaml")
        print yaml_path
        try:
            self.client.download(yaml_path,local_yaml_path)
            Logger.info('LOADER: Successfully retrieved %s.' % yaml_path)
        except Exception,e:
            Logger.exception('Connection error with message: %s.' % str(e))
    
class Client(object):
    def __init__(self,parent):
        self.parent_app = parent
        self.options = None
        self.protocol = None
        self.client = None
        self._ls = None
        self._ls_dir = None


    def ls_dir(self,path):
        if self.client is not None and self._ls_dir is not None:
            Logger.info('LOADER: Listing directories in %s' % path)
            try:
                list_dir = self._ls_dir(path)
                Logger.info('LOADER: Directory list: %s.' % ' '.join([s for s in list_dir]))
                return list_dir
            except Exception,e:
                Logger.exception('Connection error with message: %s.' % str(e))
            self.parent_app.show_error_dialog(
                    title = 'Error retrieving directory list.',
                    message = 'Please check your connection and your credentials.\n\nError message: %s' % e
            )
            return None
        return None

    def ls(self,path):
        if self.client is not None and self._ls is not None:
            Logger.info('LOADER: Listing directory %s' % path)
            try:
                list_ = self._ls(path)
                Logger.info('LOADER: Directory list: %s.' % ' '.join([s for s in list_]))
                return list_
            except Exception,e:
                Logger.exception('Connection error with message: %s.' % str(e))
            self.parent_app.show_error_dialog(
                    title = 'Error retrieving file list.',
                    message = 'Please check your connection and your credentials.\n\nError message: %s' % e
            )
            return None
        return None

    def download(self,remote_path,local_path):
        pass

    def open_error_dialog(self,error = ''):
        Logger.exception('Connection error with message: %s.' % str(error))
        message_err = '\n\nError with %s protocol: %s' % (self.protocol,error) if error else ''
        self.parent_app.show_error_dialog(
                    title = 'Connection error',
                    message = 'Please check your connection and your credentials.%s' % message_err
            )


class SFTP_client(Client):
    def __init__(self,*args, **kwargs):
        super(SFTP_client, self).__init__(*args, **kwargs)  
        self.transport = None
        self.protocol = 'sftp'

    def connect(self, options = None):
        
        if options == None:
            options = self.options
        else:
            self.options = options
        try:
            
            self.transport = paramiko.Transport((options['host'], 22))
            self.transport.connect(username = options['username'], password = options['password'])
            self.client = paramiko.SFTPClient.from_transport(self.transport)
            self.client.chdir(options['path'])
            print('aaaa'*5)
            print(self.client.listdir())
        except Exception,e:
            self.disconnect()
            self.open_error_dialog(error = e)
        self._ls = lambda x: self.client.listdir(x)
        self._ls_dir = lambda x: [s for s in self.client.listdir(x) if 'd' in str(self.client.lstat(s)).split()[0]]

    def disconnect(self):
        try:
            self.transport.close()
            self.client.close()
        except Exception,e:
            self.disconnect()
            self.open_error_dialog(error = e)
        self.transport = None
        self.client = None
        
    def download(self,remote_path,local_path):
        try:
            self.client.get(remote_path, localpath=local_path)
        except Exception,e:
            self.disconnect()
            self.open_error_dialog(error = e)


class Webdav_client(Client):
    def __init__(self,*args, **kwargs):
        super(Webdav_client, self).__init__(*args, **kwargs)  
        self.transport = None
        self.protocol = 'webdav'

    def connect(self,options = None):
        print('go webdav')
        print(options)
        if options == None:
            options = self.options
        else:
            self.options = options
        try:
            self.client = easywebdav.connect(**self.options)     
            print self.client.ls()
        except Exception,e:
            self.disconnect()
            self.open_error_dialog(error = e)
        self._ls = lambda x: self.client.ls(x)
        self._ls_dir = lambda x: [os.path.basename(os.path.dirname(f[0])) for f in self.client.ls(x)[1:] if f[0].endswith('/')] 

    def download(self,remote_path,local_path):
        try:
            self.client.download(remote_path,local_path)    
        except Exception,e:
            self.disconnect()
            self.open_error_dialog(error = e)  

    def disconnect(self):
        self.client = None

class Loader():
    def __init__(self,parent_app,root_dir):
        self.parent_app = parent_app
        self.client = None
        self.abord = False
        self.protocol = None
        self.cache_folder = os.path.join(root_dir, 'cache')
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder) 
        #self.client = easywebdav.connect(**webdav_options)
        #print self.client

#        self.libraries = self.get_folders(library="./")
        
    def connect(self,protocol,options):
        self.protocol = protocol
        Logger.info('LOADER: Trying to connect to %s using %s.' % ( options['host'],protocol))
        if self.client is not None:
            self.client.disconnect()
        if protocol == 'webdav':
            self.client = Webdav_client(self.parent_app)
        elif protocol == 'sftp':
            self.client = SFTP_client(self.parent_app)
        self.client.connect(options)   
        

        #print('cache folder: %s'% self.cache_folder)
        
        
    def get_libraries(self):
        return self.get_folders("./")

    def get_local_folders(self,library="./"):
        list_dir = os.listdir(os.path.join(self.cache_folder,library))
        return map(lambda x: os.path.join(self.cache_folder,x),list_dir)
#        list_ = self.client.ls(library)
#        self.folders = [os.path.basename(os.path.dirname(f[0])) for f in list_[1:] if f[0].endswith('/')]
#        return self.folders  

    def open_url(self,url):
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        browserIntent = Intent()
        browserIntent.setAction(Intent.ACTION_VIEW)
        browserIntent.setData(Uri.parse(url))
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(browserIntent)

#    def open_url(self,url):
#        print('opening url: %s' % url)
#        webbrowser.open(url)   
        
    def open_file(self,paper_dir,file_name,library="./"):
        # first check if it already exist in local files
        local_file_path = os.path.join(self.cache_folder,paper_dir,file_name)
        if os.path.isfile(local_file_path):
            Logger.debug("File %s already here." % local_file_path)
        else:
            Logger.debug("File %s not in the local folder, downloading it." % local_file_path)
            remote_file_path = os.path.join(paper_dir,file_name)
#            try:
            self.parent_app.open_loading_dialog("Downloading file")
            self.client.download(remote_file_path,local_file_path)
#            except:
#                self.parent_app.show_error_dialog(
#                       title = 'Connection error',
#                       message = 'Impossible to download the file. Please check your connection.'
#                )
#                return
            
        #if sys.platform.startswith('linux'):
        #    pass
        #else:
        Logger.debug("Opening file %s" % local_file_path)
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        mimetype = mimetypes.guess_type(local_file_path)[0]
        file_uri = urlparse.urljoin('file://', local_file_path)
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setDataAndType(Uri.parse(file_uri), mimetype)
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)

    def get_remote_folders(self,library="./"):
        self.busy = True
        #try:
        list_ = self.client.ls_dir(library)      
        if list_ is None:
            return None

        self.folders = list_
        print(self.folders)
        self.busy = False
        return self.folders
    
   
        
    def load_remote_to_cache(self,dialog,library="./",end_action = lambda: None):
#        import yaml
        self.busy = True
        folders = self.get_remote_folders(library)
        if folders is None:
            return 
        dialog.ids.progress_bar.max = len(folders)
        local_folder = self.cache_folder
      
        iter_copy = CopyFoldersIter(folders,local_folder,self.client)
         
        def clock_func(dt):
            iter_copy.__next__()
            dialog.ids.progress_bar.value = iter_copy.count
            dialog.info = 'Folder %g/%g: %s' % (iter_copy.count,len(folders),folders[iter_copy.count])
            if dialog.ids.progress_bar.value == dialog.ids.progress_bar.max or self.abord == True:
                self.busy = False
                self.abord = False
                Clock.unschedule(clock_func)
                dialog.dismiss()
                end_action()
            
        Clock.schedule_interval(clock_func,1/60.)
        
        return True
    
    def get_documents_from_cache(self,library= './'):
        self.busy= True
        folder_list = self.get_local_folders()
        self.busy = False
        print('folder_list')
        
        print(folder_list)
        if folder_list is not None:
            return map(Document,folder_list)#,[os.path.basename(folder) for folder in folder_list]
    
    def clear_cache(self):
        folder_list = self.get_local_folders('./')
        for folder in folder_list:
            path = os.path.join(self.cache_folder,folder)
            if os.path.isdir(path):
                shutil.rmtree(path)
        
#class Webdav_loader(Loader):
#    def __init__(self,**kwargs):
#        super(Webdav_loader, self).__init__(**kwargs)        
        
        
        
