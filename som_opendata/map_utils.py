from flask import Response, make_response
from .errors import (
    ValidateError,
)
from consolemsg import u
from yamlns import namespace as ns

implemented = ns(
    metric=['members', 'contracts'],
    geolevel=['ccaa','state'],
    relativemetric=['population', None],
    )


def validateImplementation(data):
    for field, value in data:
        if field != 'frequency':
            if value not in implemented[field]:
                raise ValidateImplementationMap(field=field, value=value)


class ValidateImplementationMap(ValidateError):
    def __init__(self, field, value):
        self.parameter = field
        self.value = value
        self.possibleValues = implemented[field]
        super(ValidateError, self).__init__(
            u"Not implemented {} '{}' try with {}"
            .format(field, value, self.possibleValues))
