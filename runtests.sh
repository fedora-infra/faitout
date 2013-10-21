#!/bin/bash
PYTHONPATH=faitout ./nosetests \
--with-coverage --cover-erase --cover-package=faitout $*
