# Test the function using the active object (which must be a camera)
# and the 3D cursor as the location to find.

import bpy
import bpy_extras

scene = bpy.context.scene
co = bpy.context.scene.cursor_location

target = bpy.data.objects["arrow"].location

co_2d = bpy_extras.object_utils.world_to_camera_view(scene, bpy.data.objects["Camera"], bpy.data.objects["arrow"].location)
print("2D Coords:", co_2d)

# If you want pixel coords
render_scale = scene.render.resolution_percentage / 100
render_size = (
    int(scene.render.resolution_x * render_scale),
    int(scene.render.resolution_y * render_scale),
)
print("Pixel Coords:", (
      round(co_2d.x * render_size[0]),
      round(co_2d.y * render_size[1]),
))
