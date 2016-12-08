import logging
import re

log = logging.getLogger(__name__)


class Resource:
    """A resource"""

    REGEX_PATTERN = '([a-z0-9]*-[a-z0-9]*-[a-z0-9]*-[a-z0-9]*-[a-z0-9]*)(\w{5}/)?([0-9]*)'
    REGEX = re.compile(REGEX_PATTERN)

    def __init__(self, filepath):
        self.revisionFilepaths = {}
        id_revision = self.get_id_and_revision(filepath)
        if id_revision:
            self.id = id_revision[0]
            logging.debug('New Resource: ' + self.id)
        else:
            logging.warning("Not a resource! " + filepath)
            raise NoResourceException(filepath)

    def add_revision(self, filepath):
        id_revision = self.get_id_and_revision(filepath)
        if id_revision:
            revision = id_revision[1]
            self.revisionFilepaths[revision] = filepath
            revision_message = ''
            if revision:
                revision_message = ', rev: ' + revision
            log.debug('Resource.add_revision() - id: ' + self.id + revision_message + ', filepath: ' + filepath)

    def get_filepath(self, revision=None):
        try:
            return self.revisionFilepaths[revision]
        except KeyError:
            return None

    @staticmethod
    def get_id_and_revision(filepath):
        match = Resource.REGEX.search(filepath)
        if match:
            id = match.group(1)

            # Revision
            revision = None
            if match.group(3):
                revision = str(int(match.group(3)))

            return id, revision
        else:
            return None


class NoResourceException(Exception):
    """Not a resource"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.message = filepath + ' is not a resource!'