import bpy
import datetime as dt

bl_info = {
    'name': 'Creating panels demonstation',
    'category': 'All'
}

'''
    [X] Timing
    [X] Save original samples
    [X] Change samples to one
    [] Render current frame
    [] Label telling them to render from most complicated frame
'''

result = "N/A"
sample_num = 0
original_output = ""
start_time = 0
end_time = 0
start_time2 = 0
end_time2 = 0
   
class EvalOp(bpy.types.Operator):
    """Eval"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
        
    def execute(self, context):
        ''' GPU RENDER TEST '''
        start_time = dt.datetime.now()
        sample_num = bpy.data.scenes["Scene"].cycles.samples
        bpy.data.scenes["Scene"].cycles.samples = 1
        original_output = bpy.data.scenes["Scene"].render.filepath
        bpy.data.scenes["Scene"].render.filepath = "FIGURE OUT LATER"
        bpy.ops.render.render(write_still=True)
        bpy.data.scenes["Scene"].render.filepath = original_output
        bpy.context.user_preferences.system.compute_device = "CUDA_0"
        print(bpy.context.user_preferences.system.compute_device)
        bpy.data.scenes["Scene"].cycles.samples = sample_num
        end_time = dt.datetime.now()
        
        ''' CPU RENDER TEST '''
        start_time2 = dt.datetime.now()
        sample_num = bpy.data.scenes["Scene"].cycles.samples
        bpy.data.scenes["Scene"].cycles.samples = 1
        original_output = bpy.data.scenes["Scene"].render.filepath
        bpy.data.scenes["Scene"].render.filepath = "FIGURE OUT LATER"
        bpy.ops.render.render(write_still=True)
        bpy.data.scenes["Scene"].render.filepath = original_output
        bpy.context.user_preferences.system.compute_device = "CPU"
        print(bpy.context.user_preferences.system.compute_device)
        bpy.data.scenes["Scene"].cycles.samples = sample_num
        end_time2 = dt.datetime.now()
        
        print(str(endtime - start_time))
        print(str(endtime2 - start_time2))
        
        return {'FINISHED'}

class Properties(bpy.types.PropertyGroup):
    my_bool = bpy.props.BoolProperty( name="GPU OR CPU", description="A simple bool property", default = True)
    another = bpy.props.BoolProperty( name="ANOTHER", description="ANOTHER DESC", default = False)
    my_enum = bpy.props.EnumProperty(
        name="",
        description="GPU OR CPU",
        items= [('OP1', "GPU", ""),
                ('OP2', "CPU", ""),
               ]
        )

class ActiveObject(bpy.types.Panel):
    bl_idname = 'Evaluator'
    bl_label = 'Evaluates the best method of rendering'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Evaluate'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        obj = context.object
        
        row = layout.row()
        row.label(text=("Use: " + result))
        #layout.prop(mytool, "my_enum")
        row = layout.row()
        row.operator("object.simple_operator", "Evaluate")

def register():
    bpy.utils.register_class(ActiveObject)
    bpy.utils.register_class(Properties)
    bpy.utils.register_class(EvalOp)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Properties)

def unregister():
    bpy.utils.unregister_class(ActiveObject)
    bpy.utils.unregister_class(Properties)
    bpy.utils.unregister_class(EvalOp)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()