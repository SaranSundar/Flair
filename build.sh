#!/bin/bash

rmdir build
rmdir dist
rm *.spec
pyinstaller -w -F -y --add-data "templates;templates" --add-data "static;static" flair.py