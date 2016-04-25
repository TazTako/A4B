######################################################################################################
# Author: TazTako (Olivier FAVRE), Lapineige, Pitiwazou (Cedric LEPILLER), Matpi                     #
# License: GPL v3                                                                                    #
######################################################################################################

bl_info = {
    "name": "Atelier 4 Blender (A4B)",
    "author": "TazTako (Olivier FAVRE), Lapineige, Pitiwazou (Cedric LEPILLER), Matpi",
    "version": (0, 3 , 2),
    "blender": (2, 72, 0),
    "description": "Atelier 4 Blender",
    "warning": "This addon is still in development.",
    "wiki_url": "http://blenderlounge.fr/forum/viewtopic.php?f=26&t=1524",
    "tracker_url": "http://blenderlounge.fr/forum/viewtopic.php?f=26&t=1524",
    "category": "User Interface"}
    
import bpy
import math
import sys
import bmesh
import os
from bpy.types import Menu, Header, PropertyGroup, Panel, UIList
from bpy.types import Menu, Operator
from bpy.props import IntProperty, FloatProperty, BoolProperty, CollectionProperty, FloatVectorProperty, StringProperty, EnumProperty
from mathutils import * 
from mathutils import Vector

############################################################################################################
#                                                    Preferences Panel                                     #
############################################################################################################

class TazTakoClicUserPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
        
    bpy.types.Scene.Enable_Install = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_AvertTab = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_AvertLoopTools = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_AvertBsurfaces = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_AvertIce = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_URL = bpy.props.BoolProperty(default=False)
            
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.scene, "Enable_Install", text="Installez le start-up fourni avant de faire joujou !", icon="ERROR")
        if context.scene.Enable_Install:
            layout.label(text="Lorsque vous installez cet addon, mes pies vont rechercher des layouts de screens pré-définis.")
            layout.label(text="Ceux-ci sont fournis dans le fichier .zip (startup_A4B.blend).")     
            layout.label(text="")
            layout.label(text="Si vous ne chargez pas ses screens, mes pie ne fonctionneront pas,")
            layout.label(text="car j'ai choisi d'adopter une philosophie de travail en atelier similaire à FreeCAD.")
            layout.label(text="")
            layout.label(text="A chaque atelier (screen layout) correspond une étape du processus de la 3D (modé, sculpt, retopo, UV, shading, FX...),")
            layout.label(text="et à chaque atelier, les pie changent de forme pour s'adapter au mieux à votre workflow.")
                                    
        layout.prop(context.scene, "Enable_AvertTab", text="KeyMap par défaut", icon="QUESTION")
        if context.scene.Enable_AvertTab:
            layout.label(text="La keymap utilise les boutons 4 & 5 de la souris associés à la touche Ctrl:")
            layout.label(text="le bouton 5 affiche le pie d'affichage")     
            layout.label(text="le bouton 5 (associé à Ctrl) affiche le pie des ateliers")
            layout.label(text="le bouton 4 affiche le 1er pie d'outils")
            layout.label(text="le bouton 4 (associé à Ctrl) affiche le 2ème pie d'outils")
                    
        layout.prop(context.scene, "Enable_URL", text="Remerciements et Liens", icon="URL")
        if context.scene.Enable_URL:
            row = layout.row(align=True)
            row.label(text="Cet addon n'aurait jamais vu le jour sans le soutien de la communauté BlenderLounge :")
            row.operator("wm.url_open", text="forum BlenderLounge").url = "http://blenderlounge.fr/forum/viewtopic.php?f=26&t=1524"
            row = layout.row(align=True)
            row.label(text="Le blog de l'auteur Olive/TazTako (Olivier FAVRE):")
            row.operator("wm.url_open", text="bd.olidou.com").url = "http://bd.olidou.com"
            
####################################################################################################################################################
#                                                         Classes du Pie Tools                                                                     #
####################################################################################################################################################

# Align X
class AlignX(bpy.types.Operator):  
    bl_idname = "align.x"  
    bl_label = "Align  X"  
  
    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'} 
    
# Align Y
class AlignY(bpy.types.Operator):  
    bl_idname = "align.y"  
    bl_label = "Align  Y"  
  
    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}    

# Align Z
class AlignZ(bpy.types.Operator):  
    bl_idname = "align.z"  
    bl_label = "Align  Z"  
  
    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

# Align to X - 0
class AlignToX0(bpy.types.Operator):  
    bl_idname = "align.2x0"  
    bl_label = "Align To X-0"  
  
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        for vert in bpy.context.object.data.vertices:
            if vert.select: 
                vert.co[0] = 0
        bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}     

# Align to Y - 0
class AlignToY0(bpy.types.Operator):  
    bl_idname = "align.2y0"  
    bl_label = "Align To Y-0"  
  
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        for vert in bpy.context.object.data.vertices:
            if vert.select: 
                vert.co[1] = 0
        bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}      

# Align to Z - 0
class AlignToZ0(bpy.types.Operator):  
    bl_idname = "align.2z0"  
    bl_label = "Align To Z-0"  
  
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        for vert in bpy.context.object.data.vertices:
            if vert.select: 
                vert.co[2] = 0
        bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}

# Align X West / Left
class AlignXLeft(bpy.types.Operator):  
    bl_idname = "alignx.left"  
    bl_label = "Align X Left"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 0
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}

# Align X East / Right
class AlignXRight(bpy.types.Operator):  
    bl_idname = "alignx.right"  
    bl_label = "Align X Right"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 0
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}
    
# Align Y North / Back
class AlignYBack(bpy.types.Operator):  
    bl_idname = "aligny.back"  
    bl_label = "Align Y back"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 1
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}

# Align Y South / Front
class AlignYFront(bpy.types.Operator):  
    bl_idname = "aligny.front"  
    bl_label = "Align Y Front"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 1
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}
    
# Align Z Top
class AlignZTop(bpy.types.Operator):  
    bl_idname = "alignz.top"  
    bl_label = "Align Z Top"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 2
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}  
    
# Align Z Bottom
class AlignZBottom(bpy.types.Operator):  
    bl_idname = "alignz.bottom"  
    bl_label = "Align Z Bottom"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 2
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}

# Apply Rotation
class ApplyRotation(bpy.types.Operator):                  
    """This Operator apply rotation of selected object"""                   
    bl_idname = "object.applyrotation"                     
    bl_label = "Apply rotation on object"        

    @classmethod                                     
    def poll(cls, context):                         
        return context.active_object is not None 

    def execute(self, context):                     
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'} 
    
# Apply Scale
class ApplyScale(bpy.types.Operator):                  
    """This Operator apply scale of selected object"""                   
    bl_idname = "object.applyscale"                     
    bl_label = "Apply scale on object"        

    @classmethod                                     
    def poll(cls, context):                         
        return context.active_object is not None 

    def execute(self, context):                     
        
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'} 
    
# Create Hole
class CreateHole(bpy.types.Operator):                  
    """This Operator create a hole on a selection"""                   
    bl_idname = "object.createhole"                     
    bl_label = "Create Hole on a Selection"        

    @classmethod                                     
    def poll(cls, context):                         
        return context.active_object is not None 

    def execute(self, context):                     
        
        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.resize(value=(0.6, 0.6, 0.6))
        bpy.ops.mesh.looptools_circle()
        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))
        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'} 
    
# Selection "Inverser" Edit/Object Mode
class ClassSelectionTakoRevert(bpy.types.Operator):
    """Invert Selection"""
    bl_idname = "class.selectiontakorevert"
    bl_label = "Class Selection Tako Revert"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.select_all(action="INVERT")
        else:
            bpy.ops.mesh.select_all(action="INVERT")           
        return {'FINISHED'}

# Separate Loose Parts (Wazou)
class WazouSeparateLooseParts(bpy.types.Operator):  
    """Separate Loose Parts"""
    bl_idname = "object.wazou_separate_looseparts"  
    bl_label = "Separate Loose Parts" 
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='TOGGLE')
        return {'FINISHED'}

# Pivot to selection
class PivotToSelection(bpy.types.Operator):  
    """Move Pivot to Selection """
    bl_idname = "object.pivot2selection"  
    bl_label = "Pivot To Selection"  
  
    def execute(self, context):
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = saved_location
        bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

# Pivot to Bottom (Modes Objet or Edit)
class PivotBottom(bpy.types.Operator):  
    """Move Pivot to Bottom of Geometry"""
    bl_idname = "object.pivotobottom"  
    bl_label = "Pivot To Bottom"  
  
    def execute(self, context):
        
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.z
                     init=1
                 elif x.co.z<a:
                     a=x.co.z
                     
            for x in o.data.vertices:
                 x.co.z-=a

            o.location.z+=a
            
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.z
                     init=1
                 elif x.co.z<a:
                     a=x.co.z
                     
            for x in o.data.vertices:
                 x.co.z-=a

            o.location.z+=a 
            bpy.ops.object.mode_set(mode = 'EDIT')
            
        return {'FINISHED'}


# Pivot to geometry (évite de repasser en mode object)
class PivotToGeometry(bpy.types.Operator):  
    """Move Pivot to Center of Geometry"""
    bl_idname = "object.pivot2geometry"  
    bl_label = "Pivot To Geometry"  
  
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

# Pivot to 3D-Cursor (évite de repasser en mode object)
class PivotToCursor(bpy.types.Operator):  
    """Move Pivot to 3D-Cursor"""
    bl_idname = "object.pivot2cursor"  
    bl_label = "Pivot To 3D-Cursor"  
  
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

# LapRelax
class LapRelax(bpy.types.Operator):
    """Apply a "Relax" on Selection (smoothing mesh keeping volume)"""
    bl_idname = "mesh.laprelax"
    bl_label = "LapRelax"
    bl_description = "Smoothing mesh keeping volume"
    bl_options = {'REGISTER', 'UNDO'}
    
    Repeat = bpy.props.IntProperty(
        name = "Repeat", 
        description = "Repeat how many times",
        default = 1,
        min = 1,
        max = 100)


    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH')

    def invoke(self, context, event):
        
        # smooth #Repeat times
        for i in range(self.Repeat):
            self.do_laprelax()
        
        return {'FINISHED'}
    
    def do_laprelax(self):

        context = bpy.context
        region = context.region  
        area = context.area
        selobj = bpy.context.active_object
        mesh = selobj.data
        bm = bmesh.from_edit_mesh(mesh)
        bmprev = bm.copy()

        for v in bmprev.verts:
            if v.select:
                tot = Vector((0, 0, 0))
                cnt = 0
                for e in v.link_edges:
                    for f in e.link_faces:
                        if not(f.select):
                            cnt = 1
                    if len(e.link_faces) == 1:
                        cnt = 1
                        break
                if cnt:
                    # dont affect border edges: they cause shrinkage
                    continue
                    
                # find Laplacian mean
                for e in v.link_edges:
                    tot += e.other_vert(v).co
                tot /= len(v.link_edges)
                
                # cancel movement in direction of vertex normal
                delta = (tot - v.co)
                if delta.length != 0:
                    ang = delta.angle(v.normal)
                    deltanor = math.cos(ang) * delta.length
                    nor = v.normal
                    nor.length = abs(deltanor)
                    bm.verts[v.index].co = tot + nor
                
                
        mesh.update()
        bm.free()
        bmprev.free()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()    

