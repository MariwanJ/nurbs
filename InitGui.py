# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Nurbs Workbench - App.      *
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

from PySide.QtCore import QT_TRANSLATE_NOOP
import FreeCAD 
import FreeCADGui 
import os,sys


__title__ = "NURBS Workbench - Init file"
__author__ = "Converted by Mariwan Jalal <mariwan.jalal@gmail.com>, Original other Microlley2"
__url__ = "https://www.freecadweb.org"

class NURBS_Workbench (Workbench):
    "NURBS Workbench object"
    def __init__(self):
        import NURBSinit
        self.__class__.Icon = NURBSinit.ICONS_PATH + 'WorkbenchIcon.svg'
        self.__class__.MenuText = "NURBS"
        self.__class__.ToolTip = "Converted nurbs- original NURBS code written by Microelly2"

    def Initialize(self):
        import NurbsTools as _nurb
        self.appendToolbar("Nurbs",_nurb.NurbsTools.list)
        self.appendMenu("Nurbs",_nurb.NurbsTools.list)
 
        
    def Activated(self):
        if not(FreeCAD.ActiveDocument):
            FreeCAD.newDocument()

        FreeCAD.Console.PrintMessage('NURBS workbench loaded\n')
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        pass

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
       
FreeCADGui.addWorkbench(NURBS_Workbench())
