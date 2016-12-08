import logging
from os import listdir, stat
from os.path import join, isdir, isfile

from voider_fix.BackupFile import BackupFile

log = logging.getLogger(__name__)


class InvalidBackupFinder:
    """Finds backup files that have 0 in file size"""
    def __init__(self, path):
        self.path = path
        self.invalidFiles = []

    def _is_empty(self, filepath):
        return stat(filepath).st_size == 0

    def _create_backup_file(self, filepath):
        self.invalidFiles.append(BackupFile(filepath))

    def _find(self, dir):
        for filepath in listdir(dir):
            fullpath = join(dir, filepath)

            # Search recursively in the directory
            if isdir(fullpath):
                self._find(fullpath)
            # File
            elif isfile(fullpath):
                # Empty and a resource
                if self._is_empty(fullpath) and BackupFile.is_resource(fullpath):
                    self._create_backup_file(fullpath)

    def findAll(self):
        """ @return all invalid backup files"""
        self._find(self.path)
        return self.invalidFiles
