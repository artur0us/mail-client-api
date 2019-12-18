#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.init.setup.main import Setup
from src.init.bootstrap.main import Bootstrap

def main():
  Setup.all()
  Bootstrap.all()

main()