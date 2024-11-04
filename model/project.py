from sys import maxsize

class Project:

    def __init__(self, id=None, name=None, status=None, enabled=None, inherit_global=None, view_status=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.enabled = enabled
        self.inherit_global = inherit_global
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return ("%s:%s:%s:%s:%s:%s:%s" %
                (self.id, self.name, self.status, self.enabled, self.inherit_global, self.view_status, self.description))


    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            # Maxsize выдает большое целое число
            return maxsize