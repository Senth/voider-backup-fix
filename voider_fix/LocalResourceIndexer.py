import logging
from os import listdir
from os.path import join, isdir, isfile

from voider_fix.LocalResources import LocalResources
from voider_fix.Resource import Resource

log = logging.getLogger(__name__)


class LocalResourceIndexer:
    """Indexes all local resources that has been downloaded by the Voider client"""
    def __init__(self, path):
        self.path = path
        self.resources = LocalResources()

    def _add_resource(self, fullpath):
        # Resource file
        id_revision = Resource.get_id_and_revision(fullpath)
        if id_revision:
            id = id_revision[0]
            resource = self.resources.get_resource(id)

            # Resource not found, create new
            if resource is None:
                resource = Resource(fullpath)
                self.resources.add_resource(resource)

            resource.add_revision(fullpath)

    def _index(self, dir):
        for filepath in listdir(dir):
            fullpath = join(dir, filepath)

            # Search recursively
            if isdir(fullpath):
                self._index(fullpath)
            # Add resource
            elif isfile(fullpath):
                self._add_resource(fullpath)

    def index(self):
        self._index(self.path)
