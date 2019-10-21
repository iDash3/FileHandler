# Install from pip
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
import sys
import os

class MyHandler(FileSystemEventHandler):
  def __init__(self, folder_src, folder_destination):
    self.folder_src = folder_src
    self.folder_destination = folder_destination

  def on_created(self, event):
    for filename in os.listdir(self.folder_src): 
      print(filename)
      src = self.folder_src + "/" + filename
      print(src)
      new_destination = self.folder_destination + "/" + filename
      os.rename(src, new_destination)
  
  def on_moved(self, event):
    pass
  
  def on_deleted(self, event):
    pass
  
  def on_modified(self, event):
    pass

if __name__ == '__main__':
  # Get path from line arguments
  # path = sys.argv[1] if len(sys.argv) > 1 else "."

  folder_to_track = './SRCDownloads'
  folder_dest = './Downloads'
  event_handler = MyHandler(folder_to_track, folder_dest)

  observer = Observer()
  observer.schedule(event_handler, folder_to_track, recursive=True)
  observer.start()

  try:
    while True:
      time.sleep(10)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