# UV-Image Sculpt / Grab
class UVSculptGrab(bpy.types.Operator):  
    """Grab the UV"""
    bl_idname = "sculpt.sculptgrab"  
    bl_label = "Scult UV - Grab"  
  
    def execute(self, context):
        if bpy.context.tool_settings.use_uv_sculpt == False:
            bpy.context.scene.tool_settings.use_uv_sculpt = True
            bpy.ops.sculpt.uv_sculpt_stroke(mode = 'NORMAL')
            bpy.context.scene.tool_settings.uv_sculpt_tool = 'GRAB'
        else:
            bpy.context.scene.tool_settings.uv_sculpt_tool = 'GRAB'
        return {'FINISHED'}
    
# UV-Image Sculpt / Relax
class UVSculptRelax(bpy.types.Operator):  
    """Relax the UV"""
    bl_idname = "sculpt.sculptrelax"  
    bl_label = "Scult UV - Relax"  
  
    def execute(self, context):
        if bpy.context.tool_settings.use_uv_sculpt == False:
            bpy.context.scene.tool_settings.use_uv_sculpt = True
            bpy.ops.sculpt.uv_sculpt_stroke(mode = 'NORMAL')
            bpy.context.scene.tool_settings.uv_sculpt_tool = 'RELAX'
        else:
            bpy.context.scene.tool_settings.uv_sculpt_tool = 'RELAX'
        return {'FINISHED'}
    
# UV-Image Sculpt / Pinch
class UVSculptPinch(bpy.types.Operator):  
    """Pinch the UV"""
    bl_idname = "sculpt.sculptpinch"  
    bl_label = "Scult UV - Pinch"  
  
    def execute(self, context):
        if bpy.context.tool_settings.use_uv_sculpt == False:
            bpy.context.scene.tool_settings.use_uv_sculpt = True
            bpy.ops.sculpt.uv_sculpt_stroke(mode = 'NORMAL')
            bpy.context.scene.tool_settings.uv_sculpt_tool = 'PINCH'
        else:
            bpy.context.scene.tool_settings.uv_sculpt_tool = 'PINCH'
        return {'FINISHED'}

# UV-Image Sculpt / Toggle
class UVSculptToggle(bpy.types.Operator):  
    """Quit "Sculpt UV" (return to normal mode) """
    bl_idname = "sculpt.sculpttoggle"  
    bl_label = "Scult UV - Toggle"  
  
    def execute(self, context):
        if bpy.context.tool_settings.use_uv_sculpt == False:
            bpy.context.scene.tool_settings.use_uv_sculpt = True
        else:
            bpy.context.scene.tool_settings.use_uv_sculpt = False
        return {'FINISHED'}
    
##################################################################################################################
#                                  Classes appelant les Layouts (via la touche "Tab")                            #               
##################################################################################################################

# Change Layout
class TazTakoScreenSetLayout(bpy.types.Operator):
    """Switches to the screen layout of the given name."""
    bl_idname="taz.layout"
    bl_label="Switch to Screen Layout"
    LayoutName = bpy.props.StringProperty()# définit variable LayoutName comme une propriété de chaîne de caractères
    def execute(self,context):
        bpy.context.window.screen = bpy.data.screens[self.LayoutName]# définit variable LayoutName
        return{'FINISHED'}
    def invoke(self,context,event):
        return self.execute(context)
    
# Switch between layouts "A4B-Animation" & "A4B-FX"
class ClassLayoutAnim(bpy.types.Operator):
    """Switch between layout "A4B-Animation" & "A4B-FX" """
    bl_idname = "class.layoutanim"
    bl_label = "Class Layout Animation"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.window.screen == bpy.data.screens["A4B-Animation"]:
            bpy.context.window.screen = bpy.data.screens["A4B-FX"]
        else:
            bpy.context.window.screen = bpy.data.screens["A4B-Animation"]
        return {'FINISHED'}    

# Switch between layouts "A4B-Skinning" & "A4B-Hair"
class ClassLayoutSkin(bpy.types.Operator):
    """Switch between layout "A4B-Skinning" & "A4B-Hair" """
    bl_idname = "class.layoutskin"
    bl_label = "Class Layout Skin"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.screen == bpy.data.screens["A4B-Skinning"]:
            bpy.context.window.screen = bpy.data.screens["A4B-Hair"]
        else:
            bpy.context.window.screen = bpy.data.screens["A4B-Skinning"]
        return {'FINISHED'}    
    
# Switch between layouts "A4B-Edit Mode" & "A4B-Scene"
class ClassLayoutEdit(bpy.types.Operator):
    """Switch between layout "A4B-Scene" & "A4B-Edit" """
    bl_idname = "class.layoutedit"
    bl_label = "Class Layout Edit"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.screen == bpy.data.screens["A4B-Scene"] or bpy.context.object.mode == 'OBJECT':
            bpy.context.window.screen = bpy.data.screens["A4B-Edit Mode"]
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.context.window.screen = bpy.data.screens["A4B-Scene"]
            bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}
    

# Switch between layouts "A4B-Nodal" & "A4B-UV Editing"
class ClassLayoutNodal(bpy.types.Operator):
    """Switch between layouts "A4B-Nodal" & "A4B-UV Editing" """
    bl_idname = "class.layoutnodal"
    bl_label = "Class Layout Nodal"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.screen == bpy.data.screens["A4B-Nodal"]:
            bpy.context.window.screen = bpy.data.screens["A4B-UV Editing"]
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.context.window.screen = bpy.data.screens["A4B-Nodal"]
        return {'FINISHED'}
    
# Switch to layout "A4B-Painting"
class ClassLayoutPaint(bpy.types.Operator):
    """Switch to layout "A4B-Painting" """
    bl_idname = "class.layoutpaint"
    bl_label = "Class Layout Paint"
    
    def execute(self, context):
        layout = self.layout
        
        bpy.context.window.screen = bpy.data.screens["A4B-Painting"]
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}    
    
# Switch to layout "A4B-Scripting"
class ClassLayoutScripting(bpy.types.Operator):
    """Switch to layout "A4B-Scripting" """
    bl_idname = "class.layoutscripting"
    bl_label = "Class Layout Scripting"
    
    def execute(self, context):
        layout = self.layout
        
        bpy.context.window.screen = bpy.data.screens["A4B-Scripting"]
        return {'FINISHED'}

# Switch between layouts "A4B-Sculpt" & "A4B-Retopology"
class ClassLayoutSculpt(bpy.types.Operator):
    """Switch between A4B-Sculpt & A4B-Retopo"""
    bl_idname = "class.layoutsculpt"
    bl_label = "Class Layout Sculpt"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.screen == bpy.data.screens["A4B-Sculpt"] or bpy.context.object.mode == 'SCULPT':
            bpy.context.window.screen = bpy.data.screens["A4B-Retopology"]
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.context.window.screen = bpy.data.screens["A4B-Sculpt"]
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.sculpt.sculptmode_toggle()
        return {'FINISHED'}
 
# Switch between layouts "A4B-Video Sequence Editor" & "A4B-Motion Tracking"
class ClassLayoutVSE(bpy.types.Operator):
    """Switch between layouts "A4B-VSE" and "A4B-Motion Tracking" """
    bl_idname = "class.layoutvse"
    bl_label = "Class Layout VSE"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.screen == bpy.data.screens["A4B-Video Editing"]:
            bpy.context.window.screen = bpy.data.screens["A4B-Motion Tracking"]
        else:
            bpy.context.window.screen = bpy.data.screens["A4B-Video Editing"]
        return {'FINISHED'}

######################################################################################################################################
#                                                     Classes du Pie View                                                            #
######################################################################################################################################

# Classe pour changer de vue (3D view, Properties, node...)
class ViewMenu(bpy.types.Operator):
    """Menu to change the views"""
    bl_idname = "object.view_menu"
    bl_label = "View_Menu"
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.area.type=self.variable
        return {'FINISHED'}
    
# Save Incremental (Lapineige)
class SaveIncrementalLapineige(bpy.types.Operator):
    """Save Incremental (must "Save As" First, without "_updated_" )"""
    bl_idname = "file.lapi_save"
    bl_label = "Lapineige Save Incremental"
    bl_options = {"REGISTER"}
    
    def execute(self, context):
        f_path = bpy.data.filepath      
        if f_path.find("_updated_") != -1:
            str_nb = f_path.rpartition("_updated_")[-1].rpartition(".blend")[0]
            int_nb = int(str_nb)
            new_nb = str_nb.replace(str(int_nb),str(int_nb+1))   
            output = f_path.replace(str_nb,new_nb)
            
            i = 1
            while os.path.isfile(output):
                str_nb = f_path.rpartition("_updated_")[-1].rpartition(".blend")[0]
                i += 1
                new_nb = str_nb.replace(str(int_nb),str(int_nb+i))
                output = f_path.replace(str_nb,new_nb)
        else:
            output = f_path.rpartition(".blend")[0]+"_updated_001"+".blend"
        
        bpy.ops.wm.save_as_mainfile(filepath=output)
        self.report({'INFO'}, "File: {0} - Created at: {1}".format(output[len(bpy.path.abspath("//")):], output[:len(bpy.path.abspath("//"))]))
        return {'FINISHED'}
    
# Object Shading Flat
class TazTakoObjectShadingFlat(bpy.types.Operator):
    """Shading Object Flat"""
    bl_idname = "class.taztako_object_shading_flat"
    bl_label = "Shading Flat"
    
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.shade_flat()            
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_flat()
            bpy.ops.object.mode_set(mode = 'EDIT')
        elif bpy.context.object.mode == "SCULPT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_flat()
            bpy.ops.sculpt.sculptmode_toggle()
        elif bpy.context.object.mode == "VERTEX_PAINT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_flat()
            bpy.ops.paint.vertex_paint_toggle()
        elif bpy.context.object.mode == "TEXTURE_PAINT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_flat()
            bpy.ops.paint.texture_paint_toggle()
        elif bpy.context.object.mode == "WEIGHT_PAINT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_flat()
            bpy.ops.paint.weight_paint_toggle()
        return {'FINISHED'} 
    
