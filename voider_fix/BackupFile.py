import logging
import re
from datetime import datetime
from os import path

log = logging.getLogger(__name__)


class BackupFile:
    """ The file to restore with a correct backup """

    REGEX_PATTERN = '([a-z0-9]*-[a-z0-9]*-[a-z0-9]*-[a-z0-9]*-[a-z0-9]*)_?([0-9]*)'
    REGEX = re.compile(REGEX_PATTERN)
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, filepath):
        self.filepath = filepath
        id_revision = self.get_id_and_revision(filepath)
        if id_revision:
            self.id = id_revision[0]
            self.revision = id_revision[1]
        self._set_timestamp(filepath)

        # Logging
        if self.revision:
            revision_string = ', rev: ' + self.revision
        else:
            revision_string = ''
        logging.debug('New BackupFile. timestamp: ' + str(self.created) + ', path: ' + filepath + ', id: ' + self.id +
                      revision_string)

    def _set_timestamp(self, filepath):
        self.created = path.getmtime(filepath)

    @staticmethod
    def is_resource(filepath):
        return BackupFile.REGEX.search(filepath) is not None

    @staticmethod
    def get_id_and_revision(filepath):
        basename = path.basename(filepath)
        match = BackupFile.REGEX.match(basename)
        if match:
            id = match.group(1)

            # Revision
            revision = None
            if match.group(2):
                revision = match.group(2)

            return id, revision
        else:
            return None

    def is_revision(self):
        return self.revision is not None

    def to_datetime(self):
        return datetime.fromtimestamp(self.created).strftime(self.DATETIME_FORMAT)
