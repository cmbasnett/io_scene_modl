bl_info = {
    'name': 'Lithtech MODL Format',
    'description': 'Import and export MODEL00P models and animations files from Lithtech Jupiter games (eg. F.E.A.R., Condemned: Criminal Origins).',
    'author': 'Colin Basnett',
    'version': (1, 0, 0),
    'blender': (2, 79, 0),
    'location': 'File > Import-Export',
    'warning': 'This add-on is under development.',
    'wiki_url': 'https://github.com/cmbasnett/io_scene_modl/wiki',
    'tracker_url': 'https://github.com/cmbasnett/io_scene_modl/issues',
    'support': 'COMMUNITY',
    'category': 'Import-Export'
}

if 'bpy' in locals():
    import importlib
    if 'lta' in locals(): importlib.reload(lta)
    if 'model'        in locals(): importlib.reload(model)
    #if 'builder'    in locals(): importlib.reload(builder)
    if 'reader'     in locals(): importlib.reload(reader)
    #if 'writer'     in locals(): importlib.reload(writer)
    if 'importer'   in locals(): importlib.reload(importer)
    #if 'exporter'   in locals(): importlib.reload(exporter)

import bpy
from . import lta
from . import model
# from . import builder
from . import reader
# from . import writer
from . import importer
# from . import exporter

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(importer.ImportOperator.menu_func_import)
    # bpy.types.INFO_MT_file_export.append(exporter.ExportOperator.menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(importer.ImportOperator.menu_func_import)
    # bpy.types.INFO_MT_file_export.remove(exporter.ExportOperator.menu_func_export)