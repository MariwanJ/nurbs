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

'''convert a draft bspline to a sketcher bspline'''
# -*- coding: utf-8 -*-
# -------------------------------------------------
# -- microelly 2017 v 0.1
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------
import NURBSinit
import FreeCAD as App
import FreeCADGui as Gui 
import os,sys

import Part 
import random

from say import *
from scipy.signal import argrelextrema
import Sketcher

import NURBSinit

# creates a BSpline Curve approximation Sketch for a list of points
#


def createSketchSpline(pts=None, label="BSpline Sketch", periodic=True):
    '''createSketchSpline(pts=None,label="BSpline Sketch",periodic=True)'''

    try:
        body = App.ActiveDocument.Body
    except:
        body = App.ActiveDocument.addObject('PartDesign::Body', 'Body')

    sk = App.ActiveDocument.addObject('Sketcher::SketchObject', 'Sketch')
    sk.Label = label
    sk.MapMode = 'FlatFace'

    App.ActiveDocument.recompute()

    if pts == None:  # some test data
        pts = [App.Vector(a) for a in [(10, 20, 30),
                                       (30, 60, 30), (20, 50, 40), (50, 80, 90)]]

    for i, p in enumerate(pts):
        sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)), int(
            round(p.y)), 0), App.Vector(0, 0, 1), 10), True)
        #if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000))
        #if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i))

        radius = 2.0
        sk.addConstraint(Sketcher.Constraint('Radius', i, radius))
        sk.renameConstraint(i, 'Weight ' + str(i+1))

        # i=5; App.ActiveDocument.Sketch016.setDatum(i,40))

    k = i+1
    l = [App.Vector(int(round(p.x)), int(round(p.y))) for p in pts]

    if not periodic:
        ll = sk.addGeometry(Part.BSplineCurve(
            l, None, None, False, 3, None, False), False)
    else:
        ll = sk.addGeometry(Part.BSplineCurve(
            l, None, None, True, 3, None, False), False)

    conList = []
    for i, p in enumerate(pts):
        conList.append(Sketcher.Constraint(
            'InternalAlignment:Sketcher::BSplineControlPoint', i, 3, k, i))
    sk.addConstraint(conList)

    App.ActiveDocument.recompute()

    sk.Placement = App.Placement(App.Vector(
        0, 0, p.z), App.Rotation(App.Vector(1, 0, 0), 0))
    sk.ViewObject.LineColor = (
        random.random(), random.random(), random.random())
    App.ActiveDocument.recompute()
    return sk


def mergeSketchSpline(pts=None, label="BSpline Sketch", periodic=True, name="Sketch"):
    '''createSketchSpline(pts=None,label="BSpline Sketch",periodic=True)'''

    try:
        body = App.ActiveDocument.Body
    except:
        body = App.ActiveDocument.addObject('PartDesign::Body', 'Body')

    sk = App.ActiveDocument.getObject(name)
    if sk == None:
        sk = App.ActiveDocument.addObject('Sketcher::SketchObject', name)

    sk.Label = label
    sk.MapMode = 'FlatFace'

    App.ActiveDocument.recompute()

    if pts == None:  # some test data
        pts = [App.Vector(a) for a in [(10, 20, 30),
                                       (30, 60, 30), (20, 50, 40), (50, 80, 90)]]

    js = []
    for i, p in enumerate(pts):
        j = sk.addGeometry(Part.Circle(App.Vector(
            int(round(p.x)), int(round(p.y)), 0), App.Vector(0, 0, 1), 10), True)
        sk

        # if something is already there, connect
        if i == 0 and int(sk.GeometryCount) >= 2:
            sk.addConstraint(Sketcher.Constraint('Coincident', j-2, 3, j, 3))

        j = int(sk.GeometryCount)-1
        js.append(j)
        #if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000))
        #if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i))

        radius = 2.0
        cj = sk.addConstraint(Sketcher.Constraint('Radius', j, radius))
        print("Constraint ", cj)
        sk.renameConstraint(cj, 'Weight ' + str(cj+1))

        # i=5; App.ActiveDocument.Sketch016.setDatum(i,40))

    l = [App.Vector(int(round(p.x)), int(round(p.y))) for p in pts]

    if not periodic:
        ll = sk.addGeometry(Part.BSplineCurve(
            l, None, None, False, 3, None, False), False)
    else:
        ll = sk.addGeometry(Part.BSplineCurve(
            l, None, None, True, 3, None, False), False)

    k = int(sk.GeometryCount)-1

    rc = sk.solve()
    conList = []
    for i, j in enumerate(js):

        conList.append(Sketcher.Constraint(
            'InternalAlignment:Sketcher::BSplineControlPoint', j, 3, k, i))
        print("okay")

    sk.addConstraint(conList)

    App.ActiveDocument.recompute()

    sk.Placement = App.Placement(App.Vector(
        0, 0, p.z), App.Rotation(App.Vector(1, 0, 0), 0))
    sk.ViewObject.LineColor = (
        random.random(), random.random(), random.random())
    App.ActiveDocument.recompute()
    return sk


