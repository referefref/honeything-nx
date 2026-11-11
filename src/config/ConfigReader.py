#!/usr/bin/env python
#
# ConfigReader.py
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import configparser

class ConfigReader:

    def __init__(self):
        # HONEYTHING_CONFIG (Python 3 port) overrides the default path
        self.configFile = os.environ.get("HONEYTHING_CONFIG", "/opt/honeything/config/config.ini")


    '''
    Parse config file and get stated section
    @section: One of the sections written in config file
    @option: One of the options in stated section
    @filename: Optional config filename
    @return: string
    '''

    def getConfig(self, section, option, filename=None):
        value = ""
        config = configparser.ConfigParser()

        if not filename:
            filename = self.configFile

        if os.path.isfile(filename):
            config.read(filename)
            try:
                value = config.get(section, option)
            except (configparser.NoSectionError, configparser.NoOptionError) as msg:
                print('No section or option. Error message : ' + str(msg))
        else:
            print('Invalid path for configuration file')
        return value