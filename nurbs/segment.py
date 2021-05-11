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


'''create a segment of s bspline surface'''

# -*- coding: utf-8 -*-
# -- microelly 2017 v 0.1
# -- GNU Lesser General Public License (LGPL)


# \cond
import FreeCAD as App
import FreeCADGui as Gui
import os, sys

from say import *
import pyob

import NURBSinit

# \endcond

# Segment of a BSpline as a parametric Part::FeaturePython


class Segment(pyob.FeaturePython):
    '''Segment of a bspline surface or curve
    Restriction:
    the first surface Face1 or the first edge Edge1 is processed
    '''

    # \cond
    def __init__(self, obj):
        pyob.FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyLink", "source", "Base")
        obj.addProperty("App::PropertyInteger", "umin", "Base")
        obj.addProperty("App::PropertyInteger", "umax", "Base")
        obj.addProperty("App::PropertyInteger", "vmin", "Base")
        obj.addProperty("App::PropertyInteger", "vmax", "Base")
        obj.addProperty("App::PropertyBool", "closeV", "Base")

        obj.umax = -1
        obj.vmax = -1

        self.obj2 = obj
        pyob.ViewProvider(obj.ViewObject)
    # \endcond

    # The properties umin, umax, vmin, vmax are interpreted as numbers of the limiting nodes
    #

    def execute(self, obj):

        if len(obj.source.Shape.Faces) >= 1:
            face = obj.source.Shape.Face1
            bs = face.Surface.copy()
            uks = bs.getUKnots()
            vks = bs.getVKnots()
            bssegment(uks[obj.umin], uks[obj.umax],
                       vks[obj.vmin], vks[obj.vmax])
        else:
            edge = obj.source.Shape.Edge1
            bs = edge.Curve.copy()
            ks = bs.getKnots()
            bssegment(ks[obj.umin], ks[obj.umax])

        if obj.closeV:
            bs.setVPeriodic()

        obj.Shape = bs.toShape()


def createSegment(name="MySegment"):
    '''creates a segment from the source area or curve
    Segments are only possible for the given nodes
    umin, ... vmax: Enter the node number
    '''

    ffobj = App.ActiveDocument.addObject(
        "Part::FeaturePython", name)
    Segment(ffobj)
    return ffobj


# Modification of a BSpline as a parametric one Part::FeaturePython

class NurbsTrafo(pyob.FeaturePython):
    '''Rotate the pole array to move the seam'''

    # \cond
    def __init__(self, obj):
        pyob.FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyLink", "source", "Base")
        obj.addProperty("App::PropertyInteger", "start", "Base")
        obj.addProperty("App::PropertyInteger", "umax", "Base")
        obj.addProperty("App::PropertyInteger", "vmin", "Base")
        obj.addProperty("App::PropertyInteger", "vmax", "Base")
        obj.addProperty("App::PropertyBool", "swapaxes",
                        "Base").swapaxes = True

        obj.umax = -1
        obj.vmax = -1
        self.obj2 = obj
        pyob.ViewProvider(obj.ViewObject)
    # \endcond

    def execute(proxy, obj):
        ''' rotates the pole '''
        if len(obj.source.Shape.Faces) >= 1:
            face = obj.source.Shape.Face1
            bs = face.Surface.copy()

            poles = bs.getPoles()
            ku = bs.getUKnots()
            kv = bs.getVKnots()
            mu = bs.getUMultiplicities()
            mv = bs.getVMultiplicities()
            perU = bs.isUPeriodic()
            perV = bs.isVPeriodic()

            k = obj.start
#            if not bs.isVPeriodic():
#                print ("not vperiodic - can't do anything - cancellation"
#                return

            if obj.swapaxes:
                y = np.array(poles).swapaxes(0, 1)
                poles2 = np.concatenate([y[k:], y[:k]]).swapaxes(0, 1)
                poles2 = np.concatenate([y[k:-1], y[:k+1]]).swapaxes(0, 1)
            else:
                y = np.array(poles)
                poles2 = np.concatenate([y[k:], y[:k]])

            print(poles2)
            App.poles2 = poles
            print(ku)
            print(kv)

            bs2 = Part.BSplineSurface()
            bs2.buildFromPolesMultsKnots(poles2,
                                         mu, mv,
                                         ku, kv,
                                         perU, perV, 3, 3,)

            obj.Shape = bs2.toShape()

        else:
            bc = obj.source.Shape.Edge1.Curve.copy()
            pols = bc.getPoles()

            multies = bc.getMultiplicities()
            knots = bc.getKnots()
            deg = bc.Degree

            i = obj.start
            pols2 = pols[i:] + pols[:i]
            bc.buildFromPolesMultsKnots(pols2, multies, knots, True, deg)

            obj.Shape = bc.toShape()


def createNurbsTrafo(name="MyNurbsTafo"):
    ''' creates a NurbsTrafo object '''

    ffobj = App.ActiveDocument.addObject(
        "Part::FeaturePython", name)
    NurbsTrafo(ffobj)
    return ffobj

