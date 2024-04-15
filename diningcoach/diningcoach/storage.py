import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class FileSystemOverwriteStorage(FileSystemStorage):
  def get_available_name(self, name, max_length=None):
    # self.delete(name)
    if self.exists(name):
      os.remove(os.path.join(self.location, name))
    return super().get_available_name(name, max_length)
