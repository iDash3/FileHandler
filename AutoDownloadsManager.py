# Install from pip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import os

class MyHandler(FileSystemEventHandler):
  ### Private variables
  def __init__(self, folder_src, folder_destination):
    self.folder_src = folder_src
    self.folder_destination = folder_destination
    self.image_types = ('png', 'jpg', 'jpeg')
    self.doc_types = ('pdf', 'txt', 'docx', 'doc')
    self.exe_types = ('exe', 'bat', 'config')
    self.especials = {}

  ### Methods for handling file events
  def on_created(self, event):
    if not event.is_directory:
      _, event_file = os.path.split(event.src_path)
      file_type = event_file.split('.')[1]
      file_name = event_file.split('.')[0]
      if len(file_name.split('_')) > 1:
        file_name_ = file_name.split('_')[1]
        file_content = file_name.split('_')[0]
        print(file_name_, file_content)
      else:
        pass
      self.__move_file(file_name, file_type)
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
    folder_name = 'Other shit'
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
    try:
      os.rename(file_path,new_file_path)
    except PermissionError:
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

  folder_to_track = './SRCDownloads'
  folder_to_go = './Downloads'
  event_handler = MyHandler(folder_to_track, folder_to_go)
  especial_cases = {
    'mn': ('MétodosNuméricos', r'D://'), 
    'ed': ('EcuacionesDiferenciales', r'D://'),
    'pye': ('ProbabilidadEstadística', r'D:\iDash\Documents\School\LiteralGrill\Probabilidad y Estadísitica'),
    'ec': ('Economia', r''),
    'al': ('AlgebraLineal', r''),
    'qm': ('QuimicaMateriales', r''),
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