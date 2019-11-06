# Install from pip
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path, PureWindowsPath
import time
import sys
import os

class MyHandler(FileSystemEventHandler):
  ### Private variables
  def __init__(self, folder_src, folder_destination):
    self.folder_src = Path(folder_src)
    self.folder_destination = Path(folder_destination)
    self.image_types = ('png', 'jpg', 'jpeg')
    self.doc_types = ('pdf', 'txt', 'docx', 'doc')
    self.exe_types = ('exe', 'bat', 'config')
    self.especials = {}

  ### Methods for handling file events
  def on_created(self, event):
    if not event.is_directory:
      event_file = Path(event.src_path)
      event_file_suffix = event_file.suffix
      event_file_name = event_file.stem

      if len(event_file_name.split('_')) > 1:
        file_content = event_file_name.split('_')[0]
        file_name = event_file_name.split('_')[1]
        print(file_name, file_content)
        self.__move_special(file_content, file_name)
      else:
        self.__move_file(event_file_name, event_file_suffix)
    else:
      # Its a directory
      pass
  
  def on_moved(self, event):
    pass
  
  def on_deleted(self, event):
    pass
  
  def on_modified(self, event):
    pass

  ### Methods for files
  ## Moves files to dir
  # Add Logging (?)
  # Dynamically change name (?)
  def __move_file(self, name, type):
    complete_file_name =  name + type
    type = type.split('.')[1]
    folder_name = 'Other shit'
    if(type in self.image_types):
      folder_name = 'Images'
    elif(type in self.doc_types):
      folder_name = 'Documents'
    elif(type in self.exe_types):
      folder_name = 'Executables'

    file_path = self.folder_src / complete_file_name 
    folder_path = self.folder_destination / folder_name 
    new_file_path = folder_path / complete_file_name
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    try:
      os.rename(file_path,new_file_path)
    except PermissionError:
      print("PERMISSION ERROR")
    except FileNotFoundError:
      print("FILENOTFOUND")
    except FileExistsError:
      print("FILEEXIST")
  
  def __move_special(self, content, name):
    pass

  ### To add new especial cases, insert a dictonary of couples
  ## example = {id: (name, path)}
  def add_especial(self, es_id, es_name, es_path):
    self.especials[es_id] = (es_name, es_path)
  def add_especials(self, new_especials):
    self.especials.update(new_especials)


if __name__ == '__main__':
  # Get path from line arguments
  # path = sys.argv[1] if len(sys.argv) > 1 else "."

  ## Check for compatibility on Linux and Mac
  folder_to_track = './SRCDownloads'
  folder_to_go = './Downloads'
  event_handler = MyHandler(folder_to_track, folder_to_go)

  especial_cases = {
    'mn': ('MétodosNuméricos', PureWindowsPath('')), 
    'ed': ('EcuacionesDiferenciales', PureWindowsPath('')),
    'pye': ('ProbabilidadEs', PureWindowsPath('')),
    'ec': ('Economia', PureWindowsPath('')),
    'al': ('AlgebraLineal', PureWindowsPath('')),
    'qm': ('QuimicaMateriales', PureWindowsPath('')),
  }

  observer = Observer()
  observer.schedule(event_handler, folder_to_track)
  observer.start()

  try:
    while True:
      time.sleep(10)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()