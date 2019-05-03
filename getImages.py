import bpy
from math import radians, sqrt
#to run in background, use: ./blender -b -P <script_location>

#global constants
#camDimY = 1080      #in pixels
#camDimX = 1920
borderSize = 700   #could be user_input as zoom
                    #or relative to obj size

# IMPORT OBJECT
#bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete() #delete all objects

fileLoc = "/Users/jeffsanchez/Desktop/SA/3d_to_gif/teapot.obj"
                #should be a command line argument
bpy.ops.import_scene.obj(filepath=fileLoc)
                #use import_mesh for ply and stl files
mainObj = bpy.context.selected_objects[0]
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')   #ensure that obj is centered
#bpy.ops.transform.transform(mode='ALIGN')           #align local frame to global frame
                                                    #cause camera operates in global frame
                                                    
# ADD CAMERA
xAngle = radians(60)    #would be user input
yAngle = 0
zAngle = 0
bpy.ops.object.camera_add(view_align=False, enter_editmode=False,
                            rotation=(xAngle, yAngle, zAngle))

bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects[mainObj.name].select = True
#bpy.context.scene.objects.active = bpy.data.objects[mainObj.name]  #make it active selected object

bpy.context.scene.render.resolution_x -= borderSize   #make cam view smaller
bpy.context.scene.render.resolution_y -= borderSize
bpy.context.scene.camera = bpy.data.objects['Camera']           #set active camera
bpy.ops.view3d.camera_to_view_selected()                        #fit obj in cam view
bpy.context.object.data.clip_end = 1000                         #to see even far away obj's
bpy.context.scene.render.resolution_x += borderSize
bpy.context.scene.render.resolution_y += borderSize   #reset cam view size

# SET LIGHTING
bpy.context.scene.world.light_settings.use_environment_light = True

#TAKE IMAGES
rotationSteps = 10      #number of images, would be usr input
mainObj.convert_space(from_space='WORLD', to_space='LOCAL')
for step in range(0,rotationSteps):
   #mainObj.rotation_euler.rotate_axis("Z", radians(step*(360.0/rotationSteps)))
   mainObj.rotation_euler[2] = radians(step*(360.0/rotationSteps))
   bpy.data.scenes["Scene"].render.filepath = \
                '/Users/jeffsanchez/Desktop/SA/3d_to_gif/images/%d.jpg' % step
   bpy.ops.render.render(write_still=True)
