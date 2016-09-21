from subtitleDownloader import sub_downloader
import os

files_loc = '/media/oferfrid/UNTITLED'

for fn in os.listdir(files_loc):
     if fn.split('.')[-1]=='mkv':
        print fn
        try:
            sub_downloader(fn)
        except:
            print ':('
            pass

# sub_downloader(file_loc)