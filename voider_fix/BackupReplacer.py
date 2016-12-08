import logging
from os import utime, remove, makedirs
from os.path import join
from shutil import copyfile, move

log = logging.getLogger(__name__)


class BackupReplacer:
    """Replaces backup server files with correct ones"""
    NOT_FOUND_DIR_NAME = 'NOT_FOUND'

    def __init__(self, backup_files, resources):
        self.backup_files = backup_files
        self.resources = resources
        self.delete = False
        self.move = False
        self.not_found_dir = ''

    def set_move(self, not_found_dir):
        self.move = True
        self.delete = False
        self.not_found_dir = join(not_found_dir, self.NOT_FOUND_DIR_NAME)
        makedirs(self.not_found_dir, exist_ok=True)

    def set_delete(self):
        self.delete = True
        self.move = False

    @staticmethod
    def _show_error_message(pre_message, backup_file, resource):
        error_message = pre_message + "Didn't find "
        if resource:
            error_message += 'revision '
        else:
            error_message += 'resource '
        error_message += 'for backup file: ' + backup_file.filepath + ', created: ' + backup_file.to_datetime()
        logging.warning(error_message)

    def _delete(self, backup_file, resource):
        self._show_error_message('Delete. ', backup_file, resource)
        remove(backup_file.filepath)

    def _move(self, backup_file, resource):
        self._show_error_message('Moving to NOT_FOUND. ', backup_file, resource)
        move(backup_file.filepath, self.not_found_dir)

    def _move_or_delete(self, backup_file, resource):
        if self.move:
            self._move(backup_file, resource)
        elif self.delete:
            self._delete(backup_file, resource)
        else:
            self._show_error_message('', backup_file, resource)

    def _replace(self, backup_file, resource):
        resource_filepath = resource.get_filepath(backup_file.revision)

        # Replace
        if resource_filepath:
            copyfile(resource_filepath, backup_file.filepath)

            # Restore backup time again
            utime(backup_file.filepath, (backup_file.created, backup_file.created))
        else:
            self._move_or_delete(backup_file, resource)

    def replace(self):
        for backup_file in self.backup_files:
            # Skip backup files in NOT_FOUND directory
            if self.NOT_FOUND_DIR_NAME not in backup_file.filepath:
                resource = self.resources.get_resource(backup_file.id)

                if resource:
                    self._replace(backup_file, resource)
                else:
                    self._move_or_delete(backup_file, None)
