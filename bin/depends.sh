#!/usr/bin/bash
# situation (c) Ian Dennis Miller

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -a . -r requirements-dev.txt situation
source ~/.virtualenvs/situation/bin/activate
