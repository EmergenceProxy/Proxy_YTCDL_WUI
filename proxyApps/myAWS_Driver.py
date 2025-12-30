import os
import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/grand/Documents/AWS_Docs/proxyApps/')
sys.path.insert(0, 'C:/Users/grand/Documents/AWS_Docs/proxyApps/pyCode')
print(f"-----------------os path: {os.getcwd()}")
from pyCode.pageSketchBook import drawHTML

from pyCode.prxyYT_CommentDL_Web import DownloadSession