# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from cccomptes import app
from cccomptes.commands import manager

# class DebugConfig:
#     ASSETS_DEBUG = True

if __name__ == "__main__":
    # app.config['ASSETS_DEBUG'] = True
    manager.run()
