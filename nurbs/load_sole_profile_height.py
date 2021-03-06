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


'''
load height and length information for a sole from a sketcher file
filename is 'User parameter:Plugins/shoe').GetString("height profile")
the skeche contains exactly one bspline curve
'''


# \cond
import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit



import os
import sys

import spreadsheet_lib
#reload (spreadsheet_lib)
from spreadsheet_lib import ssa2npa, npa2ssa, cellname

# \endcond
# from .errors import show dialog

from say import *

# load height profile from file
#


class Nurbs_LoadHeightProfileFromFile:
    def Activated(self):
        try:
            aktiv = App.ActiveDocument
            if aktiv == None:
                showdialog("Error", "no Sole Document",
                           "first open or create a sole document")

            fn = App.ParamGet(
                'User parameter:Plugins/shoe').GetString("height profile")
            if fn == '':
                fn = NURBSinit.DATA_PATH+"heelsv3.fcstd"

                App.ParamGet(
                    'User parameter:Plugins/shoe').SetString("height profile", fn)

            dok = App.open(fn)

            sss = dok.findObjects("Sketcher::SketchObject")

            try:
                s = sss[0]
                c = s.Shape.Edge1.Curve
            except:
                showdialog("Error", "Height profile document has no sketch")

            pts = c.discretize(86)

            mpts = []
            for i in [0, 15, 25, 35, 45, 55, 65, 75, 85]:
                mpts.append(pts[i])

            App.closeDocument(dok.Name)

            dok2 = aktiv
            App.setActiveDocument(dok2.Name)

            ss = dok2.Spreadsheet

            # write data in the spreadsheet
            for s in range(8):
                cn = cellname(s+3, 9)
                ss.set(cn, str(mpts[-s-1].y))

            # put up your heel
            for j in range(7):
                cn = cellname(j+2, 26)
                ss.set(cn, str((mpts[-1].y)))

            dok2.recompute()
            import sole
            # reload(sole)
            sole.run()
            dok2.recompute()

        except:
            showdialog()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Load Height Profile From File")
        return {'Pixmap': NURBSinit.ICONS_PATH+'drawing.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_LoadHeightProfileFromFile"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs  Nurbs_LoadHeightProfileFromFile", _tooltip)}

Gui.addCommand("Nurbs_LoadHeightProfileFromFile",
               Nurbs_LoadHeightProfileFromFile())
