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

import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import Points
import Part
import Draft


import NURBSinit

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import random
import scipy as sp
from scipy import signal

from PySide import QtGui
import sys
import traceback
import random

import FreeCADGui as Gui 

import NURBSinit
import os
import Draft

if 0:
    pass

    # Make help wire
    [a] = Gui.Selection.getSelection()
    bc = a.Shape.Edge1.Curve
    pts = a.Shape.Edge1.Curve.getPoles()
    # print  (len(pts)
    # Draft.makeWire(pts)
    #App.ActiveDocument.ActiveObject.Label="Poles "+a.Label

    pts = [bc.value(k) for k in bc.getKnots()]
    print(len(pts))
    Draft.makeWire(pts)
    App.ActiveDocument.ActiveObject.Label = "Knotes "+a.Label
    App.ActiveDocument.ActiveObject.ViewObject.PointSize = 10
    App.ActiveDocument.ActiveObject.ViewObject.PointColor = (1., 0., 0.)

class Nurbs_RemoveKnots:
    def Activated(self):
        [a] = Gui.Selection.getSelection()
        bc0 = a.Object.Shape.Edge1.Curve
        kc = len(bc0.getKnots())
        
        for pos in range(1, kc):
            print(pos)
            # for t in (30000,40000,10000,5000,2000,1000,500,200,100,50,20,10,5,3,2,1):
            # 1.5 and 1 do not work
            for t in (20, 16, 14, 12, 6, 2, 1.5, 1):
                bc = bc0.copy()
                print("huhu")
                rc = bc.removeKnot(pos, 0, t)
                print(t, rc)
                if rc:
                    sp = App.ActiveDocument.addObject(
                        "Part::Spline", "approx Spline")
                    sp.Shape = bc.toShape()
                    App.ActiveDocument.ActiveObject.Label = "BC-" + \
                        str(pos)+" "+str(t)+" " + a.Object.Label
        
                #    pts=bc.getPoles()
                #    print  (len(pts)
                #    Draft.makeWire(pts)
                #    App.ActiveDocument.ActiveObject.Label="W-"+str(pos)+" "+a.Object.Label
                    if 0:
                        pts = [bc.value(k) for k in bc.getKnots()]
                #        print  (len(pts)
                        Draft.makeWire(pts)
                        App.ActiveDocument.ActiveObject.Label = "Kn " + \
                            str(t)+a.Object.Label
                        App.ActiveDocument.ActiveObject.ViewObject.PointSize = 12
                        App.ActiveDocument.ActiveObject.ViewObject.PointColor = (
                            0., 1., 0.)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_RemoveKnots")
        return {'Pixmap':  NURBSinit.ICONS_PATH + 'removeKnots.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_RemoveKnots"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs", _tooltip)}
Gui.addCommand("Nurbs_RemoveKnots", Nurbs_RemoveKnots())

