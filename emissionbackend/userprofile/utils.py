#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# define Python user-defined exceptions
class NoServerAvailableException(Exception):
    "Raise when no server available for new user"

    def __init__(self, message="No server available"):
        self.message = message
        super().__init__(self.message)


class NoUserEmailException(Exception):
    "Raise when no usenr email is provided"

    def __init__(self, message="Email is required"):
        self.message = message
        super().__init__(self.message)
