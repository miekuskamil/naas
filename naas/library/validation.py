#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import ipaddress
import logging

from flask import request
from werkzeug.exceptions import UnprocessableEntity, BadRequest


logger = logging.getLogger("NAAS")


class Validate(object):
    """Validators and such"""

    def __init__(self):
        self._field_name = None
        self.http = ValidateHTTP()

    @staticmethod
    def custom_port():
        # If "port" is in payload, don't do anything, otherwise set it to 22
        request.json.setdefault("port", 22)

    def is_ip_addr(self, ip, name=None):
        self._field_name = name
        self.is_not_none(ip, name)
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            self._error("invalid IP Address")

    def is_json(self):
        if not request.json:
            self._error("json required")

    def is_not_none(self, s, name=None):
        self._field_name = name
        if s is None:
            self._error("value cannot be null")

    @staticmethod
    def is_config_set():
        request.json.setdefault("config_set", False)

    def is_command_set(self):
        if not request.json["commands"]:
            self._error("please provide commands in a list")
        if not isinstance(request.json["commands"], list):
            self._error("please provide commands in a list", code=422)

    def has_credentials(self):
        if not request.json["username"] or not request.json["password"]:
            self._error("you must provide a username and password")
        if not isinstance(request.json["username"], str) or not isinstance(request.json["password"], str):
            self._error("username and password must be strings", code=422)

    def has_platform(self):
        if not request.json["platform"]:
            self._error("you must provide a netmiko platform")
        if not isinstance(request.json["platform"], str):
            self._error("platform must be a string", code=422)

    @staticmethod
    def _error(message, code=400):
        logger.error(message)
        if code == 400:
            raise BadRequest
        elif code == 422:
            raise UnprocessableEntity


class ValidateHTTP(object):
    def __init__(self):
        self.headers = {k.lower(): v for k, v in request.headers.items()}
        self.method = request.method

    @staticmethod
    def _error():
        logger.error("Invalid HTTP request")
        raise BadRequest