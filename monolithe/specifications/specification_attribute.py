# -*- coding: utf-8 -*-

import json
import pkgutil

from copy import deepcopy

from monolithe.lib import SDKUtils


class SpecificationAttribute(object):
    """ Define an attribute of an object

    """
    def __init__(self, specification, data=None):
        """ Define an attribute

            Example:
                remote_name: associatedGatewayID
                local_name: associated_gateway_id
                remote_type: String
                local_type: str
        """
        self.__default_attribute__ = None

        self.specification = specification

        # Main attributes
        self.description = None
        self.remote_name = None
        self.local_name = None
        self.remote_type = None
        self.local_type = None
        self.has_time_attribute = False

        # Other attributes
        self.allowed_chars = None
        self.allowed_choices = None
        self.autogenerated = False
        self.availability = None
        self.creation_only = False
        self.default_order = False
        self.default_value = None
        self.filterable = None
        self.format = None
        self.max_length = None
        self.max_value = None
        self.min_length = None
        self.min_value = None
        self.orderable = False
        self.readonly = False
        self.required = False
        self.unique = False

        # Specific attributes
        self.ignored = False

        # Load information from data
        if data:
            self.from_dict(data)

    def from_dict(self, data):
        """

        """
        self.remote_name = data['name']

        self.local_name = SDKUtils.get_python_name(self.specification.monolithe_config.map_attribute(self.specification.remote_name, self.remote_name))

        self.allowed_chars = data['allowedChars']
        self.allowed_choices = data['allowedChoices']
        self.autogenerated = data['autogenerated']
        self.channel = data['channel']
        self.creation_only = data['creationOnly']
        self.default_order = data['defaultOrder']
        self.description = data['description']
        self.exposed = data['exposed']
        self.filterable = data['filterable']
        self.format = data['format']
        self.max_length = data['maxLength']
        self.max_value = data['maxValue']
        self.min_length = data['minLength']
        self.min_value = data['minValue']
        self.orderable = data['orderable']
        self.read_only = data['readOnly']
        self.required = data['required']
        self.transient = data['transient']
        self.type = data['type']
        self.unique = data['unique']

        self.local_type = SDKUtils.get_python_type_name(type_name=self.type)

        if self.local_type == 'time':
            self.has_time_attribute = True

        if not self.local_type:
            # Simply ignore attributes otherwise...
            # CS 02/06/2015
            # Ignoring attribute enterprise of object InfrastructurePortProfile
            # Ignoring attribute gateway of object InfrastructureGatewayProfile
            # Ignoring attribute enterprise of object InfrastructureGatewayProfile
            self.ignored = True
            # Printer.log("Deliberately ignoring attribute %s because of type %s" % (self.remote_name, self.type))

    def to_dict(self):
        """ Transform an attribute to a dict
        """

        if self.__default_attribute__ is None:
            default_data = pkgutil.get_data(__package__, '/data/default_attribute.json')
            self.__default_attribute__ = json.loads(default_data)

        data = deepcopy(self.__default_attribute__)

        data['allowedChars'] = self.allowed_chars
        data['allowedChoices'] = self.allowed_choices
        data['autogenerated'] = self.autogenerated
        data['channel'] = self.channel
        data['creationOnly'] = self.creation_only
        data['defaultOrder'] = self.default_order
        data['description'] = self.description
        data['exposed'] = self.exposed
        data['filterable'] = self.filterable
        data['format'] = self.format
        data['maxLength'] = self.max_length
        data['maxValue'] = self.max_value
        data['minLength'] = self.min_length
        data['minValue'] = self.min_value
        data['name'] = self.remote_name
        data['orderable'] = self.orderable
        data['readOnly'] = self.read_only
        data['required'] = self.required
        data['transient'] = self.transient
        data['type'] = self.type
        data['unique'] = self.unique

        return data
