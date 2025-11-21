import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator

bl_info = {
    "name": "SS14 PolygonModel Exporter",
    "author": "Doctor-Cpu",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "File > Export > SS14 PolygonModel (.yml)",
    "description": "Export mesh as Space Station 14 PolygonModel YAML",
    "category": "Import-Export",
}

class ExportSS14PolygonModel(Operator, ExportHelper):
    """Export selected mesh as SS14 PolygonModel YAML"""
    bl_idname = "export_scene.ss14_polygon_model"
    bl_label = "Export SS14 PolygonModel"
    bl_options = {'PRESET'}

    filename_ext = ".yml"

    def execute(self, context):
        return {'FINISHED'}


def menu_func_export(self, context):
    self.layout.operator(ExportSS14PolygonModel.bl_idname,
                         text="SS14 PolygonModel (.yml)")


def register():
    bpy.utils.register_class(ExportSS14PolygonModel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSS14PolygonModel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
