import sys
sys.path.append("/home/ymstkz/.local/lib/python3.10/site-packages/cv2/")

from email.mime import image
from operator import truediv
import os
from xml.etree.ElementTree import tostring
import bpy 
import bpy_extras
from math import pi
from mathutils import Vector
import datetime
import cv2

###################################
### set parameters 
###################################

target_model = "traffic_light_red"
num_of_photo = 1
background_img_dir = "/media/slab/LAP_CHOL_DATA_2/contest_dataset/background/"
output_dir         = "/media/slab/LAP_CHOL_DATA_2/contest_dataset/ymstkz/"
dt                 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
out_dir            = output_dir + target_model + "/" + dt + "/"
out_label_dir      = out_dir + "label/"
out_image_dir      = out_dir + "image/" 
use_gpu            = True
debug              = True

# save renderrig image
def render(i):
    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render(filepath= out_image_dir + str(i).zfill(10) + ".png")

    return out_image_dir + str(i).zfill(10) + ".png"

def label(scene, obj, i):
    bound_box = [list(), list()]
    bound_box[0].clear
    bound_box[1].clear
    
    for i in range(0, 8):
        temp = obj.matrix_world @ Vector(obj.bound_box[i])
        bound_box[0].append(temp[0])
        bound_box[1].append(temp[2]) 

    left_up      = bpy_extras.object_utils.world_to_camera_view(scene, bpy.data.objects["Camera"], Vector((min(bound_box[0]), obj.bound_box[0][1], min(bound_box[1]))))
    right_bottom = bpy_extras.object_utils.world_to_camera_view(scene, bpy.data.objects["Camera"], Vector((max(bound_box[0]), obj.bound_box[0][1], max(bound_box[1]))))
    
    render_scale = scene.render.resolution_percentage / 100    
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),  
    )
    left_up = [round(left_up.x * render_size[0]), round(left_up.y * render_size[1])]
    right_bottom = [round(right_bottom.x * render_size[0]), round(right_bottom.y * render_size[1])]
    print("Left Up Coords:", left_up)
    print("Rgiht Buttom Coords:", right_bottom)
    
    return [left_up, right_bottom]

def main():
    if not os.path.exists(background_img_dir):
        print("couldn't find '" + background_img_dir + "' directiory.")
        exit()
    else:
        print("find " + background_img_dir + " !")
    
    if not os.path.exists(output_dir):
        print("couldn't find '" + output_dir + "' directiory.")
        exit()
    else:
        print("find " + output_dir + " !")


    if not os.path.exists(output_dir + target_model):
        os.mkdir(output_dir + target_model)
        
    os.mkdir(out_dir)   
    os.mkdir(out_label_dir)
    os.mkdir(out_image_dir)    
    
    # create project
    bpy.data.objects.remove(bpy.data.objects["Cube"])
    bpy.data.objects.remove(bpy.data.objects["Light"])
    scene = bpy.context.scene

    # add camera
    camera = bpy.data.objects["Camera"]
    camera.location = (0, -5, 0)
    camera.rotation_euler = (((pi * 90 / 180),0,0))
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    
    # add target model
    bpy.ops.wm.append(filepath="../models/" + target_model + ".blend", directory="../models/" + target_model + ".blend" + "/Collection/", filename=target_model)
    target = bpy.data.objects["traffic_light_body"]

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

    # create node tree for icluding background image to render image.
    links = node_tree.links
    back_image_node = nodes.new(type='CompositorNodeImage')
    back_image_node.image = bpy.data.images.load(background_img_dir + "0000000000.jpg", check_existing=False)

    scale_node = nodes.new(type="CompositorNodeScale")
    scale_node.space = "RENDER_SIZE"
    scale_node.frame_method = "CROP"
    alphao_node = nodes.new('CompositorNodeAlphaOver') 
    renderl_node = nodes.new('CompositorNodeRLayers')   
    comp_node = nodes.new('CompositorNodeComposite')   
    links.new(back_image_node.outputs[0], scale_node.inputs[0])  
    links.new(scale_node.outputs[0], alphao_node.inputs[1])
    links.new(renderl_node.outputs[0], alphao_node.inputs[2])
    links.new(alphao_node.outputs[0], comp_node.inputs[0])

    # scene background enviroment light
    node_tree = scene.world.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    env_node = nodes.new('ShaderNodeTexEnvironment')
    env_node.image = bpy.data.images.load(background_img_dir + "0000000000.jpg", check_existing=False)
    links.new(env_node.outputs["Color"], nodes[1].inputs["Color"])
    links.new(nodes[1].outputs["Background"], nodes[0].inputs["Surface"])

    # start create dataset
    for i in range(0, num_of_photo):
        #random_setting()
        img_path = render(int(i))
        cood = label(scene, target, int(i))

        if debug:
            img = cv2.imread(img_path)
            img = cv2.rectangle(img, (cood[0][0], cood[0][1]), (cood[1][0], cood[1][1]), (255, 0, 0), thickness=1, lineType=cv2.LINE_4)
            cv2.imwrite(filename="./out.png", img=img)

if __name__  == "__main__":
    main()
