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

'''create some helper parts like the facebinder
for nurbs surfaces
modes are ["poleGrid","isoGrid","Surface"]
'''
import FreeCAD as App
import FreeCADGui as Gui
import os, sys

from say import *
import pyob

import NURBSinit
import nurbs
## The Helper can display a Poles Grid, iso-Curve Grid or single isocurves as parametric Part::FeaturePython objects
 

class Helper(pyob.FeaturePython):

    ##\cond
    def __init__(self, obj,uc=5,vc=5):
        pyob.FeaturePython.__init__(self, obj)

        self.TypeId="NurbsHelper"
        obj.addProperty("App::PropertyLink","source","XYZ","Length of the Nurbs")
        obj.addProperty("App::PropertyEnumeration","mode","XYZ","").mode=["poleGrid","isoGrid","Surface","uIso","vIso"]
        obj.addProperty("App::PropertyFloat","factor","XYZ","").factor=0
        obj.addProperty("App::PropertyFloat","param","XYZ","").param=4



    def attach(self,vobj):
        self.Object = vobj.Object

    ##\endcond

    def execute(self, fp):
        '''call VO.Proxy.updataData'''
        fp.ViewObject.Proxy.updateData(fp,"Execute")


#    def onChanged(self, fp, prop):
#        pass

#    def onDocumentRestored(self, fp):
#        say(["onDocumentRestored",str(fp.Label)+ ": "+str(fp.Proxy.__class__.__name__)])

    def create_knotes_shape2(self):
        '''create a grid of iso curves '''
#        #bs=self.obj2.source.Proxy.getBS()
#        print ("obj2",self.obj2)
        bs=self.obj2.source.Shape.Face1.Surface
#        print ("bs",bs)
#        #shape=.helper.create_knotes_shape(None,bs)

        uk=bs.getUKnots()
        vk=bs.getVKnots()

        sss=[]

        for iu in uk:
            pps=[]
            for iv in vk:
                p=bs.value(iu,iv)
                pps.append(p)
            tt=Part.BSplineCurve()
            tt.interpolate(pps)
            ss=tt.toShape()
            sss.append(ss)

        for iv in vk:
            pps=[]
            for iu in uk:
                p=bs.value(iu,iv)
                pps.append(p)
            tt=Part.BSplineCurve()
            tt.interpolate(pps)
            ss=tt.toShape()
            sss.append(ss)

        comp=Part.Compound(sss)
        self.obj2.Shape=comp
        print (comp)
        print (sss)
        return comp

    def create_curve(self):
        '''create a single isoCurve'''

        fp=self.obj2
        bs=self.obj2.source.Shape.Face1.Surface
        if fp.factor == 0.0:
            if fp.mode=='uIso':
                ks=bs.getUKnots()
                bc=bs.uIso(ks[int(fp.param)])
            elif fp.mode=='vIso':
                ks=bs.getVKnots()
                bc=bs.vIso(ks[int(fp.param)])
            else:
                raise Exception("unexpected mode: " + fp.mode)
        else:
            if fp.mode=='uIso':
                bc=bs.uIso(fp.param/fp.factor)
            elif fp.mode=='vIso':
                bc=bs.vIso(fp.param/fp.factor)
            else:
                raise Exception("unexpected mode: " + fp.mode)

        self.obj2.Shape=bc.toShape()




## The ViewProviderHelper uses updateData to recreate the shape 


