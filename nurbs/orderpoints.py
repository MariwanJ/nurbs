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

# -*- coding: utf-8 -*-
# -------------------------------------------------
# -- radial ordering of a xy-planar point cloudc
# -- microelly 2017 v 0.1
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


import random
import Draft
import Part

import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit

import scipy as sp
from scipy.signal import argrelextrema


try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    

import Plot2 as plt

from PySide import QtGui
import sys
import traceback
import random


def showdialog(title="Error", text="See the ReportView for more details", detail=None):
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle(title)
    if detail != None:
        msg.setDetailedText(detail)
    msg.exec_()


def sayexc(title='Error', mess=''):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    ttt = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    lls = eval(ttt)
    l = len(lls)
    l2 = lls[(l-3):]
    App.Console.PrintError(mess + "\n" + "-->  ".join(l2))
    showdialog(title, text=mess, detail="--> ".join(l2))


''' transfer point set into path '''


def orderdata(obj, inner=False, plotit=False, medianfil=0, cf=True):
    pts = None
    try:
        pts = obj.Points.Points
        print("Points")
    except:
        pts = obj.Points
        print("Draft")

    npts = np.array(pts).swapaxes(0, 1)
    mp = (npts[0].mean(), npts[1].mean(), npts[2].mean())

    vm = App.Vector(mp)
    lengths = np.array([(App.Vector(p)-vm).Length for p in pts])

    lax = lengths.max()
    lin = lengths.min()
    lea = lengths.mean()

    pl2 = App.Placement()
    pl2.Base = vm

    # restrictive circles
    if 0 and cf:
        if medianfil > 0:
            circle = Draft.makeCircle(radius=lea, placement=pl2, face=False)
            circle.Label = "Mean Circle"
            App.ActiveDocument.ActiveObject.ViewObject.LineColor = (0., 0., 1.)

        else:
            if inner:
                circle = Draft.makeCircle(
                    radius=lin, placement=pl2, face=False)
                circle.Label = "Inner Circle"
                App.ActiveDocument.ActiveObject.ViewObject.LineColor = (
                    0., 1., 0.)
            else:
                circle = Draft.makeCircle(
                    radius=lax, placement=pl2, face=False)
                circle.Label = "Outer Circle"
                App.ActiveDocument.ActiveObject.ViewObject.LineColor = (
                    1., 0., 0.)

    aps = {}
    rads = {}

    for v in pts:
        vn = v-vm
        #    print np.arctan2(vm.x,vm.y)
        try:
            if aps[np.arctan2(vn.x, vn.y)] != vn:
                print("Error 2 points same direction")
                print(v)
                print(aps[np.arctan2(vn.x, vn.y)])
        except:
            aps[np.arctan2(vn.x, vn.y)] = vn
            rads[np.arctan2(vn.x, vn.y)] = vn.Length

    kaps = aps.keys()
    kaps.sort()

    ptss = [aps[k] for k in kaps]
    radss = np.array([rads[k] for k in kaps])

    if medianfil > 0:
        l4 = np.array(radss)
        # window size for smoothing
        f = medianfil
        path = np.concatenate([[l4[0]] * f, l4, [l4[-1]]*f])
        y2 = sp.signal.medfilt(path, f)
        mmaa = y2[f:-f]

        if plotit:
            import Plot2
            Plot2.figureWindow("Win1")

            Plot2.plot(kaps, radss, 'radss')
            Plot2.plot(kaps, mmaa, 'mmaa')
            Plot2.legend(True)
            # plt.show()

    else:

        if inner:
            z1 = argrelextrema(radss, np.less)
        else:
            z1 = argrelextrema(radss, np.greater)

        z1 = z1[0]
        zaps = np.array(kaps)[z1]
        mm1 = radss[z1]

        if inner:
            z = argrelextrema(mm1, np.less)
        else:
            z = argrelextrema(mm1, np.greater)

        z = z[0]
        zaps2 = np.array(z1)[z]
        zaps = np.array(kaps)[zaps2]
        mm = mm1[z]

        mmaa = np.interp(kaps, zaps, mm)

        if plotit:
            import Plot2
            Plot2.figureWindow("Win2")
            Plot2.plot(kaps, radss, 'radss')
            Plot2.plot(kaps, mm, 'mm')
            Plot2.plot(kaps, mmaa, 'mmaa')
            Plot2.legend(True)

#            plt.plot(kaps,radss, 'r-')
#            plt.plot(zaps,mm, 'bo-')
#            plt.plot(kaps,mmaa, 'b-')
#            plt.show()

    y = np.cos(kaps)
    x = np.sin(kaps)
    x *= mmaa
    y *= mmaa
    z = x*0

    pps = np.array([x, y, z]).swapaxes(0, 1)
    goods = [App.Vector(tuple(p))+vm for p in pps[1:]]
    Draft.makeWire(goods, closed=True, face=False)


def ThousandsOfRunWhatShouldIdo():

    # default parameters
    p = {
        "MedianFilterWindow": [21, 'Integer'],
        "ShowDataPlots": [False, 'Boolean'],
        "DrawCircles": [True, 'Boolean'],
        "inner": [False, 'Boolean'],
        "outer": [False, 'Boolean'],
        "median": [False, 'Boolean'],
        "debug": [False, 'Boolean'],
    }

    # parameter -----------------
    t = App.ParamGet('User parameter:Plugins/nurbs/'+'orderpoints')
    l = t.GetContents()
    if l == None:
        l = []
    for k in l:
        p[k[1]] = k[2]
    for k in p:
        if p[k].__class__.__name__ == 'list':
            typ = p[k][1]
            if typ == 'Integer':
                t.SetInt(k, p[k][0])
            if typ == 'Boolean':
                t.SetBool(k, p[k][0])
            if typ == 'String':
                t.SetString(k, p[k][0])
            if typ == 'Float':
                t.SetFloat(k, p[k][0])
            p[k] = p[k][0]
    # --------------------

    mf = p['MedianFilterWindow']
    dp = p["ShowDataPlots"]
    inner = p['inner']
    outer = p['outer']
    median = p["median"]
    debug = p['debug']
    cf = p['DrawCircles']

    if len(Gui.Selection.getSelection()) == 0:
        showdialog('Oops', 'nothing selected - nothing to do for me',
                   'Please select a point cloud')

    inner = False
    outer = False
    inner = True
    outer = True

    for obj in Gui.Selection.getSelection():
        if median:
            orderdata(obj, medianfil=mf, plotit=True, cf=cf)
            App.ActiveDocument.ActiveObject.Label = obj.Label + \
                " Median " + str(mf) + " Approx"
            App.ActiveDocument.ActiveObject.ViewObject.LineColor = (0., 0., 1.)
            Gui.updateGui()
        if inner:
            orderdata(obj, inner=True, plotit=dp)
            App.ActiveDocument.ActiveObject.Label = "Inner Approx for " + obj.Label
            App.ActiveDocument.ActiveObject.ViewObject.LineColor = (0., 1., 0.)
            Gui.updateGui()
        if outer:
            orderdata(obj, inner=False, plotit=dp)
            App.ActiveDocument.ActiveObject.Label = "Outer Approx for " + obj.Label
            App.ActiveDocument.ActiveObject.ViewObject.LineColor = (1., 0., 0.)
            Gui.updateGui()