# Object Shading Smooth
class TazTakoObjectShadingSmooth(bpy.types.Operator):
    """Shading Object Smooth"""
    bl_idname = "class.taztako_object_shading_smooth"
    bl_label = "Shading Smooth"
    
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.shade_smooth()            
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth()
            bpy.ops.object.mode_set(mode = 'EDIT')
        elif bpy.context.object.mode == "SCULPT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth()
            bpy.ops.sculpt.sculptmode_toggle()
        elif bpy.context.object.mode == "VERTEX_PAINT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth()
            bpy.ops.paint.vertex_paint_toggle()
        elif bpy.context.object.mode == "TEXTURE_PAINT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth()
            bpy.ops.paint.texture_paint_toggle()
        elif bpy.context.object.mode == "WEIGHT_PAINT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth()
            bpy.ops.paint.weight_paint_toggle()
        return {'FINISHED'} 
    
# Switch Painting Modes : Texture > Vertex > Weight
class ClassSwitchPaintingModes(bpy.types.Operator):
    """Switch between Painting Modes"""
    bl_idname = "class.switchpaintingmodes"
    bl_label = "Class Switch Painting Modes"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.object.mode == "TEXTURE_PAINT":
            bpy.ops.paint.vertex_paint_toggle()
        elif bpy.context.object.mode == "VERTEX_PAINT":
            bpy.ops.paint.weight_paint_toggle()
        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}
    
# Shading Variable (bbox, wireframe, solid, textured, rendered)
class ShadingVariable(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.shadingvariable"
    bl_label = ""
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True
              
    def execute(self, context):
        for screen in bpy.data.screens:
            for area in screen.areas:
                 for space in area.spaces:
                    print(space.type)
                    if space.type == 'VIEW_3D':
                        space.viewport_shade=self.variable     
        return {'FINISHED'}
    
# Switch Nodal : Shader > Compositing > Texture
class ClassSwitchNodal(bpy.types.Operator):
    """Switch between Shader & Compo"""
    bl_idname = "class.switchnodal"
    bl_label = "Class Switch Nodal"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.space_data.tree_type == 'ShaderNodeTree':
            bpy.context.space_data.tree_type = 'CompositorNodeTree'
        elif bpy.context.space_data.tree_type == 'CompositorNodeTree':
            bpy.context.space_data.tree_type = 'TextureNodeTree'
        else:
            bpy.context.space_data.tree_type = 'ShaderNodeTree'
        return {'FINISHED'}
    
# Switch Outliner / Properties
class ClassSwitchOutlinerProperties(bpy.types.Operator):
    """Switch between "Outliner" & "Properties" panels"""
    bl_idname = "class.switchoutlinerproperties"
    bl_label = "Class Switch Outliner Properties"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.context.area.type == 'OUTLINER':
            bpy.context.area.type = 'PROPERTIES'
        else:
            bpy.context.area.type = 'OUTLINER'
        return {'FINISHED'}
    
############################################################################################################################
#                                              Pie Menu - Ateliers (Ctrl bouton 5)                                         #
############################################################################################################################

class TazTakoPieLayout(Menu):
    bl_idname = "tazpie.layouts"
    bl_label = "CHOOSE YOUR ATELIER"
    
    def draw(self, context):
        layout = self.layout
        
        pie = layout.menu_pie()
        
        if not bpy.context.object:
            # 1 - Ouest
            pie.operator("class.layoutvse", text="Video Edit", icon='SEQ_SEQUENCER')
            # 2 - Est
            pie.operator("class.layoutscripting", text="Script", icon='CONSOLE')
                       
        else:
            # 1 - Ouest
            pie.operator("class.layoutedit", text="Scene > Edit", icon='EDITMODE_VEC_HLT')
            # 2 - Est
            pie.operator("class.layoutpaint", text="Painting", icon='TPAINT_HLT')
            # 3 - Sud
            pie.operator("class.layoutvse", text="Video Edit > Motion Track", icon='SEQ_SEQUENCER')
            # 4 - Nord
            pie.operator("class.layoutnodal", text="Nodal > UV", icon='MATERIAL')
            # 5 - Nord-Ouest
            pie.operator("class.layoutsculpt", text="Sculpt > Retopo", icon='SCULPTMODE_HLT')
            # 6 - Nord-Est
            pie.operator("class.layoutskin", text="Skin > Hair", icon='BONE_DATA')
            # 7 - Sud-Ouest
            pie.operator("class.layoutscripting", text="Script", icon='CONSOLE')
            # 8 - Sud-Est
            pie.operator("class.layoutanim", text="Anim > FX", icon='ANIM')
            
####################################################################################################################################################
#                                               Pie Menu Vew - Gestion affichage (bouton 5)                                                        #
####################################################################################################################################################

class TazTakoPieView(Menu):
    bl_idname = "tazpie.view"
    bl_label = "VIEW"
    
    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

# ---- Pie Menu Affichage - Vue 3D ----

        if bpy.context.area.type == 'VIEW_3D':
            if not bpy.context.object:
                # 1 - Ouest
                pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
            else:
                box = pie.split().column()
                row = box.row(align=True)
                row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')# nouvelle classe (Lapineige)
                row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
                # 2 - Est
                box = pie.split().column()
                row = box.row(align=True)
                row.operator("view3d.render_border", text="Render Border", icon='RENDER_REGION')
                row.operator("view3d.clear_render_border", text="Clear", icon='CANCEL')
                # 3 - Sud
                if bpy.context.object.mode == 'EDIT':# Overlays
                    box = pie.split().box().column()
                    box.label("Show Normals :")
                    box.prop(context.active_object.data, "show_normal_face", text="Face", icon='FACESEL')
                    box.prop(context.active_object.data, "show_normal_loop", text="Edge", icon='LOOPSEL')
                    box.prop(context.active_object.data, "show_normal_vertex", text="Vertex", icon='VERTEXSEL')
                    box.label("Show Overlays :")
                    box.prop(context.active_object.data, "show_edge_seams", text="Seams (UV)")
                    box.prop(context.active_object.data, "show_edge_sharp", text="Sharpness")
                    box.prop(context.active_object.data, "show_freestyle_edge_marks", text="Freestyle")
                    box.prop(context.active_object.data, "show_edge_crease", text="Crease (SubSurf)")
                    box.prop(context.active_object.data, "show_edge_bevel_weight", text="Bevel")
                    box.prop(context.active_object.data, "show_extra_edge_lenght", text="Lenght")
                elif bpy.context.object.mode == 'OBJECT':# Camera
                    box = pie.split().box().column()
                    box.label("Camera :")
                    if context.space_data.lock_camera:
                        box.prop(context.space_data, "lock_camera", icon = "LOCKED")
                    else:
                        box.prop(context.space_data, "lock_camera", icon = "UNLOCKED")
                    box.operator("view3d.camera_to_view_selected", text="Cam. to Selected", icon='CAMERA_DATA')
                    box.operator("view3d.camera_to_view", text="View to Cam.", icon = 'VISIBLE_IPO_ON')
                    box.operator("object.track_set", text="Cam. track to object (select 1st Cam, 2nd Object)", icon='CAMERA_DATA').type='TRACKTO'
                    box.operator("view3d.object_as_camera", text="Activate this Camera", icon='HAND')
                elif bpy.context.object.mode == "TEXTURE_PAINT" or bpy.context.object.mode == "VERTEX_PAINT" or bpy.context.object.mode == "WEIGHT_PAINT":# Painting Modes
                    pie.operator("class.switchpaintingmodes", text="Tex > Vert > Weight", icon='FILE_REFRESH')# nouvelle classe
                elif bpy.context.object.mode == "SCULPT":# Switch direct vers A4B-Retopo
                    pie.operator("class.layoutsculpt", text="> Retopo", icon='FILE_REFRESH')# nouvelle classe
                else:
                    box = pie.split().box().column()
                    box.label("Still in development", icon='INFO')
                # 4 - Nord
                box = pie.split().box().column()
                # Matcaps
                if context.space_data.use_matcap:
                    row = box.row(align=True)
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "01", text="", icon="MATCAP_01")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "02", text="", icon="MATCAP_02")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "03", text="", icon="MATCAP_03")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "04", text="", icon="MATCAP_04")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "05", text="", icon="MATCAP_05")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "06", text="", icon="MATCAP_06")
                    row = box.row(align=True)
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "07", text="", icon="MATCAP_07")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "08", text="", icon="MATCAP_08")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "09", text="", icon="MATCAP_09")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "10", text="", icon="MATCAP_10")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "11", text="", icon="MATCAP_11")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "12", text="", icon="MATCAP_12")
                    row = box.row(align=True)
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "13", text="", icon="MATCAP_13")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "14", text="", icon="MATCAP_14")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "15", text="", icon="MATCAP_15")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "16", text="", icon="MATCAP_16")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "17", text="", icon="MATCAP_17")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "18", text="", icon="MATCAP_18")
                    row = box.row(align=True)
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "19", text="", icon="MATCAP_19")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "20", text="", icon="MATCAP_20")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "21", text="", icon="MATCAP_21")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "22", text="", icon="MATCAP_22")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "23", text="", icon="MATCAP_23")
                    row.prop_enum(bpy.context.space_data, "matcap_icon", "24", text="", icon="MATCAP_24")
                # Shading Flat / Smooth & Enable Matcaps
                if bpy.context.object.mode == 'OBJECT' or bpy.context.object.mode == 'EDIT' or bpy.context.object.mode == 'SCULPT' or bpy.context.object.mode == 'POSE' or bpy.context.object.mode == 'PARTICLE_EDIT':
                    box.prop(context.space_data, "use_matcap", text="MatCaps", icon='TRIA_UP')
                # Shading
                row = box.row(align=True)
                row.operator("object.shadingvariable", icon="BBOX").variable="BOUNDBOX"
                row.operator("object.shadingvariable", icon="WIRE").variable="WIREFRAME"
                row.operator("object.shadingvariable", icon="SOLID").variable="SOLID"
                row.operator("object.shadingvariable", icon="POTATO").variable="TEXTURED"
                row.operator("object.shadingvariable", icon="MATERIAL").variable="MATERIAL"
                row.operator("object.shadingvariable", icon="SMOOTH").variable="RENDERED"
                row = box.row(align=True)
                row.operator("class.taztako_object_shading_flat", text="Flat")# nouvelle classe
                row.operator("class.taztako_object_shading_smooth", text="Smooth")# nouvelle classe
                # 5 - Nord-Ouest
                pie.operator("view3d.view_selected", text="Zoom Selected", icon='VIEWZOOM')
                # 6 - Nord-Est
                pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
                # 7 - Sud-Ouest
                pie.operator("view3d.walk", text="Walk Navigation (ZSQD)", icon='LOGIC')
                # 8 - Sud-Est
                pie.operator("view3d.localview", text="Toggle Isolate", icon="GHOST_ENABLED")
                                                                   
