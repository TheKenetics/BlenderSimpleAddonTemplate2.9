bl_info = {
	"name": "Name",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (2, 80, 0),
	"location": "View3D > Toolshelf > Add Objects",
	"description": "Description",
	"warning": "",
	"wiki_url": "",
	"category": "Add Mesh"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences

"""
General Notes to Self
list(scene.somethingbig) - To see arrays in console

##Props
options = {
	"HIDDEN", # Hidden from UI, good for operators
	"SKIP_SAVE", # This prop is not saved in presets
	"ANIMATABLE",
	"LIBRARY_EDITABLE", # This prop can edited from linked instances (changes not saved)
	"PROPORTIONAL", # 
	"TEXTEDIT_UPDATE"
}

#Number
min, max, soft_min, soft_max
unit = "LENGTH", "AREA", "VOLUME", "ROTATION", "TIME", "VELOCITY", "ACCELERATION", "MASS", "CAMERA", "POWER"
subtype = "PIXEL", "UNSIGNED", "PERCENTAGE", "FACTOR", "ANGLE", "TIME", "DISTANCE", "DISTANCE_CAMERA"
"POWER", "TEMPERATURE"

#Float
precision = 3 # display precision
subtype = ""

#XVector
size = 3
subtype = "COLOR" , "TRANSLATION", "DIRECTION", "VELOCITY", "ACCELERATION", "MATRIX", "EULER"
"QUATERNION", "AXISANGLE", "XYZ", "XYZ_LENGTH", "COLOR_GAMMA", "COORDINATES", "LAYER"
"LAYER_MEMBER"

#String
subtype = "DIR_PATH", "FILE_PATH", "FILE_NAME", "BYTE_STRING", "PASSWORD"

#Enum
Dynamic
def get_enum_items(self, context):
	enum_list = []
	
	for obj in context.selected_objects:
		enum_list.append( (obj.name, obj.name, "") )
	
	return enum_list
obj_name : EnumProperty(items=get_enum_items, name="Object Name")
Static
obj_name : EnumProperty(
	items=[
		("ITEM","Item Name", "Item Description", "UI_ICON", 0),
		("ITEM2","Item Name2", "Item Description", "UI_ICON", 1)
	],
	name="Object Name",
	description=""
)

##Collections
context.scene.collection - Master Scene collection
context.collection - Active Collection
collection.all_objects - all objects in this and child collections
collection.objects - objects in this collection
collection.children - child collections
collection.children.link(collection2) - link collection2 as child of collection
	will throw error if already in collection
collection.children.unlink(collection2) - unlink collection2 as child of collection
collection.objects.link(obj) - link object to collection
collection.objects.unlink(obj) - unlink object

##Window
context.area.type - Type of area

Window Manager
context.window_manager

"""

## Helper Functions
def get_addon_preferences():
	return bpy.context.preferences.addons[__package__].preferences


## Structs
#class SA_Settings(PropertyGroup):
#	pass


## Operators
"""
Class and bl_idname Names
[A-Z][A-Z0-9]*_{ABBREV}_[A-Za-z0-9_]+
Abbrev:
_HT_ Header
_MT_ Menu
_OT_ Operator
_PT_ Panel
_UL_ UIList
Ex:
Classname = ADDONABBREVIATION_OT_something
idname = addonabbreviation.something

Show messages
self.report({"INFO", "WARNING", "ERROR"}, "Message")
"""
class SA_OT_simple_operator(Operator):
	"""Tooltip"""
	bl_idname = "sa.simple_operator"
	bl_label = "Simple Object Operator"
	"""
		REGISTER - Display in info window and support redo toolbar panel
		UNDO - Push an undo event, needed for operator redo
			Crashes blender if adding a modifier to existing object then redo?
		BLOCKING - Block anthing else from moving the cursor
		MACRO - ?
		GRAB_CURSOR - Enables wrapping when continuous grab is enabled
		GRAB_CURSOR_X
		GRAB_CURSOR_Y
		BLOCKING - Enables wrapping when continuous grab is enabled
		PRESET - Display a preset button with operator settings
		INTERNAL - Removes operator from search results
	"""
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		# poll is called alot if operator is in ui (button), so try to keep it short and simple
		# you can put more complex checks at beginning of execute or invoke, when operator actually runs
		return context.active_object

	# Dialog invoke
	#def invoke(self, context, event):
	#	return context.window_manager.invoke_props_dialog(self)

	# Modal Invoke
	#def invoke(self, context, event):
	#	# Start modal operation
	#	context.window_manager.modal_handler_add(self)
	#	return {"RUNNING_MODAL"}

	#def modal(self, context: bpy.types.Context, event:bpy.types.Event):
	#	print(f"Type: {event.type}, Value: {event.value}")
	#	# if cancel
	#	if event.type in {"RIGHTMOUSE", "ESC"}:
	#		return {"CANCELLED"}
	#	elif event.type == "MOUSEMOVE":
	#		self.change += (event.mouse_x - event.mouse_prev_x)
	#	print(f"{event.type} {event.value}")
		
	#	return {"RUNNING_MODAL"}

	def execute(self, context):
		
		"""
		Return Types
		FINISHED - Confirm operation and finish
		CANCELLED - Undo operation and finish
		RUNNING_MODAL - Call modal() next
		PASS_THROUGH - Do nothing and pass event on
		INTERFACE - Handled but not executed
		"""
		return {'FINISHED'}


## UI
class SA_PT_hello_world_panel(Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Hello World Panel"
	bl_idname = "OBJECT_PT_hello"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "object"
	#object, objectmode, mesh_edit, curve_edit, render, output

	def draw(self, context):
		layout = self.layout
		# layout.use_property_split = True
		# always add None checks when getting active items
		obj = context.object

		# items added to layout usually go from top to bottom
		# cols create a vertical box - col = layout.col(align=True)
		# rows create a horizontal box - row = layout.row(align=True)
		layout.label(text=f"Active object is: {obj.name}", icon="WORLD_DATA")
		layout.prop(obj, "name")

		# create a column layout that is more tightly space together
		col = layout.col(align=True)
		col.operator("mesh.primitive_cube_add")
		# next operator will be closer to first if you use align=True
		# Use OperatorClassName.bl_idname when adding buttons for operators that you created
		# operator() returns an OperatorProperties obj that you can use to change defaults for that button's operator
		col.operator("mesh.primitive_cube_add")
		
		# create a small checkbox next to something
		#row = layout.row(align=True)
		#row.prop(settings, "bool", text="", icon="ICON")
		#row.prop(settings, "prop")

		# create vertical box
		#box = layout.box()
		
		# split = layout.split()
		# left col
		# col = split.col()
		# ...
		# right col
		# col = split.col()
		
		
		#layout.separator(factor=1)

## Append to UI Helper Functions
# to get menu class name, hover over menu in Blender. Name is like VIEW3D_MT_add
# menus are listed in bpy.types
#def draw_func(self, context):
#	layout = self.layout
#


## Preferences
class SA_addon_preferences(AddonPreferences):
	bl_idname = __package__
	
	# Properties
	show_mini_manual : BoolProperty(name="Show Mini Manual", default=False)

	def draw(self, context):
		layout = self.layout
		
		layout.prop(self, "show_mini_manual", toggle=True)
		
		if self.show_mini_manual:
			layout.label(text="Topic", icon="DOT")
			layout.label(text="Details",icon="THREE_DOTS")


## Register
classes = (
	SA_OT_simple_operator,
	SA_PT_hello_world_panel
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	## Add Custom Properties
	#bpy.Types.WindowManager.something = IntProperty() # to not save things with blend file
	#bpy.Types.Scene.something = IntProperty()
	
	## Append to UI
	# bpy.types.CLASS.append(helper_func)

def unregister():
	## Remove from UI
	# bpy.types.CLASS.remove(helper_func)
	
	## Remove Custom Properties
	#del bpy.Types.Scene.something
	#del bpy.Types.WindowManager.something
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
