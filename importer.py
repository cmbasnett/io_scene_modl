import bpy
import bpy_extras
from bpy.props import StringProperty
from .reader import ModelReader


class ImportOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = 'io_scene_modl.modl_import'  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = 'Import Lithtech MODL'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    # ImportHelper mixin class uses this
    filename_ext = ".model00p"

    filter_glob = StringProperty(
        default="*.model00p",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        reader = ModelReader().from_file(self.filepath)
        return {'FINISHED'}

    @staticmethod
    def menu_func_import(self, content):
        self.layout.operator(ImportOperator.bl_idname, text='Lithtech MODL (.model00p)')