# ---- Pie Menu Affichage - Node Editor ----

        elif bpy.context.area.type == 'NODE_EDITOR':
            # 1 - Ouest
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')# nouvelle classe (Lapineige)
            row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 2 - Est
            pie.operator("node.view_all", text="View All Nodes", icon='NODETREE')
            # 3 - Sud
            pie.operator("class.switchnodal", text="Shaders > Compo > Tex.", icon='FILE_REFRESH')# nouvelle classe
            # 4 - Nord
            box = pie.split().box().column()
            box.label("Shading :")
            row = box.row(align=True)
            row.operator("object.shadingvariable", icon="BBOX").variable="BOUNDBOX"
            row.operator("object.shadingvariable", icon="WIRE").variable="WIREFRAME"
            row.operator("object.shadingvariable", icon="SOLID").variable="SOLID"
            row.operator("object.shadingvariable", icon="POTATO").variable="TEXTURED"
            row.operator("object.shadingvariable", icon="MATERIAL").variable="MATERIAL"
            row.operator("object.shadingvariable", icon="SMOOTH").variable="RENDERED"
            # 5 - Nord-Ouest
            pie.operator("node.view_selected", text="Zoom Node", icon='NODE_SEL')
            # 6 - Nord-Est
            pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
                        
# ---- Pie Menu Affichage - Image Editor ----

        elif bpy.context.area.type == 'IMAGE_EDITOR':
            # 1 - Ouest
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')# nouvelle classe (Lapineige)
            row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 2 - Est
            pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
            # 3 - Sud
            pie.operator("image.view_all", text="Fit Image", icon='IMAGE_COL').fit_view=True
            # 4 - Nord
            pie.prop(context.space_data.uv_editor, "show_stretch", text="Show Stretch UV (toggle)", icon='IPO_SINE')
            # 5 - Nord-Ouest
            pie.prop(context.space_data, "show_repeat", text="Repeat Image (toggle)", icon='MESH_GRID')
                        
                    
# ---- Pie Menu Affichage - Outliner ----

        elif bpy.context.area.type == 'OUTLINER':
            # 1 - Ouest
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')
            row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 2 - Est
            pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
            # 3 - Sud
            pie.operator("class.switchoutlinerproperties", text="> Properties", icon='FILE_REFRESH')# nouvelle classe
            # 4 - Nord
            pie.operator("outliner.show_active", text="Show Active Object", icon='VIEW3D')
                                
# ---- Pie Menu Affichage - Properties ----

        elif bpy.context.area.type == 'PROPERTIES':
            # 1 - Ouest
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')
            row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 2 - Est
            pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
            # 3 - Sud
            pie.operator("class.switchoutlinerproperties", text="> Outliner", icon='FILE_REFRESH')# nouvelle classe
            
# ---- Pie Menu Affichage - Anim ----

        elif bpy.context.area.type == 'TIMELINE' or bpy.context.area.type == 'GRAPH_EDITOR' or bpy.context.area.type == 'DOPESHEET_EDITOR' or bpy.context.area.type == 'NLA_EDITOR':      
            # 1 - Ouest
            pie.operator("object.view_menu", text="> Time Line", icon='TIME').variable="TIMELINE"
            # 2 - Est
            pie.operator("object.view_menu", text="> Dope Sheet", icon='ACTION').variable="DOPESHEET_EDITOR"
            # 3 - Sud
            pie.operator("object.view_menu", text="> Graph Editor", icon='IPO').variable="GRAPH_EDITOR"
            # 4 - Nord
            pie.operator("object.view_menu", text="> NLA Editor", icon='NLA').variable="NLA_EDITOR"            
            
# ---- Pie Menu Affichage - Text Editor ----

        elif bpy.context.area.type == 'TEXT_EDITOR':
            # 1 - Ouest
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')
            row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 2 - Est
            pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
            # 3 - Sud
            pie.operator("text.save", text="Save Script", icon='SAVE_COPY')
            # 4 - Nord
            pie.operator("text.properties", text="Properties Panel", icon='MENU_PANEL')
                                    
# ---- Pie Menu Affichage - Autres vues ----

        else:
            # 1 - Ouest
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("file.lapi_save", text="Update .blend (+ 1)", icon='RECOVER_LAST')
            row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 2 - Est
            pie.operator("wm.window_fullscreen_toggle", text="Blender Full Screen", icon="FULLSCREEN_ENTER")
                                                
######################################################################################################################################
#                                                       Pie Menu - Outils 1 (bouton 4)                                               #
######################################################################################################################################

class TazTakoPieTools1(Menu):
    bl_idname = "tazpie.tools1"
    bl_label = "TOOLS 1"
            
    def draw(self, context):
        layout = self.layout
        
        pie = layout.menu_pie()
    
# ---- Pie Menu Outils 1 - Vue 3D / Sans objet dans la scene ----

        if bpy.context.area.type == 'VIEW_3D':
            if not bpy.context.object:
                # 1 - Ouest
                pie.operator("wm.open_mainfile", text="Open", icon='FILE_FOLDER')
                # 2 - Est
                pie.menu("INFO_MT_file_open_recent", text="Recent...", icon='OPEN_RECENT')
                # 3 - Sud
                box = pie.split().box().column()
                box.label("Import Asset :")
                box.operator("wm.append", text="Append", icon='APPEND_BLEND')
                box.separator()
                box.operator("wm.link", text="Link", icon='LINK_BLEND')
                box.separator()
                box.operator("import_scene.obj", text=".obj", icon='MOD_WAVE')
                # 4 - Nord
                pie.menu("INFO_MT_add", text="Add...", icon='COLLAPSEMENU')
            
# ---- Pie Menu Outils 1 - Vue 3D / Layout Retopology ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Retopology"]:# pb: impossible en l'état actuel de sculpter, peindre, etc, sans changer de layout
                if bpy.context.object.mode == 'EDIT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Retopology (Edit-Mode) are still in development", icon='INFO') 
                    # 2 - Est
                    pie.operator("mesh.laprelax", text = "Lap Relax", icon = 'LATTICE_DATA')# nouvelle classe
                    # 3 - Sud
                    box = pie.split().box().column()
                    box.label("Normals :")
                    box.operator("mesh.normals_make_consistent", text="Recalculate", icon='SCRIPTWIN')
                    box.operator("mesh.flip_normals", text="Flip", icon='FILE_REFRESH')
                    # 4 - Nord
                    if tuple (bpy.context.tool_settings.mesh_select_mode) == (False, False, True):
                        pie.operator("mesh.tris_convert_to_quads", text="Tris -> Quads")                
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Retopology (other modes) are still in development", icon='INFO')
                    # 2 - Est
                    
                                                                
# ---- Pie Menu Outils 1 - Vue 3D / Layout UV Editing ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-UV Editing"]:# pb: impossible en l'état actuel de sculpter, peindre, etc, sans changer de layout
               if bpy.context.object.mode == 'EDIT':
                   # 1 - Ouest
                   box = pie.split().box().column()
                   box.label("Tools 1 for UV Editing (Edit-Mode) are still in development", icon='INFO')
               else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for UV Editing (other modes) are still in development", icon='INFO')
               
