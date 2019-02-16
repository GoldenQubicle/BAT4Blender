import bpy

for ob in bpy.context.collection.objects:
	print(ob.name)