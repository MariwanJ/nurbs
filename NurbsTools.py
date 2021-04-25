# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Nurbs Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import NURBSinit

sys.path.append(NURBSinit.NURBS_PATH)
from nurbs import *
class NurbsTools:
    import ALLNURBS
    list = ["Nurbs_List0Group",
            "Nurbs_List1Group",
            "Nurbs_List2Group",        
            "Nurbs_List3Group",
            "Nurbs_List4Group",
            "Nurbs_List5Group",
            "Nurbs_List6Group",
            "Nurbs_List7Group",
            "Nurbs_List8Group",
            "Nurbs_List9Group",
            "Nurbs_List10Group",
            "Nurbs_List11Group",
            "Nurbs_List12Group",
            "Nurbs_List13Group",
            "Nurbs_List14Group",
            ]

    """Nurbs Part Tools Toolbar"""
    def GetResources(self):
        return{
            'Pixmap':    NURBSinit.ICONS_PATH + 'NURBS.svg',
            'MenuText': 'Nurbs Tools',
            'ToolTip':  'Nurbs Tools'
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if Gui.activeDocument():
            return True
        else:
            return False