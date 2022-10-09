from operator import truediv
from xml.etree.ElementTree import tostring
import bpy 
from math import pi
import time

###################################
### set parameters 
###################################

target_model = "trafic_light"
background_img_dir = "/media/slab/LAP_CHOL_DATA_2/contest_dataset/background/"
output_dir         = "/media/slab/LAP_CHOL_DATA_2/contest_dataset/dataset/"
use_gpu      = True


# save renderrig image
def render(i):
    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render(filepath= output_dir + tostring(i) + ".jpg")


def main():
    # create / save project
    bpy.data.objects.remove(bpy.data.objects["Cube"])
    bpy.data.objects.remove(bpy.data.objects["Light"])

    scene = bpy.context.scene

    # add camera
    camera = bpy.data.objects["Camera"]
    camera.location = (0, -200, 0)
    camera.rotation_euler = (((pi * 90 / 180),0,0))
    camera.data.clip_end = 200


    # add target model
    bpy.ops.import_scene.fbx(filepath="../models/"+ target_model +".fbx")

    # check render engine
    if use_gpu:
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'
        scene.render.film_transparent = True
    
    scene.use_nodes = True
    node_tree = scene.node_tree
    nodes = node_tree.nodes
    for n in nodes:
        nodes.remove(n)

    links = node_tree.links
    image_node = nodes.new(type='CompositorNodeImage')
    image_node.image = bpy.data.images.load(background_img_dir + "0000000001.jpg", check_existing=False)

    scale_node = nodes.new(type="CompositorNodeScale")
    scale_node.space = "RENDER_SIZE"
    scale_node.frame_method = "CROP"
    links.new(image_node.outputs[0], scale_node.inputs[0])
    
    alphao_node = nodes.new('CompositorNodeAlphaOver')   
    links.new(scale_node.outputs[0], alphao_node.inputs[1])

    renderl_node = nodes.new('CompositorNodeRLayers')   
    links.new(renderl_node.outputs[0], alphao_node.inputs[2])

    comp_node = nodes.new('CompositorNodeComposite')   
    links.new(alphao_node.outputs[0], comp_node.inputs[0])
    # bpy.context.space_data.params.filename = "photo.blend"

if __name__  == "__main__":
    main()