class ViewProviderHelper(pyob.ViewProvider):

    ##\cond


    def attach(self, obj):
        obj.Proxy = self
        self.Object = obj


    def showVersion(self):
        cl=self.Object.Proxy.__class__.__name__
        PySide.QtGui.QMessageBox.information(None, "About ", "Nurbs"  +"\nVersion 0.0"  )


    def setupContextMenu(self, obj, menu):
        cl=self.Object.Proxy.__class__.__name__
        action = menu.addAction("About " + cl)
        action.triggered.connect(self.showVersion)

        action = menu.addAction("Edit ...")
        action.triggered.connect(self.edit)

    #        for m in self.cmenu + self.anims():
    #            action = menu.addAction(m[0])
    #            action.triggered.connect(m[1])

    ##\endcond

    def getIcon(self):
        '''symbol for the helper'''

        return """
            /* XPM */
            static const char * ViewProviderNurbs_xpm[] = {
            "16 16 6 1",
            "     c None",
            ".    c #141010",
            "+    c #615BD2",
            "@    c #C39D55",
            "#    c #000000",
            "$    c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def updateData(self, fp, prop):
        '''update the shape'''
        if prop == "Shape": return
        if prop == "Placement": return
        pm=fp.Placement
        if fp.source!=None:
            #say("VO updateData " + prop)
            #say((fp,fp.source,fp.mode))
            try:
                mode=fp.mode
                if mode == "poleGrid":
                    # fp.Shape=fp.source.Shape
                    fp.Shape=fp.source.Proxy.create_uv_grid_shape()
                elif mode == "isoGrid":
                    #fp.Shape=App.ActiveDocument.Torus.Shape
                    #fp.Shape=fp.source.Proxy.create_grid_shape()
                    print ("update isogrid")
                    fp.Proxy.create_knotes_shape2()
                elif mode == "uIso" or mode == "vIso":
                    print ("create Curve")
                    fp.Proxy.create_curve()
                else:
                    # fp.Shape=App.ActiveDocument.Cylinder.Shape
                    fp.Shape=fp.source.Shape
                    pass

            except:
                sayexc("Shape from Source")
            fp.Placement=pm
        else:
            #sayW("no source Shape")
            pass
        return



def makeHelper():
    ''' creates a Helper object as Part::FeaturePython
    the parameters must be set in a next step.
    '''
    a=App.ActiveDocument.addObject("Part::FeaturePython","Helper")
    a.Label="Nurbs Helper generated"
    Helper(a)
    ViewProviderHelper(a.ViewObject)
    a.ViewObject.ShapeColor=(0.00,1.00,1.00)
    a.ViewObject.Transparency = 70
    return a

class Nurbs_MakeHelperSel:
    def Activated(self):
        self.makeHelperSel()
    def makeHelperSel(self):
        ''' creates a helper of mode "isoGrid" for the Gui-selected objects'''
        for obj in Gui.Selection.getSelection():
            h=makeHelper()
            h.source=obj
            h.mode="isoGrid"
            h.Placement.Base.x=2400

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_MakeHelperSel")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_MakeHelperSel"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs ", _tooltip)}

Gui.addCommand("Nurbs_MakeHelperSel", Nurbs_MakeHelperSel())



class Nurbs_HelperTest:
    def Activated(self):
        self.RunTest()
    def RunTest(self):
        '''testcase creates a nurbs and 3 helpers'''

        try:
            App.closeDocument("Unnamed")
            App.newDocument("Unnamed")
            App.setActiveDocument("Unnamed")
            App.ActiveDocument=App.getDocument("Unnamed")
            Gui.ActiveDocument=Gui.getDocument("Unnamed")
        except:
            pass

        import nurbs
        nurbs.testRandomB()

        hp=makeHelper()
        hp.source=App.ActiveDocument.Nurbs
        hp.Label="Helper Surface"
        hp.mode="Surface"
        hp.Placement.Base.x=1200

        hp2=makeHelper()
        hp2.source=App.ActiveDocument.Nurbs
        hp2.mode="isoGrid"
        hp2.Placement.Base.x=2400
        hp2.Label="Helper isoGrid"

        hp3=makeHelper()
        hp3.source=App.ActiveDocument.Nurbs
        hp3.mode="poleGrid"
        hp3.Placement.Base.x=3600
        hp3.Label="Helper poleGrid"

        Gui.activeDocument().activeView().viewAxonometric()
        Gui.SendMsgToActiveView("ViewFit")

        hp4=makeHelper()
        hp4.source=App.ActiveDocument.Nurbs
        hp4.Label="Helper isoCurve U"
        hp4.factor=0
        hp4.mode="uIso"
        hp4.param=3

        hp5=makeHelper()
        hp5.source=App.ActiveDocument.Nurbs
        hp5.Label="Helper isoCurve V"
        hp5.factor=0
        hp5.mode="vIso"
        hp5.param=3


    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_HelperTest")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Nurbs", "Nurbs_HelperTest"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs ", _tooltip)}

Gui.addCommand("Nurbs_HelperTest", Nurbs_HelperTest())