# ---- Pie Menu Outils 1 - Vue 3D / Layout Animation ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Animation"] :
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Animation (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Animation (other modes) are still in development", icon='INFO')
            
# ---- Pie Menu Outils 1 - Vue 3D / Layout FX ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-FX"]:
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for FX (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for FX (other modes) are still in development", icon='INFO')

# ---- Pie Menu Outils 1 - Vue 3D / Layout Skinning ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Skinning"]:
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Skinning (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Skinning (other modes) are still in development", icon='INFO')
            
# ---- Pie Menu Outils 1 - Vue 3D / Layout Hair ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Hair"]:
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Hair (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 1 for Hair (other modes) are still in development", icon='INFO')
                
# ---- Pie Menu Outils 1 - Vue 3D / Mode Object ----

            elif bpy.context.object.mode == 'OBJECT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.menu("MenuPivot", text="Pivot & 3D-Cursor...", icon='CURSOR')
                box.separator()
                box.operator("object.join", text="Join objects", icon='ROTATECENTER')
                box.operator("object.wazou_separate_looseparts", text="Separate Loose Parts", icon='ROTATECOLLECTION')# nouvelle classe
                box.separator()
                row = box.row(align=True)
                row.label("Duplicate :")
                row.operator("object.duplicate_move", text="Normal", icon='UNLINKED')
                row.operator("object.duplicate_move_linked", text="Linked", icon='LINKED')
                # 2 - Est
                box = pie.split().box().column()
                box.label("Import :")
                box.operator("wm.append", text="Append", icon='APPEND_BLEND')
                box.separator()
                row = box.row(align=True)
                row.operator("wm.link", text="Link", icon='LINK_BLEND')
                row.operator("object.proxy_make", text="Proxy", icon='EMPTY_DATA')
                box.separator()
                box.operator("import_scene.obj", text=".obj", icon='MOD_WAVE')
                # 3 - Sud
                box = pie.split().box().column()
                box.label("Select :")
                box.operator("view3d.select_border", text="Border (B)", icon='BORDER_RECT')
                box.operator("view3d.select_circle", text="Circle (C)", icon='INLINK')
                box.operator("view3d.select_lasso", text="Lasso (Ctrl)", icon='BORDER_LASSO')
                box.separator()
                box.operator("class.selectiontakorevert", text="Reverse", icon='FILE_REFRESH')
                box.separator()
                box.operator("object.select_linked", text="Same Material").type='MATERIAL'
                # 4 - Nord
                box = pie.split().box().column()
                box.menu("INFO_MT_add", text="Add...", icon='COLLAPSEMENU')
                box.menu("MenuModifiers", text="Modifiers...", icon='MODIFIER')

# ---- Pie Menu Outils 1 - Vue 3D / Mode Edit ----

            elif bpy.context.object.mode == 'EDIT':
                # 1 - Ouest
                pie.operator("mesh.loopcut_slide", text="Loop Cut")
                # 2 - Est
                pie.operator("mesh.inset", text="Inset")
                # 3 - Sud
                box = pie.split().box().column()
                box.label("Tools :")
                box.operator("view3d.edit_mesh_extrude_individual_move", text="Extrude (Individual)")
                box.operator("mesh.remove_doubles", text="Remove Doubles")
                box.operator("transform.shrink_fatten", text="Shrink Fatten (gonfler/réduire)")
                box.operator("transform.tosphere", text="To Sphere")
                box.operator("object.createhole", text="Hole")#nouvelle classe (Wazou ?)
                box.separator()
                box.menu("INFO_MT_mesh_add", text="Add...", icon='COLLAPSEMENU')
                box.menu("MenuModifiers", text="Modifiers...", icon='MODIFIER')
                # 4 - Nord
                pie.operator("mesh.bevel", text="Bevel")
                # 5 - Nord-Ouest
                pie.operator("mesh.subdivide", text="Subdivide")
                # 6 - Nord-Est
                pie.operator("mesh.knife_tool", text="Knife")
                # 7 - Sud-Ouest
                pie.operator("mesh.merge", text="Merge", icon='AUTOMERGE_ON')
                # 8 - Sud-Est
                pie.operator("transform.push_pull", text="Push Pull")
                
# ---- Pie Menu Outils 1 - Vue 3D / Mode Sculpt ----

            elif bpy.context.object.mode == 'SCULPT':
                # 1 - Ouest
                pie.operator("paint.brush_select", text='Toggle Draw / Brush', icon='BRUSH_SCULPT_DRAW').sculpt_tool='DRAW'# c'est un toggle avec FBrush :)
                # 2 - Est
                pie.operator("paint.brush_select", text='Nudge', icon='BRUSH_NUDGE').sculpt_tool= 'NUDGE'
                # 3 - Sud
                box = pie.split().box().column()
                box.operator("paint.brush_select", text='Flatten', icon='BRUSH_FLATTEN').sculpt_tool='FLATTEN'
                box.operator("paint.brush_select", text='Fill', icon='BRUSH_FILL').sculpt_tool='FILL'
                box.operator("paint.brush_select", text='Smooth', icon='BRUSH_SMOOTH').sculpt_tool= 'SMOOTH'
                box.operator("paint.brush_select", text='Mask', icon='BRUSH_MASK').sculpt_tool='MASK'
                box.operator("paint.brush_select", text='Pinch', icon='BRUSH_PINCH').sculpt_tool= 'PINCH'
                box.operator("paint.brush_select", text='Snakehook', icon='BRUSH_SNAKE_HOOK').sculpt_tool= 'SNAKE_HOOK'
                box.operator("paint.brush_select", text='Thumb', icon='BRUSH_THUMB').sculpt_tool= 'THUMB'
                box.operator("paint.brush_select", text='Layer', icon='BRUSH_LAYER').sculpt_tool= 'LAYER'
                box.operator("paint.brush_select", text='Claystrips', icon='BRUSH_CREASE').sculpt_tool= 'CLAY_STRIPS'
                box.operator("paint.brush_select", text='Scrape/Peaks', icon='BRUSH_SCRAPE').sculpt_tool= 'SCRAPE'
                box.label("Shortcuts :")
                row = box.split()
                row.label("Radius")
                row.label("F")
                row = box.split()
                row.label("Strenght")
                row.label("Shift F ")
                # 4 - Nord
                pie.operator("paint.brush_select", text="Clay", icon='BRUSH_CLAY').sculpt_tool='CLAY'
                # 5 - Nord-Ouest
                pie.operator("paint.brush_select", text='Inflate', icon='BRUSH_INFLATE').sculpt_tool='INFLATE'
                # 6 - Nord-Est
                pie.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'
                # 7 - Sud-Ouest
                pie.operator("paint.brush_select", text="Crease", icon='BRUSH_CREASE').sculpt_tool='CREASE'
                # 8 - Sud-Est
                pie.operator("paint.brush_select", text='Twist', icon='BRUSH_ROTATE').sculpt_tool= 'ROTATE'
                          
# ---- Pie Menu Outils 1 - Vue 3D / Texture Painting ----

            elif bpy.context.object.mode == 'TEXTURE_PAINT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 1 for Texture Painting are still in development", icon='INFO') 
            
# ---- Pie Menu Outils 1 - Vue 3D / Vertex Painting ----

            elif bpy.context.object.mode == 'VERTEX_PAINT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 1 for Vertex Painting are still in development", icon='INFO') 

# ---- Pie Menu Outils 1 - Vue 3D / Weight Painting ----

            elif bpy.context.object.mode == 'WEIGHT_PAINT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 1 for Weight Painting are still in development", icon='INFO')               
            
# ---- Pie Menu Outils 1 - Vue 3D / Layout Motion Tracking ----

            elif bpy.context.screen == bpy.data.screens["A4B-Motion Tracking"]:
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 1 for Motion Tracking are still in development", icon='INFO')
            
# ---- Pie Menu Outils 1 - Image Editor ----

        elif bpy.context.area.type == 'IMAGE_EDITOR':
            # 1 - Ouest
            pie.operator("uv.pin", text="Pin", icon='PINNED').clear=False
            # 2 - Est
            pie.operator("uv.pin", text="Un-Pin", icon='UNPINNED').clear=True
            # 3 - Sud
            box = pie.split().box().column()
            box.label("Sculpt UV :")
            box.operator("sculpt.sculpttoggle", text="Toggle")# nouvelle classe
            box.operator("sculpt.sculptrelax", text="Relax")# nouvelle classe
            box.operator("sculpt.sculptgrab", text="Grab")# nouvelle classe
            box.operator("sculpt.sculptpinch", text="Pinch")# nouvelle classe
            # 4 - Nord
            box = pie.split().box().column()
            box.label("Align :")
            box.operator("uv.align", text="X (column)", icon='ALIGN').axis = "ALIGN_X"
            box.operator("uv.align", text="Y (horizon)", icon='ALIGN').axis = "ALIGN_Y"
            # 5 - Nord-Ouest
            pie.operator("uv.minimize_stretch", text="Minimize Stretch")
            # 6 - Nord-Est
            pie.operator("uv.average_islands_scale", text="Average Islands Scale", icon='UV_ISLANDSEL')
                        
# ---- Pie Menu Outils 1 - Node Editor ----

        elif bpy.context.area.type == 'NODE_EDITOR':
            # 1 - Ouest
            box = pie.split().box().column()
            box.label("Help Preview Rendering :")
            box.operator("node.mute_toggle", text="Mute Node (M)", icon="GHOST_ENABLED")
            row = box.split()
            row.label("-NW- Connect to Viewer", icon="VISIBLE_IPO_ON")
            row.label("Ctrl Shift LMB")
            # 2 - Est
            box = pie.split().box().column()
            box.menu("NODE_MT_add", text="Add...")# appelle le menu Add
            if bpy.context.space_data.tree_type == 'ShaderNodeTree':
                box.menu("MenuShaders", text="Shaders...", icon='MATERIAL')
                box.menu("MenuDiversNode", text="Various...", icon='NODETREE')
                box.menu("MenuTextures", text="Textures...", icon='POTATO')
            elif bpy.context.space_data.tree_type == 'CompositorNodeTree':
                box.menu("MenuCompositing", text="Compositing...")
            # 3 - Sud
            box = pie.split().box().column()
            box.label("Organize :")
            box.operator("node.nw_align_nodes", text="-NW- Align Selected Nodes", icon='ALIGN')
            box.operator("node.add_node", text="Reroute", icon='OOPS').type='NodeReroute'
            row = box.row(align=True)
            row.label("Frame :", icon='SNAP_PEEL_OBJECT')
            row.operator("node.add_node", text="Create").type='NodeFrame'
            row.operator("node.nw_frame_selected", text="-NW- ...with selected Nodes")
            row = box.row(align=True)
            row.label("Group :", icon='LINENUMBERS_ON')
            row.operator("node.group_make", text="Create")
            row.operator("node.group_ungroup", text="Un-Group")
            # 4 - Nord
            box = pie.split().box().column()
            box.label("Manage Nodes :")
            box.operator("node.duplicate_move", text="Duplicate", icon="COLLAPSEMENU")
            box.operator("node.delete_reconnect", text="Delete with Reconnect", icon="CANCEL")
            box.operator("node.nw_merge_nodes", text="-NW- Merge Nodes")
            row = box.split()
            row.label("-NW- Switch Node type", icon='FILE_REFRESH')
            row.label("Shift S")
            row = box.split()
            row.label("Cut Link", icon='UNLINKED')
            row.label("Ctrl LMB")
      
# ---- Pie Menu Outils 1 - Text Editor ----

        elif bpy.context.area.type == 'TEXT_EDITOR':
            # 1 - Ouest
            pie.operator("text.unindent", text="Un-Indent", icon='BACK')
            # 2 - Est
            pie.operator("text.indent", text="Indent", icon='FORWARD')
            # 3 - Sud
            pie.operator("text.save", text="Save Script", icon='SAVE_COPY')
            # 4 - Nord
            pie.operator("text.start_find", text="Search...", icon='VIEWZOOM')
            # 5 - Nord-Ouest
            pie.operator("text.uncomment", text="Un-Comment", icon='NLA')
            # 6 - Nord-Est
            pie.operator("text.comment", text="Comment", icon='FONT_DATA')
            # 7 - Sud-Ouest
            pie.operator('text.select_line',icon='BORDER_RECT')

# ---- Pie Menu Outils 1 - Layout Video Editing ----

        elif bpy.context.area.type == 'SEQUENCE_EDITOR':
            # 1 - Ouest
            box = pie.split().box().column()
            box.label("Tools for Video Editing are still in development", icon='INFO') 
            
######################################################################################################################################
#                                                Pie Menu - Outils 2 (Ctrl + bouton 4)                                               #
######################################################################################################################################

class TazTakoPieTools2(Menu):
    bl_idname = "tazpie.tools2"
    bl_label = "TOOLS 2"
            
    def draw(self, context):
        layout = self.layout
        
        pie = layout.menu_pie()
    
# ---- Pie Menu Outils 2 - Vue 3D / Sans objet dans la scene ----

        if bpy.context.area.type == 'VIEW_3D':
            if not bpy.context.object:
                # 1 - Ouest
                pie.operator("wm.open_mainfile", text="Open", icon='FILE_FOLDER')
                # 2 - Est
                pie.menu("INFO_MT_file_open_recent", text="Recent...", icon='OPEN_RECENT')
                # 3 - Sud
                box = pie.split().box().column()
                box.label("Import Asset :")
                box.operator("wm.append", text="Append", icon='APPEND_BLEND')
                box.separator()
                box.operator("wm.link", text="Link", icon='LINK_BLEND')
                box.separator()
                box.operator("import_scene.obj", text=".obj", icon='MOD_WAVE')
                # 4 - Nord
                pie.menu("INFO_MT_add", text="Add...", icon='COLLAPSEMENU')
            
# ---- Pie Menu Outils 2 - Vue 3D / Layout Retopology ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Retopology"]:# pb: impossible en l'état actuel de sculpter, peindre, etc, sans changer de layout
                if bpy.context.object.mode == 'EDIT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Retopology (Edit-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Retopology (other modes) are still in development", icon='INFO')
                                                                
# ---- Pie Menu Outils 2 - Vue 3D / Layout UV Editing ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-UV Editing"]:# pb: impossible en l'état actuel de sculpter, peindre, etc, sans changer de layout
               if bpy.context.object.mode == 'EDIT':
                   # 1 - Ouest
                   box = pie.split().box().column()
                   box.label("Tools 2 for UV-Editing (Edit-Mode) are still in development", icon='INFO')
               else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for UV Editing (other modes) are still in development", icon='INFO')
                    
# ---- Pie Menu Outils 2 - Vue 3D / Layout Animation ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Animation"] :
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Animation (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Animation (other modes) are still in development", icon='INFO')
            
# ---- Pie Menu Outils 2 - Vue 3D / Layout FX ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-FX"]:
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for FX (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for FX (other modes) are still in development", icon='INFO')

# ---- Pie Menu Outils 2 - Vue 3D / Layout Skinning ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Skinning"]:
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Skinning (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Skinning (other modes) are still in development", icon='INFO')
            
# ---- Pie Menu Outils 2 - Vue 3D / Layout Hair ---- mis en tête de liste pour court-circuiter les pie génériques object/edit/sculpt/paint plus bas

            elif bpy.context.screen == bpy.data.screens["A4B-Hair"]:
                if bpy.context.object.mode == 'OBJECT':
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Hair (Object-Mode) are still in development", icon='INFO')
                else:
                    # 1 - Ouest
                    box = pie.split().box().column()
                    box.label("Tools 2 for Hair (other modes) are still in development", icon='INFO')
                    
# ---- Pie Menu Outils 2 - Vue 3D / Mode Object ----

            elif bpy.context.object.mode == 'OBJECT':
                # 1 - Ouest
                box = pie.split().box().column()
                row = box.row(align=True)
                row.label("Apply :")
                row.operator("object.applyrotation", text="Rot", icon='MAN_ROT')# nouvelle classe
                row.operator("object.applyscale", text="Scale", icon='MAN_SCALE')# nouvelle classe
                # 2 - Est
                box = pie.split().box().column()
                row = box.row(align=True)
                row.label("Clear :")
                row.operator("object.location_clear", text="Loc", icon='MAN_TRANS')
                row.operator("object.rotation_clear", text="Rot", icon='MAN_ROT')
                row.operator("object.scale_clear", text="Scale", icon='MAN_SCALE')
                # 3 - Sud
                box = pie.split().box().column()
                box.label("still in development", icon='INFO')
                # 4 - Nord
                box = pie.split().box().column()
                box.operator("object.parent_set", text="Parenter", icon='LOCKED')
                box.operator("object.parent_clear", text="Dé-Parenter", icon='UNLOCKED')

# ---- Pie Menu Outils 2 - Vue 3D / Edit Mode ----

            elif bpy.context.object.mode == 'EDIT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools :")
                box.menu("MenuAlign", text="Align...", icon='ALIGN')
                box.menu("MenuPivot", text="Pivot & 3D-Cursor...", icon='CURSOR')
                # 2 - Est
                box = pie.split().box().column()
                box.label("Mark Edges :")
                if tuple (bpy.context.tool_settings.mesh_select_mode) == (False, True, False):
                    row = box.row(align=True)
                    row.label("Freestyle :")
                    row.operator("mesh.mark_freestyle_edge", text="Mark", icon="FILE_TICK").clear=False
                    row.operator("mesh.mark_freestyle_edge", text="Un-Mark", icon="CANCEL").clear=True
                    row = box.row(align=True)
                    row.label("Seam (découpe UV):")
                    row.operator("mesh.mark_seam", text="Mark", icon="FILE_TICK").clear=False
                    row.operator("mesh.mark_seam", text="Un-Mark", icon="CANCEL").clear=True
                    row = box.row(align=True)
                    row.label("Lighting :")
                    row.operator("mesh.mark_sharp", text="Flat").clear=False
                    row.operator("mesh.mark_sharp", text="Smooth").clear=True
                    row = box.row(align=True)
                    row.label("SubSurf :")
                    row.operator("transform.edge_crease", text="Adjust Crease", icon="STYLUS_PRESSURE")
                    row = box.row(align=True)
                    row.label("Bevel :")
                    row.operator("transform.edge_bevelweight", text="Adjust Weight", icon="STYLUS_PRESSURE")
                else:
                    box.label("Please select edges to view this part")
                # 3 - Sud
                box = pie.split().box().column()
                if tuple (bpy.context.tool_settings.mesh_select_mode) == (False, True, False):
                    box.label("Select Edges similar to :")
                    box.operator("mesh.select_similar", text="Seam (UV)").type='SEAM'
                    box.operator("mesh.select_similar", text="Crease (SubSurf)").type='CREASE'
                    box.operator("mesh.select_similar", text="Sharpness (Shading)").type='SHARP'
                    box.operator("mesh.select_similar", text="FreeStyle").type='FREESTYLE_EDGE'
                    box.operator("mesh.select_similar", text="Lenght").type='LENGTH'
                elif tuple (bpy.context.tool_settings.mesh_select_mode) == (False, False, True):
                    box.label("Select Faces similar to :")
                    box.operator("mesh.select_similar", text="Material").type='MATERIAL'
                    box.operator("mesh.select_similar", text="Area").type='AREA'
                    box.operator("mesh.select_similar", text="Normal").type='NORMAL'
                else:
                    box.label("No applicable on vertices")
                # 4 - Nord
                box = pie.split().box().column()
                box.label("Select :")
                box.operator("view3d.select_border", text="Border (B)", icon='BORDER_RECT')
                box.operator("view3d.select_circle", text="Circle (C)", icon='INLINK')
                box.operator("view3d.select_lasso", text="Lasso (Ctrl)", icon='BORDER_LASSO')
                box.separator()
                box.operator("class.selectiontakorevert", text="Reverse", icon='FILE_REFRESH')
                box.separator()
                row = box.row(align=True)
                row.operator("mesh.select_more", text="More", icon='ZOOMIN')
                row.operator("mesh.select_less", text="Less", icon='ZOOMOUT')
                box.separator()
                row = box.row(align=True)
                row.operator("mesh.loop_multi_select", text="Loop").ring=False
                row.operator("mesh.loop_multi_select", text="Ring").ring=True
                
# ---- Pie Menu Outils 2 - Vue 3D / Mode Sculpt ----

            elif bpy.context.object.mode == 'SCULPT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 2 for Sculpt-Mode are still in development", icon='INFO')
               
# ---- Pie Menu Outils 2 - Vue 3D / Texture Painting ----

            elif bpy.context.object.mode == 'TEXTURE_PAINT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 2 for Texture Painting are still in development", icon='INFO') 
            
# ---- Pie Menu Outils 2 - Vue 3D / Vertex Painting ----

            elif bpy.context.object.mode == 'VERTEX_PAINT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 2 for Vertex Painting are still in development", icon='INFO') 

# ---- Pie Menu Outils 2 - Vue 3D / Weight Painting ----

            elif bpy.context.object.mode == 'WEIGHT_PAINT':
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 2 for Weight Painting are still in development", icon='INFO')               
            
# ---- Pie Menu Outils 2 - Vue 3D / Layout Motion Tracking ----

            elif bpy.context.screen == bpy.data.screens["A4B-Motion Tracking"]:
                # 1 - Ouest
                box = pie.split().box().column()
                box.label("Tools 2 for Motion Tracking are still in development", icon='INFO')
            
# ---- Pie Menu Outils 2 - Image Editor ----

        elif bpy.context.area.type == 'IMAGE_EDITOR':
            # 1 - Ouest
            box = pie.split().box().column()
            box.label("Tools 2 for Image Editor are still in development", icon='INFO')
                        
# ---- Pie Menu Outils 2 - Node Editor ----

        elif bpy.context.area.type == 'NODE_EDITOR':
            # 1 - Ouest
            box = pie.split().box().column()
            box.label("Tools 2 for Node Editor are still in development", icon='INFO')
      
# ---- Pie Menu Outils 2 - Text Editor ----

        elif bpy.context.area.type == 'TEXT_EDITOR':
            # 1 - Ouest
            box = pie.split().box().column()
            box.label("Tools 2 for Text Editor are still in development", icon='INFO')

# ---- Pie Menu Outils 2 - Layout Video Editing ----

        elif bpy.context.area.type == 'SEQUENCE_EDITOR':
            # 1 - Ouest
            box = pie.split().box().column()
            box.label("Tools 2 for Video Editing are still in development", icon='INFO')
            
######################################################################################################################################
#                                                       Menus                                                                        #
######################################################################################################################################

# Pivot & 3D-Cursor
class MenuPivot(bpy.types.Menu):
    bl_label = "Pivot"

    def draw(self, context):
        layout = self.layout

        layout.label("Move Pivot to :")
        layout.operator("object.pivotobottom", text="Bottom", icon='NLA_PUSHDOWN')# nouvelle classe
        layout.operator("object.pivot2cursor", text="3D-Cursor", icon='CURSOR')# nouvelle classe
        layout.operator("object.pivot2geometry", text="Mesh", icon='ROTATE')# nouvelle classe
        layout.operator("object.pivot2selection", text="Selected", icon='EDIT')# nouvelle classe
        layout.separator()
        layout.label("Move 3D Cursor to :")
        if not bpy.context.object:
            layout.operator("view3d.snap_cursor_to_center", text="Origin (0/0/0)", icon='WORLD_DATA')
        else:
            layout.operator("view3d.snap_cursor_to_selected", text="Selected", icon='VIEW3D')
            layout.operator("view3d.snap_cursor_to_active", text="Active", icon='OBJECT_DATA')
            layout.operator("view3d.snap_cursor_to_center", text="Origin (0/0/0)", icon='WORLD_DATA')
            layout.separator()
            layout.operator("view3d.snap_selected_to_cursor", text="Move Selection on 3D-Cursor", icon='ANIM_DATA')

# Align
class MenuAlign(bpy.types.Menu):
    bl_label = "Align"

    def draw(self, context):
        layout = self.layout

        layout.label("Align X :")
        layout.operator("align.x", text="All selected")# nouvelle classe (Wazou)
        layout.operator("align.2x0", text="to Zero (origin)")# nouvelle classe (Wazou)
        layout.operator("alignx.left", text="to West Side")# nouvelle classe (Wazou)
        layout.operator("alignx.right", text="to East Side")# nouvelle classe (Wazou)
        layout.separator()
        layout.label("Align Y :")
        layout.operator("align.y", text="All selected")# nouvelle classe (Wazou)
        layout.operator("align.2y0", text="to Zero (origin)")# nouvelle classe (Wazou)
        layout.operator("aligny.front", text="to South Side")# nouvelle classe (Wazou)
        layout.operator("aligny.back", text="to North Side")# nouvelle classe (Wazou)
        layout.separator()
        layout.label("Align Z :")
        layout.operator("align.z", text="All selected")# nouvelle classe (Wazou)
        layout.operator("align.2z0", text="to Zero (origin)")# nouvelle classe (Wazou)
        layout.operator("alignz.bottom", text="to Bottom")# nouvelle classe (Wazou)
        layout.operator("alignz.top", text="to Top")# nouvelle classe (Wazou)
                    
# Shaders
class MenuShaders(bpy.types.Menu):
    bl_label = "Shaders"

    def draw(self, context):
        layout = self.layout

        layout.operator("node.add_node", text="Mix", icon='GROUP_VCOL').type='ShaderNodeMixShader'   
        layout.operator("node.add_node", text="Add", icon='GROUP_VCOL').type='ShaderNodeAddShader'   
        layout.separator()
        layout.operator("node.add_node", text="Diffuse").type='ShaderNodeBsdfDiffuse'
        layout.operator("node.add_node", text="Glossy").type='ShaderNodeBsdfGlossy'
        layout.operator("node.add_node", text="Transparent (plastique)").type='ShaderNodeBsdfTransparent'
        layout.operator("node.add_node", text="Translucent (papier cigarette, simili SSS)").type='ShaderNodeBsdfTranslucent'
        layout.operator("node.add_node", text="Refraction (verre amputé de sa glossy)").type='ShaderNodeBsdfRefraction'
        layout.operator("node.add_node", text="Glass BSDF (verre)").type='ShaderNodeBsdfGlass'
        layout.operator("node.add_node", text="Anisotropic (métal poli)").type='ShaderNodeBsdfAnisotropic'
        layout.operator("node.add_node", text="SSS (peau, bougie)").type='ShaderNodeSubsurfaceScattering'
        layout.operator("node.add_node", text="Velvet (moquette ?)").type='ShaderNodeBsdfVelvet'
        layout.operator("node.add_node", text="Emission", icon='OUTLINER_OB_LAMP').type='ShaderNodeEmission'
        layout.operator("node.add_node", text="Hair", icon='HAIR').type='ShaderNodeBsdfHair'
        layout.separator()
        layout.operator("node.add_node", text="Hold Out (crée un alpha)", icon='MATCAP_24').type='ShaderNodeHoldout'
        layout.operator("node.add_node", text="Background", icon='WORLD').type='ShaderNodeBackground'
        
# Input-Output / Vector / Converter / Color
class MenuDiversNode(bpy.types.Menu):
    bl_label = "Input-Output / Vector / Converter / Color"

    def draw(self, context):
        layout = self.layout

        layout.operator("node.add_node", text="UV Map", icon='INFO').type='ShaderNodeUVMap'
        layout.operator("node.add_node", text="Normal Map", icon='MATCAP_23').type='ShaderNodeNormalMap'
        layout.operator("node.add_node", text="Bump").type='ShaderNodeBump'
        layout.operator("node.add_node", text="Attribute (pour les vertex color par ex)", icon='INFO').type='ShaderNodeAttribute'
        layout.operator("node.add_node", text="Texture Coordinate (generated window camera)", icon='TEXTURE_SHADED').type='ShaderNodeTexCoord'
        layout.operator("node.add_node", text="Mapping (loc rot scale)", icon='TEXTURE_SHADED').type='ShaderNodeMapping'
        layout.separator()
        layout.operator("node.add_node", text="Lamp Output", icon='OUTLINER_OB_LAMP').type='ShaderNodeOutputLamp'
        layout.operator("node.add_node", text="Fresnel (joue sur les bords de l'objet)").type='ShaderNodeFresnel'
        layout.operator("node.add_node", text="Layer Weight (fresnel en blend ou facing 0-1)").type='ShaderNodeLayerWeight'
        layout.separator()
        layout.operator("node.add_node", text="Math").type='ShaderNodeMath'
        layout.separator()
        layout.operator("node.add_node", text="RGB", icon='COLOR').type='ShaderNodeRGB'
        layout.operator("node.add_node", text="Color Ramp", icon='COLOR').type='ShaderNodeValToRGB'
        layout.operator("node.add_node", text="Mix RGB", icon='COLOR').type='ShaderNodeMixRGB'
        layout.operator("node.add_node", text="Hue Saturation", icon='RNDCURVE').type='ShaderNodeHueSaturation'
        layout.operator("node.add_node", text="Bright Contrast", icon='RNDCURVE').type='ShaderNodeBrightContrast'
        
# Textures
class MenuTextures(bpy.types.Menu):
    bl_label = "Textures"

    def draw(self, context):
        layout = self.layout

        layout.operator("node.add_node", text="Bitmap", icon='IMAGE_DATA').type='ShaderNodeTexImage'
        layout.operator("node.add_node", text="Environment", icon='WORLD').type='ShaderNodeTexEnvironment'
        layout.operator("node.add_node", text="Checker (damier)", icon='TEXTURE').type='ShaderNodeTexChecker'
        layout.operator("node.add_node", text="Gradient (type color ramp)", icon='IPO_EXPO').type='ShaderNodeTexGradient'
        layout.operator("node.add_node", text="Briques", icon='MOD_BUILD').type='ShaderNodeTexBrick'
        layout.operator("node.add_node", text="Wave").type='ShaderNodeTexWave'
        layout.operator("node.add_node", text="Voronoi").type='ShaderNodeTexVoronoi'
        layout.operator("node.add_node", text="Magic").type='ShaderNodeTexMagic'
        layout.operator("node.add_node", text="Noise").type='ShaderNodeTexNoise'
        layout.operator("node.add_node", text="Musgrave").type='ShaderNodeTexMusgrave'
        layout.operator("node.add_node", text="Sky").type='ShaderNodeTexSky'
                                
# Compositing
class MenuCompositing(bpy.types.Menu):
    bl_label = "Compositing"

    def draw(self, context):
        layout = self.layout

        layout.label("Input :")
        layout.operator("node.add_node", text="Bokeh Image", icon='IMAGE_COL').type='CompositorNodeBokehImage'
        layout.operator("node.add_node", text="Image", icon='IMAGE_COL').type='CompositorNodeImage'
        layout.operator("node.add_node", text="Mask", icon='MOD_MASK').type='CompositorNodeMask'
        layout.operator("node.add_node", text="Movie Clip", icon='FILE_MOVIE').type='CompositorNodeMovieClip'
        layout.operator("node.add_node", text="Render Layers", icon='RENDERLAYERS').type='CompositorNodeRLayers'
        layout.operator("node.add_node", text="RGB", icon='COLOR').type='CompositorNodeRGB'
        layout.operator("node.add_node", text="Texture").type='CompositorNodeTexture'
        layout.operator("node.add_node", text="Time").type='CompositorNodeTime'
        layout.operator("node.add_node", text="Track Position").type='CompositorNodeTrackPos'
        layout.operator("node.add_node", text="Value", icon='UI').type='CompositorNodeValue'
        layout.label("Output :")
        layout.operator("node.add_node", text="Composite", icon='SCENE').type='CompositorNodeComposite'
        layout.operator("node.add_node", text="File Output", icon='FILESEL').type='CompositorNodeOutputFile'
        layout.operator("node.add_node", text="Levels", icon='RNDCURVE').type='CompositorNodeLevels'
        layout.operator("node.add_node", text="Split-Viewer", icon='CAMERA_STEREO').type='CompositorNodeSplitViewer'
        layout.operator("node.add_node", text="Viewer", icon='RESTRICT_VIEW_OFF').type='CompositorNodeViewer'
        layout.label("Filter :")
        layout.operator("node.add_node", text="Dilate / Erode").type='CompositorNodeDilateErode'
        layout.operator("node.add_node", text="Despeckle").type='CompositorNodeDespeckle'
        layout.operator("node.add_node", text="Defocus").type='CompositorNodeDefocus'
        layout.operator("node.add_node", text="Filter").type='CompositorNodeFilter'
        layout.operator("node.add_node", text="Glare").type='CompositorNodeGlare'
        layout.operator("node.add_node", text="Inpaint").type='CompositorNodeInpaint'
        layout.operator("node.add_node", text="Pixelate").type='CompositorNodePixelate'
        layout.operator("node.add_node", text="Sun Beams").type='CompositorNodeSunBeams'
        layout.label("Blur :")
        layout.operator("node.add_node", text="Blur").type='CompositorNodeBlur'
        layout.operator("node.add_node", text="Bilateral").type='CompositorNodeBilateralblur'
        layout.operator("node.add_node", text="Bokeh").type='CompositorNodeBokehBlur'
        layout.operator("node.add_node", text="Directional").type='CompositorNodeDBlur'
        layout.operator("node.add_node", text="Vector").type='CompositorNodeVecBlur'
        layout.label("Vector :")
        layout.operator("node.add_node", text="Map Range").type='CompositorNodeMapRange'
        layout.operator("node.add_node", text="Map Value").type='CompositorNodeMapValue'
        layout.operator("node.add_node", text="Normal").type='CompositorNodeNormal'
        layout.operator("node.add_node", text="Normalize").type='CompositorNodeNormalize'
        layout.operator("node.add_node", text="Vector Curves").type='CompositorNodeCurveVec'
        layout.label("Distort :")
        layout.operator("node.add_node", text="Corner Pin").type='CompositorNodeCornerPin'
        layout.operator("node.add_node", text="Crop").type='CompositorNodeCrop'
        layout.operator("node.add_node", text="Displace").type='CompositorNodeDisplace'
        layout.operator("node.add_node", text="Flip").type='CompositorNodeFlip'
        layout.operator("node.add_node", text="Lens Distortion").type='CompositorNodeLensdist'
        layout.operator("node.add_node", text="Map UV").type='CompositorNodeMapUV'
        layout.operator("node.add_node", text="Movie Distortion").type='CompositorNodeMovieDistortion'
        layout.operator("node.add_node", text="Plane Track Deform").type='CompositorNodePlaneTrackDeform'
        layout.operator("node.add_node", text="Rotate").type='CompositorNodeRotate'
        layout.operator("node.add_node", text="Scale").type='CompositorNodeScale'
        layout.operator("node.add_node", text="Stabilize 2D").type='CompositorNodeStabilize'
        layout.operator("node.add_node", text="Transform").type='CompositorNodeTransform'
        layout.operator("node.add_node", text="Translate").type='CompositorNodeTranslate'
        layout.label("Matte :")
        layout.operator("node.add_node", text="Channel Key").type='CompositorNodeChannelMatte'
        layout.operator("node.add_node", text="Chroma Key").type='CompositorNodeChromaMatte'
        layout.operator("node.add_node", text="Color Key").type='CompositorNodeColorMatte'
        layout.operator("node.add_node", text="Color Spill").type='CompositorNodeColorSpill'
        layout.operator("node.add_node", text="Difference Key").type='CompositorNodeDiffMatte'
        layout.operator("node.add_node", text="Distance Key").type='CompositorNodeDistanceMatte'
        layout.operator("node.add_node", text="Keying").type='CompositorNodeKeying'
        layout.operator("node.add_node", text="Keying Screen").type='CompositorNodeKeyingScreen'
        layout.operator("node.add_node", text="Luminance Key").type='CompositorNodeLumaMatte'
        layout.label("Mask :")
        layout.operator("node.add_node", text="Box").type='CompositorNodeBoxMask'
        layout.operator("node.add_node", text="Double Edge").type='CompositorNodeDoubleEdgeMask'
        layout.operator("node.add_node", text="Ellipse").type='CompositorNodeEllipseMask'
        layout.label("Converter :")
        layout.operator("node.add_node", text="Alpha Convert", icon='IMAGE_ALPHA').type='CompositorNodePremulKey'
        layout.operator("node.add_node", text="Color Ramp", icon='COLOR').type='CompositorNodeValToRGB'
        layout.operator("node.add_node", text="ID Mask", icon='MOD_MASK').type='CompositorNodeIDMask'
        layout.operator("node.add_node", text="Math", icon='DISCLOSURE_TRI_RIGHT').type='CompositorNodeMath'
        layout.operator("node.add_node", text="RGB to BW", icon='IMAGEFILE').type='CompositorNodeRGBToBW'
        layout.operator("node.add_node", text="Set Alpha", icon='IMAGE_ALPHA').type='CompositorNodeSetAlpha'
        layout.label("Combine :")
        layout.operator("node.add_node", text="RGBA").type='CompositorNodeCombRGBA'
        layout.operator("node.add_node", text="HSVA").type='CompositorNodeCombHSVA'
        layout.operator("node.add_node", text="YUVA").type='CompositorNodeCombYUVA'
        layout.operator("node.add_node", text="YCbCrA").type='CompositorNodeCombYCCA'
        layout.label("Separate :")
        layout.operator("node.add_node", text="RGBA").type='CompositorNodeSepRGBA'
        layout.operator("node.add_node", text="HSVA").type='CompositorNodeSepHSVA'
        layout.operator("node.add_node", text="YUVA").type='CompositorNodeSepYUVA'
        layout.operator("node.add_node", text="YCbCrA").type='CompositorNodeSepYCCA'
        
# Modifiers
class MenuModifiers(bpy.types.Menu):
    bl_label = "Modifiers"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.modifier_add", text="Array", icon='MOD_ARRAY').type='ARRAY'
        layout.operator("object.modifier_add", text="Bevel", icon='MOD_BEVEL').type='BEVEL'
        layout.operator("object.modifier_add", text="Boolean", icon='MOD_BOOLEAN').type='BOOLEAN'
        layout.operator("object.modifier_add", text="Edge Split", icon='MOD_EDGESPLIT').type='EDGE_SPLIT'
        layout.operator("object.modifier_add", text="Mirror", icon='MOD_MIRROR').type='MIRROR'
        layout.operator("object.modifier_add", text="Solidify", icon='MOD_SOLIDIFY').type='SOLIDIFY'
        layout.operator("object.modifier_add", text="SubSurf", icon='MOD_SUBSURF').type='SUBSURF'
        layout.operator("object.modifier_add", text="Shrinkwrap", icon='MOD_SHRINKWRAP').type='SHRINKWRAP'
               
        
############################################################################################################################
#                                             Les Registers / KeyMap                                                       #
############################################################################################################################

addon_keymaps = []
       
def register():
    
    bpy.utils.register_class(TazTakoClicUserPrefs)
    # Classes Layouts
    bpy.utils.register_class(TazTakoScreenSetLayout)
    bpy.utils.register_class(ClassLayoutAnim)
    bpy.utils.register_class(ClassLayoutSkin)
    bpy.utils.register_class(ClassLayoutEdit)
    bpy.utils.register_class(ClassLayoutNodal)
    bpy.utils.register_class(ClassLayoutPaint)
    bpy.utils.register_class(ClassLayoutScripting)
    bpy.utils.register_class(ClassLayoutSculpt)
    bpy.utils.register_class(ClassLayoutVSE)
    # Pie-Menus
    bpy.utils.register_class(TazTakoPieLayout)
    bpy.utils.register_class(TazTakoPieView)
    bpy.utils.register_class(TazTakoPieTools1)
    bpy.utils.register_class(TazTakoPieTools2)
    # Classes Pie View
    bpy.utils.register_class(ViewMenu)
    bpy.utils.register_class(TazTakoObjectShadingFlat)
    bpy.utils.register_class(TazTakoObjectShadingSmooth)
    bpy.utils.register_class(ShadingVariable)
    bpy.utils.register_class(ClassSelectionTakoRevert)
    bpy.utils.register_class(ClassSwitchNodal)
    bpy.utils.register_class(ClassSwitchPaintingModes)
    bpy.utils.register_class(ClassSwitchOutlinerProperties)
    # Classes Pie Tools
    bpy.utils.register_class(AlignX)
    bpy.utils.register_class(AlignY)
    bpy.utils.register_class(AlignZ)
    bpy.utils.register_class(AlignToX0)
    bpy.utils.register_class(AlignToY0)
    bpy.utils.register_class(AlignToZ0)
    bpy.utils.register_class(AlignXLeft)
    bpy.utils.register_class(AlignXRight)
    bpy.utils.register_class(AlignYBack)
    bpy.utils.register_class(AlignYFront)
    bpy.utils.register_class(AlignZTop)
    bpy.utils.register_class(AlignZBottom)
    bpy.utils.register_class(LapRelax)
    bpy.utils.register_class(UVSculptGrab)
    bpy.utils.register_class(UVSculptRelax)
    bpy.utils.register_class(UVSculptPinch)
    bpy.utils.register_class(UVSculptToggle)
    bpy.utils.register_class(ApplyRotation)
    bpy.utils.register_class(ApplyScale)
    bpy.utils.register_class(CreateHole)
    bpy.utils.register_class(WazouSeparateLooseParts)
    bpy.utils.register_class(SaveIncrementalLapineige)
    bpy.utils.register_class(PivotToSelection)
    bpy.utils.register_class(PivotBottom)
    bpy.utils.register_class(PivotToGeometry)
    bpy.utils.register_class(PivotToCursor)
    # Menus
    bpy.utils.register_class(MenuPivot)
    bpy.utils.register_class(MenuAlign)
    bpy.utils.register_class(MenuShaders)
    bpy.utils.register_class(MenuDiversNode)
    bpy.utils.register_class(MenuTextures)
    bpy.utils.register_class(MenuCompositing)
    bpy.utils.register_class(MenuModifiers)
                               
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        
        # Pie Layouts - Ctrl + bouton 5
        km = wm.keyconfigs.addon.keymaps.new(name="Screen")
        kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON5MOUSE", "PRESS", ctrl=True).properties.name="tazpie.layouts"
        
        # Pie Affichage - bouton 5
        km = wm.keyconfigs.addon.keymaps.new(name="Screen")
        kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON5MOUSE", "PRESS").properties.name="tazpie.view"
        
        # Pie Tools - bouton 4
        km = wm.keyconfigs.addon.keymaps.new(name="Screen")
        kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON4MOUSE", "PRESS").properties.name="tazpie.tools1"
        
        # Pie Tools - Ctrl + bouton 4
        km = wm.keyconfigs.addon.keymaps.new(name="Screen")
        kmi = km.keymap_items.new("wm.call_menu_pie", "BUTTON4MOUSE", "PRESS", ctrl=True).properties.name="tazpie.tools2"
        
        #addon_keymaps.append(km)
        
def unregister():
    
    bpy.utils.unregister_class(TazTakoClicUserPrefs)
    # Layouts
    bpy.utils.unregister_class(TazTakoScreenSetLayout)
    bpy.utils.unregister_class(ClassLayoutAnim)
    bpy.utils.unregister_class(ClassLayoutSkin)
    bpy.utils.unregister_class(ClassLayoutEdit)
    bpy.utils.unregister_class(ClassLayoutNodal)
    bpy.utils.unregister_class(ClassLayoutPaint)
    bpy.utils.unregister_class(ClassLayoutScripting)
    bpy.utils.unregister_class(ClassLayoutSculpt)
    bpy.utils.unregister_class(ClassLayoutVSE)
    # Pie-Menus
    bpy.utils.unregister_class(TazTakoPieLayout)
    bpy.utils.unregister_class(TazTakoPieView)
    bpy.utils.unregister_class(TazTakoPieTools1)
    bpy.utils.unregister_class(TazTakoPieTools2)
    # Classes Pie View
    bpy.utils.unregister_class(ViewMenu)
    bpy.utils.unregister_class(TazTakoObjectShadingFlat)
    bpy.utils.unregister_class(TazTakoObjectShadingSmooth)
    bpy.utils.unregister_class(ShadingVariable)
    bpy.utils.unregister_class(ClassSelectionTakoRevert)
    bpy.utils.unregister_class(ClassSwitchNodal)
    bpy.utils.unregister_class(ClassSwitchPaintingModes)
    bpy.utils.unregister_class(ClassSwitchOutlinerProperties)
    # Classes Pie Tools
    bpy.utils.unregister_class(AlignX)
    bpy.utils.unregister_class(AlignY)
    bpy.utils.unregister_class(AlignZ)
    bpy.utils.unregister_class(AlignToX0)
    bpy.utils.unregister_class(AlignToY0)
    bpy.utils.unregister_class(AlignToZ0)
    bpy.utils.unregister_class(AlignXLeft)
    bpy.utils.unregister_class(AlignXRight)
    bpy.utils.unregister_class(AlignYBack)
    bpy.utils.unregister_class(AlignYFront)
    bpy.utils.unregister_class(AlignZTop)
    bpy.utils.unregister_class(AlignZBottom)
    bpy.utils.unregister_class(ApplyRotation)
    bpy.utils.unregister_class(ApplyScale)
    bpy.utils.unregister_class(CreateHole)
    bpy.utils.unregister_class(WazouSeparateLooseParts)
    bpy.utils.unregister_class(SaveIncrementalLapineige)
    bpy.utils.unregister_class(PivotToSelection)
    bpy.utils.unregister_class(PivotBottom)
    bpy.utils.unregister_class(PivotToGeometry)
    bpy.utils.unregister_class(PivotToCursor)
    bpy.utils.unregister_class(UVSculptGrab)
    bpy.utils.unregister_class(UVSculptRelax)
    bpy.utils.unregister_class(UVSculptPinch)
    bpy.utils.unregister_class(UVSculptToggle)
    bpy.utils.unregister_class(LapRelax)
    # Menus
    bpy.utils.unregister_class(MenuPivot)
    bpy.utils.unregister_class(MenuAlign)
    bpy.utils.unregister_class(MenuShaders)
    bpy.utils.unregister_class(MenuDiversNode)
    bpy.utils.unregister_class(MenuTextures)
    bpy.utils.unregister_class(MenuCompositing)
    bpy.utils.unregister_class(MenuModifiers)                    
        
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]
           
if __name__ == "__main__":
    register()
