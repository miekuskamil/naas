#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import logging

from flask import request
from functools import wraps
from naas.library import validation


logger = logging.getLogger(name="NAAS")


def valid_payload(f):
    """
    Decorator function to check validity of a NAAS payload
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        v = validation.Validate()
        v.is_json()
        v.is_ip_addr(request.json["ip"], "ip")
        v.is_config_set()
        v.is_command_set()
        v.custom_port()
        v.has_credentials()
        v.has_platform()
        logger.info(
            "%s is issuing %s commands to %s", request.json["user"], len(request.json["commands"]), request.json["ip"]
        )
        logger.debug(
            "%s is issuing the following commands to %s: %s",
            request.json["user"],
            request.json["ip"],
            request.json["commands"],
        )
        return f(*args, **kwargs)

    return wrapper