# Fine segment of a BSpline as a parametric one Part::FeaturePython


class FineSegment(pyob.FeaturePython):
    ''' creates a fine segment that is finer than the normal segmentation of the nurb
    factor indicates the number of the gradations
    the numbers umin, ... vmax are integral parts of factor
    '''

    # \cond
    def __init__(self, obj):
        pyob.FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyLink", "source", "Base")
        obj.addProperty("App::PropertyInteger", "factor", "Base")
        obj.addProperty("App::PropertyInteger", "umin", "Base")
        obj.addProperty("App::PropertyInteger", "umax", "Base")
        obj.addProperty("App::PropertyInteger", "vmin", "Base")
        obj.addProperty("App::PropertyInteger", "vmax", "Base")

        obj.factor = 100

        obj.umin = 0
        obj.vmin = 0
        obj.umax = obj.factor
        obj.vmax = obj.factor

        self.obj2 = obj
        pyob.ViewProvider(obj.ViewObject)
    # \endcond

#    def execute(proxy, obj):
#        pass

    # The properties umin, umax, vmin, vmax are divided by factor
    # and then interpreted as the limiting node
    #
    # FineSegment can cut very precisely with a large value of * factor *
    #

    def onChanged(self, obj, prop):
        if prop in ["vmin", "vmax", "umin", "umax", "source"]:

            if obj.source == None:
                return

            face = obj.source.Shape.Face1
            bs = face.Surface.copy()
#            bs.setUNotPeriodic()
#            bs.setVNotPeriodic()

            if obj.umin < 0:
                obj.umin = 0
            if obj.vmin < 0:
                obj.vmin = 0

            if obj.umax > obj.factor:
                obj.umax = obj.factor
            if obj.vmax > obj.factor:
                obj.vmax = obj.factor
            if obj.umin > obj.umax:
                obj.umin = obj.umax
            if obj.vmin > obj.vmax:
                obj.vmin = obj.vmax

            umin = 1.0/obj.factor*obj.umin
            umax = 1.0/obj.factor*obj.umax
            vmin = 1.0/obj.factor*obj.vmin
            vmax = 1.0/obj.factor*obj.vmax

            if bs.isVPeriodic() and not vmax < bs.getVKnots()[-1]:
                vmax = bs.getVKnots()[-1]
# does not work like that:
#                obj.vmax=int(round(vmax*obj.factor,0))

            if bs.isUPeriodic() and not umax < bs.getUKnots()[-1]:
                umax = bs.getUKnots()[-1]
#                obj.umax=int(round(umax*obj.factor,0))

#            print  bs.getUKnots()
#            print  bs.getVKnots()
#            print ("interval",umin,umax,vmin,vmax)

            if umin > 0 and umin not in bs.getUKnots():
                bs.insertUKnot(umin, 1, 0)

            if umax < obj.factor and umax not in bs.getUKnots():
                bs.insertUKnot(umax, 1, 0)

            if vmin > 0 and vmin not in bs.getVKnots():
                bs.insertVKnot(vmin, 1, 0)

            # and vmax< bs.getVKnots()[-1]:
            if vmax < obj.factor and vmax not in bs.getVKnots():
                bs.insertVKnot(vmax, 1, 0)

            uks = bs.getUKnots()
            if umin < uks[0]:
                umin = uks[0]

#            print ("interval",umin,umax,vmin,vmax)
            bssegment(umin, umax, vmin, vmax)
            obj.Shape = bs.toShape()


def createFineSegment(name="MyFineSegment"):
    ''' creates a FineSegment object '''

    ffobj = App.ActiveDocument.addObject("Part::FeaturePython", name)
    FineSegment(ffobj)
    return ffobj


def runsegment():
    '''Use case for the Gui.Selection a segment is generated'''

    source = None
    if len(Gui.Selection.getSelection()) != 0:
        source = Gui.Selection.getSelection()[0]
    s = createSegment()
    s.source = source
    sm.umax = -2
    sm.umin = 2


def runfinesegment():
    '''Use case for the Gui.Selection a FineSegement is generated'''

    source = None
    if len(Gui.Selection.getSelection()) != 0:
        source = Gui.Selection.getSelection()[0]
    s = createFineSegment()
    s.source = source


def runnurbstrafo():
    '''Use case for the Gui.Selection a NurbsTrafo is generated'''

    source = None
    if len(Gui.Selection.getSelection()) != 0:
        source = Gui.Selection.getSelection()[0]
    s = createNurbsTrafo()
    s.source = source


# \cond
def ThousandsOfMainFunction():

    sm = createSegment()
    sm.source = App.ActiveDocument.Poles
    sm.umax = 5

    k = createFineSegment()
    k.source = App.ActiveDocument.Poles

    s = createNurbsTrafo()
    s.source = App.ActiveDocument.Poles


# \endcond
