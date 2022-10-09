import sys
sys.path.append("/home/ymstkz/.local/lib/python3.10/site-packages/cv2/")

from email.mime import image
from operator import truediv
import os
from xml.etree.ElementTree import tostring
import bpy 
import random
import bpy_extras
from math import pi
from mathutils import Vector
import datetime
import cv2
import time

###################################
### set parameters 
###################################

target_model = "traffic_light_red"
num_of_photo = 0
background_img_dir = "/media/slab/LAP_CHOL_DATA_2/contest_dataset/background/"
output_dir         = "/media/slab/LAP_CHOL_DATA_2/contest_dataset/ymstkz/"
dt                 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
out_dir            = output_dir + target_model + "/" + dt + "/"
out_label_dir      = out_dir + "label/"
out_image_dir      = out_dir + "image/" 
digit              = 10
use_gpu            = True
debug              = True
resolution_x       = 1280
resolution_y       = 720

# save renderrig image
def render(i):
    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render(filepath= out_image_dir + str(i).zfill(digit) + ".png")
    return out_image_dir + str(i).zfill(10) + ".png"

def label(scene, obj, i):
    bound_box = [list(), list()]
    
    for i in range(0, 8):
        temp = obj.matrix_world @ Vector(obj.bound_box[i])
        temp = bpy_extras.object_utils.world_to_camera_view(scene, bpy.data.objects["Camera"], temp)
        bound_box[0].append(temp[0])
        bound_box[1].append(temp[1])

    render_scale = scene.render.resolution_percentage / 100

    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),  
    )
    left_up = [round(max(bound_box[0]) * render_size[0]), round(min(bound_box[1]) * render_size[1])]
    right_bottom = [round(min(bound_box[0]) * render_size[0]), round(max(bound_box[1]) * render_size[1])]
    print("Left Up Coords:", left_up)
    print("Rgiht Buttom Coords:", right_bottom)
    
    return [left_up, right_bottom]

def random_setting(target):
    scale = random.uniform(0.5, 1.0)
    location = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]
    rotate = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]
    bpy.data.objects["traffic_light_red"].scale[0]            = scale
    bpy.data.objects["traffic_light_red"].scale[1]            = scale
    bpy.data.objects["traffic_light_red"].scale[2]            = scale
    bpy.data.objects["traffic_light_red"].location[0]         = location[0]
    bpy.data.objects["traffic_light_red"].location[2]         = location[1]
    bpy.data.objects["traffic_light_red"].rotation_euler[1]   = rotate[1]
    bpy.data.objects["traffic_light_red"].rotation_euler[2]   = rotate[0]

    # lighting
    bpy.data.materials["traffic_light_red"].node_tree.nodes["Principled BSDF"].inputs[20].default_value = random.uniform(0, 20) # housha
    bpy.data.materials["traffic_light_red"].node_tree.nodes["カラーランプ"].color_ramp.elements[1].color = (1, 0.0192237, 0, 1) # RGBA
    bpy.data.materials["traffic_light_red"].node_tree.nodes["カラーランプ"].color_ramp.elements[1].color = (1, 0.0192237, 0, 1) # RGBA

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
    camera.location = (0, -3, 0)
    camera.rotation_euler = (((pi * 90 / 180),0,0))
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    
    # add target model
    bpy.ops.wm.append(filepath="../models/" + target_model + ".blend", directory="../models/" + target_model + ".blend" + "/Collection/", filename=target_model)

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
    links.new(env_node.outputs["Color"], nodes[1].inputs["Color"])
    links.new(nodes[1].outputs["Background"], nodes[0].inputs["Surface"])
    
    back_image_node.image = bpy.data.images.load(background_img_dir  + str(0).zfill(digit) + ".jpg", check_existing=False)
    env_node.image = bpy.data.images.load(background_img_dir + str(0).zfill(digit) + ".jpg", check_existing=False)
    target = bpy.data.objects["traffic_light_body"]

    # start create dataset
    for i in range(0, num_of_photo):
        back_image_node.image = bpy.data.images.load(background_img_dir  + str(i).zfill(digit) + ".jpg", check_existing=False)
        env_node.image = bpy.data.images.load(background_img_dir + str(i).zfill(digit) + ".jpg", check_existing=False)
        
        random_setting(target)
        img_path = render(int(i))
        cood = label(scene, target, int(i))

        if cood[0][0] > resolution_x or cood[0][0] < 0: 
            i-=1
            continue
        if cood[1][0] > resolution_x or cood[1][0] < 0:
            i-=1
            continue 
        if cood[0][1] > resolution_y or cood[0][1] < 0:
            i-=1
            continue
        if cood[1][1] > resolution_y or cood[1][1] < 0: 
            i-=1
            continue

        if debug:
            img = cv2.imread(img_path)
            img = cv2.rectangle(img, (cood[0][0], resolution_y-cood[0][1]), (cood[1][0], resolution_y-cood[1][1]), (255, 0, 0), thickness=1, lineType=cv2.LINE_4)
            img = cv2.circle(img, (cood[0][0], resolution_y-cood[0][1]), 10, (0, 255, 0))
            img = cv2.circle(img, (cood[1][0], resolution_y-cood[1][1]), 10, (0, 255, 0))
            cv2.imwrite(filename="./out.png", img=img)

if __name__  == "__main__":
    main()
