# Install from pip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import time
import sys
import os

class MyHandler(FileSystemEventHandler):
  def __init__(self, folder_src, folder_destination):
    self.folder_src = folder_src
    self.folder_destination = folder_destination
    self.image_types = ('png', 'jpg', 'jpeg')
    self.doc_types = ('pdf', 'txt', 'docx', 'doc')
    self.exe_types = ('exe', 'bat', 'config')

  def on_created(self, event):
    if not event.is_directory:
      _, event_file = os.path.split(event.src_path)
      file_type = event_file.split('.')[1]
      file_name = event_file.split('.')[0]
      self.__move_file(file_name, file_type)
    else:
      print('Its a directory')
  
  def on_moved(self, event):
    pass
  
  def on_deleted(self, event):
    pass
  
  def on_modified(self, event):
    pass

  # Function to check for every item in types if a dir exists if not, create it
  # Add Logging
  # Dynamically change name (?)
  def __move_file(self, name, type):
    folder_name = 'Miscellaneaus'
    if(type in self.image_types):
      folder_name = 'Images'
    elif(type in self.doc_types):
      folder_name = 'Documents'
    elif(type in self.exe_types):
      folder_name = 'Executables'

    file_path = self.folder_src + '/{}.{}'.format(name, type)
    folder_path = self.folder_destination + '/' + folder_name
    new_file_path = folder_path + '/{}.{}'.format(name, type)
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    shutil.move(file_path,new_file_path)

if __name__ == '__main__':
  # Get path from line arguments
  # path = sys.argv[1] if len(sys.argv) > 1 else "."

  folder_to_track = './SRCDownloads'
  folder_to_go = './Downloads'
  event_handler = MyHandler(folder_to_track, folder_to_go)

  observer = Observer()
  observer.schedule(event_handler, folder_to_track)
  observer.start()

  try:
    while True:
      time.sleep(10)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
