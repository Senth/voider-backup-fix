class LocalResources:
    """Register for all local files"""
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource):
        self.resources[resource.id] = resource

    def get_resource(self, id):
        """@return resource, or None if not found"""
        try:
            return self.resources[id]
        except KeyError:
            return None