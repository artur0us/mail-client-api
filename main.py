#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from constants import *
from setup_app import *
from http_server import *


"""
App entry point
"""


def main():
  # Setting up some parameters
  setup_all()
  # HTTP server
  run_http()

main()
