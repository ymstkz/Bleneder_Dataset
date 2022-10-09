import random
import bpy
import time
from mathutils import Vector
            
for i in range(1, 0):
    # 原点を移動
    # カメラ座標系での中心 : (x, z) = (-128, -72) 
    # 範囲 : y = -120, x = {-43 ~ -212}, z = {-24, -118}
    bpy.context.scene.cursor.location[0] = -120
    bpy.context.scene.cursor.location[1] = random.uniform(-47, -208)
    bpy.context.scene.cursor.location[2] = random.uniform(-28, -100)
        
    # rotation
    rotate[0] = random.uniform(0, 0.87)
    rotate[1] = random.uniform(-0.87, 0.87)
    
    bpy.data.objects["light_red"].rotation_euler[1]   = rotate[0]
    bpy.data.objects["light_red"].rotation_euler[2]   = rotate[1]
    bpy.data.objects["light_body"].rotation_euler[1]  = rotate[0]
    bpy.data.objects["light_body"].rotation_euler[2]  = rotate[1]
    bpy.data.objects["light_bar"].rotation_euler[1]   = rotate[0]
    bpy.data.objects["light_bar"].rotation_euler[2]   = rotate[1]
    bpy.data.objects["light_point"].rotation_euler[1] = rotate[0]
    bpy.data.objects["light_point"].rotation_euler[2] = rotate[1]
    
    # Scaling 
    scale = random.uniform(0.3, 1.0)
    bpy.data.objects["light_body"].scale[0]  = light_body[0] * scale
    bpy.data.objects["light_body"].scale[1]  = light_body[1] * scale
    bpy.data.objects["light_body"].scale[2]  = light_body[2] * scale
    bpy.data.objects["light_bar"].scale[0]   = light_bar[0] * scale
    bpy.data.objects["light_bar"].scale[1]   = light_bar[1] * scale
    bpy.data.objects["light_bar"].scale[2]   = light_bar[2] * scale
    bpy.data.objects["light_red"].scale[0]   = light_red[0] * scale
    bpy.data.objects["light_red"].scale[1]   = light_red[1] * scale
    bpy.data.objects["light_red"].scale[2]   = light_red[2] * scale
    bpy.data.objects["light_point"].scale[0] = light_point[0] * scale
    bpy.data.objects["light_point"].scale[1] = light_point[1] * scale
    bpy.data.objects["light_point"].scale[2] = light_point[2] * scale
    
    # moving 
    bpy.data.objects["light_body"].location[0] = bpy.context.scene.cursor.location[0]
    bpy.data.objects["light_body"].location[1] = bpy.context.scene.cursor.location[1]
    bpy.data.objects["light_body"].location[2] = bpy.context.scene.cursor.location[2]
    bpy.data.objects["light_bar"].location[0] = bpy.context.scene.cursor.location[0]
    bpy.data.objects["light_bar"].location[1] = bpy.context.scene.cursor.location[1]
    bpy.data.objects["light_bar"].location[2] = bpy.context.scene.cursor.location[2]
    bpy.data.objects["light_red"].location[0] = bpy.context.scene.cursor.location[0]
    bpy.data.objects["light_red"].location[1] = bpy.context.scene.cursor.location[1]
    bpy.data.objects["light_red"].location[2] = bpy.context.scene.cursor.location[2]
    bpy.data.objects["light_point"].location[0] = bpy.context.scene.cursor.location[0]
    bpy.data.objects["light_point"].location[1] = bpy.context.scene.cursor.location[1]
    bpy.data.objects["light_point"].location[2] = bpy.context.scene.cursor.location[2]
    
    # adaptive light
    bpy.data.materials["light_red"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = random.randint(40, 150) * scale
    bpy.data.materials["light_red"].node_tree.nodes["Mapping"].inputs[3].default_value[0] = random.uniform(0.8, 1.1)
         
    # random background light
    #bpy.data.objects["ceiling_light"].data.energy = random1.randint(1300000)
    
    # 背景を変更
    bpy.data.materials["background"].node_tree.nodes["Image Texture.001"].image_user.frame_start = i
    
    # 画像を保存
    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render(filepath="/Users/ymstkz/workspace/lab/design_contest/trafic_light/dataset/" + str(i) + ".jpg")


# Let's try, Draw BB

bound_box = [list(), list()]
bound_box[0].clear
bound_box[1].clear

target = bpy.data.objects["arrow"]

for j in range(0, 8):
    temp = target.matrix_world @ Vector(target.bound_box[j])
    bound_box[0].append(temp[1])
    bound_box[1].append(temp[2])
    
bpy.data.objects["right_bottom"].location[1] = min(bound_box[0])
bpy.data.objects["right_bottom"].location[2] = min(bound_box[1])
bpy.data.objects["left_up"].location[1] = max(bound_box[0])
bpy.data.objects["left_up"].location[2] = max(bound_box[1]) 

bpy.data.objects["right_bottom"].location[0] = target.location[0]
bpy.data.objects["left_up"].location[0] = target.location[0]

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        matrix = area.spaces.active.region_3d.perspective_matrix
        
matrix = bpy.data.screens[0].areas[0].spaces[0]

a = Vector(
        (bpy.data.objects["right_bottom"].location[0],
        bpy.data.objects["right_bottom"].location[1], 
        bpy.data.objects["right_bottom"].location[2],
        0))
        
b = matrix @ a

#bpy.data.objects["right_bottom"].location[0] = b[0]
#bpy.data.objects["right_bottom"].location[1] = b[1]
#bpy.data.objects["right_bottom"].location[2] = b[2]

print(b)
print(a)

#bpy.data.materials["light_blue"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
#bpy.data.materiaasls["light_blue"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 50
#bpy.data.materials["light_yellow"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
#bpy.data.materials["light_yellow"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 50
#bpy.data.materials["light_red"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0
#bpy.data.materials["light_red"].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 50

# 3D 原点をカメラ中心に移動
#bpy.context.scene.cursor.location[0] = -128
#bpy.context.scene.cursor.location[1] = -120
#bpy.context.scene.cursor.location[2] = -72


# bouding box 
# bpy.data.objects["light_body"].bound_box
# bpy.context.scene.cursor.location = bpy.data.objects["light_body"].matrix_world @ Vector(bpy.data.objects["light_body"].bound_box[0])
