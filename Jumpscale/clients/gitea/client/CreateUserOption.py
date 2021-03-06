# DO NOT EDIT THIS FILE. This file will be overwritten when re-running go-raml.

"""
Auto-generated class for CreateUserOption
"""
from six import string_types

from . import client_support




class CreateUserOption(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(**kwargs):
        """
        :type email: string_types
        :type full_name: string_types
        :type login_name: string_types
        :type password: string_types
        :type send_notify: bool
        :type source_id: int
        :type username: string_types
        :rtype: CreateUserOption
        """

        return CreateUserOption(**kwargs)

    def __init__(self, json=None, **kwargs):
        pass
        if json is None and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'CreateUserOption'
        data = json or kwargs

        # set attributes
        data_types = [string_types]
        self.email = client_support.set_property('email', data, data_types, False, [], False, True, class_name)
        data_types = [string_types]
        self.full_name = client_support.set_property('full_name', data, data_types, False, [], False, False, class_name)
        data_types = [string_types]
        self.login_name = client_support.set_property(
            'login_name', data, data_types, False, [], False, False, class_name)
        data_types = [string_types]
        self.password = client_support.set_property('password', data, data_types, False, [], False, True, class_name)
        data_types = [bool]
        self.send_notify = client_support.set_property(
            'send_notify', data, data_types, False, [], False, False, class_name)
        data_types = [int]
        self.source_id = client_support.set_property('source_id', data, data_types, False, [], False, False, class_name)
        data_types = [string_types]
        self.username = client_support.set_property('username', data, data_types, False, [], False, True, class_name)

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
