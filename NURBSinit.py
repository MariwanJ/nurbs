# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a apart of the Open Source Nurbs Workbench - FreeCAD. *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os,sys

"""
This file will add all paths needed for the NURBS.
ICON path should be always added as bellow 
'Resources/icons/' 
"""
#Nurbs  -Nurbs
__dir__ = os.path.dirname(__file__)
NURBS_PATH=os.path.join(__dir__,'nurbs/')
DATA_PATH=os.path.join(__dir__,'Resources/Documents/testdata/')
ICONS_PATH=os.path.join(__dir__,'Resources/icons/')
IMAGES_PATH=os.path.join(__dir__,'Resources/images/')
