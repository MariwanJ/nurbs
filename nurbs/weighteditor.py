# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Part
import Draft
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

# -*- coding: utf-8 -*-
# -------------------------------------------------
# -- change sketcher constrains from a separate dialog
# --
# -- microelly 2017 v 0.1
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------
import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit
#import matplotlib.colors as colors


import PySide
from PySide import QtGui, QtCore


def runex(window):
    window.hide()
    for k in 'pk', 'pn', 'kn':
        try:
            App.ActiveDocument.removeObject(k)
        except:
            pass
    for k in window.texts:
        App.ActiveDocument.removeObject(k.Label)


def wrun(w):
    for q in w.box:
        print(w.sk.Label, q.i, q.value(), q.c.Name)
        w.sk.setDatum(q.i, 1+q.value())
    App.ActiveDocument.recompute()
    pk(w.sk, w)

# ---------------


def pk(obj=None, w=None):
    try:
        pk = App.ActiveDocument.pk
    except:
        pk = App.ActiveDocument.addObject("Part::Spline", "pk")
    try:
        kn = App.ActiveDocument.kn
    except:
        kn = App.ActiveDocument.addObject("Part::Spline", "kn")
    try:
        pn = App.ActiveDocument.pn
    except:
        pn = App.ActiveDocument.addObject("Part::Spline", "pn")

    if 1:
        pass

        # Hilfswire machen
        if obj != None:
            a = obj
        else:
            [a] = Gui.Selection.getSelection()
        bc = a.Shape.Edge1.Curve
        pts = a.Shape.Edge1.Curve.getPoles()
        print("Poles", len(pts))
        if len(w.texts) == 0:
            for i, p in enumerate(pts):
                t = Draft.makeText([str(i+1), '', '', '', ''], p, True)
                t.ViewObject.FontSize = 20
                w.texts.append(t)

        # _t=Draft.makeWire(pts,closed=True,face=False)
        p1 = Part.makePolygon(pts)
        pn.Shape = p1

        #pn.Label="Poles "+a.Label
        # pn.ViewObject.PointSize=10
        pn.ViewObject.PointColor = (1., 0., 1.)
        pn.ViewObject.LineColor = (1., 0., 1.)

        pts2 = [bc.value(k) for k in bc.getKnots()]
        print("Knots:", len(pts2))
        # _t=Draft.makeWire(pts,closed=True,face=False)
        p2 = Part.makePolygon(pts2)
        kn.Shape = p2
        #kn.Label="Knotes "+a.Label
        kn.ViewObject.PointSize = 10
        kn.ViewObject.PointColor = (0., 1., 1.)
        kn.ViewObject.LineColor = (0., 1., 1.)

        polys = []
        print(pts)
        print(pts2)
        for i in range(1, len(pts)):
            print(i, [pts[i], pts2[i-1]])
            try:
                polyg = Part.makePolygon([pts[i], pts2[i-1]])
                polys.append(polyg)
            except:
                pass

        comp = Part.makeCompound(polys)
        pk.Shape = comp


# -----------------


def dialog(sk=None):

    if sk == None:
        [sk] = Gui.Selection.getSelection()
    if 1:

        w = QtGui.QWidget()
        w.sk = sk
        w.texts = []

        tc = sk.ViewObject.LineColor
        color = colors.rgb2hex(sk.ViewObject.LineColor)
        invers = (1.0-tc[0], 1.0-tc[1], 1.0-tc[2])
        icolor = colors.rgb2hex(invers)
        mcolor = '#808080'
        w.setStyleSheet("QWidget { background-color:"+color+"}\
            QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
            background-color:#ccc;text-align:left;;padding:6px;padding-left:4px;color:#333; }")

        box = QtGui.QVBoxLayout()
        w.setLayout(box)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        l = QtGui.QLabel(sk.Label)
        l.setText('<font color='+icolor+'>'+sk.Label+'</font>')
        box.addWidget(l)

        w.box = []
        for i, c in enumerate(sk.Constraints):
            print(c.Name, c.Value)
            if c.Name.startswith("Weight"):
                l = QtGui.QLabel(c.Name)
                l.setText('<font color='+icolor+'>'+c.Name+'</font>')
                box.addWidget(l)

                d = QtGui.QSlider(QtCore.Qt.Horizontal)
                d.c = c
                d.i = i

                box.addWidget(d)
                d.setValue(c.Value-1)
                d.setMaximum(100)
                d.setMinimum(0)
                d.valueChanged.connect(lambda: wrun(w))
                w.box.append(d)

        w.r = QtGui.QPushButton("close")
        box.addWidget(w.r)
        w.r.pressed.connect(lambda: runex(w))
        wrun(w)
        w.show()

    return w


class Nurbs_WeightEditor:
    def Activated(self):
        for sk in Gui.Selection.getSelection():
            w = dialog(sk)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_WeightEditor")
        return {'Pixmap':  NURBSinit.ICONS_PATH + 'WeightEditor.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_WeightEditor"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs", _tooltip)}
Gui.addCommand("Nurbs_WeightEditor", Nurbs_WeightEditor())