def closecurve(sk):
    j = int(sk.GeometryCount)-2
    sk.addConstraint(Sketcher.Constraint('Coincident', 0, 3, j, 3))


def runobj(obj, label=None):
    '''creates the SketchSpline for an object'''

    sk = createSketchSpline(
        obj.Shape.Edge1.Curve.getPoles(), str(obj.Label) + " Sketch")
    if label != None:
        sk.Label = label
    return sk

class Nurbs_CreateSketchSpline_runsubs:
    def Activated(self):
        self.runsubs()
    def runsubs(self):
        '''creates sketches for several sub-edges'''
        sx = Gui.Selection.getSelection()
        s = sx[0]
        for so in s.SubObjects:
            try:
                bc = so.Curve
                pts = bc.getPoles()
                l = s.ObjectName
                print(l, len(pts))
                periodic = bc.isPeriodic()
                createSketchSpline(pts, str(l) + " Sketch", periodic)
            except:
                sayexc2(title='Error', mess='something wrong with ' + obj.Label)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_CreateSketchSpline_runsubs")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_CreateSketchSpline_runsubs"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs ", _tooltip)}

Gui.addCommand("Nurbs_CreateSketchSpline_runsubs", Nurbs_CreateSketchSpline_runsubs())




class Nurbs_CreateSketchSpline_Runall:
    def Activated(self):
        self.runall()
        
    def runall(self):
        '''creates sketches for several sub-edges'''
        rc=None
        sx = Gui.Selection.getSelection()
        s = sx[0]
        name = "mergeS_"+s.Name
        for so in s.Shape.Edges:
            print(so)
            try:
                bc = so.Curve
                print(bc)
                pts = bc.getPoles()
                print(pts)
                l = s.Label
                print(l)
                print(l, len(pts))
                periodic = bc.isPeriodic()
                # createSketchSpline(pts,str(l) + " Sketch" ,periodic)
                rc = mergeSketchSpline(pts, str(l) + " Sketch", periodic, name)
                name = rc.Name
            except:
                sayexc2(title='Error', mess='something wrong with ' + s.Label)
        closecurve(rc)

    def GetResources(self):      
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_CreateSketchSpline_Runall")
        return {'Pixmap':  NURBSinit.ICONS_PATH + 'drawing.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_CreateSketchSpline_Runall"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs", _tooltip)}

Gui.addCommand("Nurbs_CreateSketchSpline_Runall", Nurbs_CreateSketchSpline_Runall())



class Nurbs_createSketchSpline:
    '''convert a draft bspline to a sketcher bspline'''
    def Activated(self):
        '''creates a sketch for each selected object from Edge1'''

        if len(Gui.Selection.getSelection()) == 0:
            showdialog('Oops', 'nothing selected - nothing to do for me',
                       'Please select a Draft Bspline or Draft Wire')

        for obj in Gui.Selection.getSelection():
            try:
                bc = obj.Shape.Edge1.Curve
                pts = bc.getPoles()
                l = obj.Label
                print(l, len(pts))
                periodic = bc.isPeriodic()
                createSketchSpline(pts, str(l) + " Sketch", periodic)
            except:
                sayexc2(title='Error', mess='something wrong with ' + obj.Label)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_createSketchSpline")
        return {'Pixmap':  NURBSinit.ICONS_PATH + 'drawing.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_createSketchSpline"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs", _tooltip)}

Gui.addCommand("Nurbs_createSketchSpline", Nurbs_createSketchSpline())