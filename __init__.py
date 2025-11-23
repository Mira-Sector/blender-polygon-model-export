import bpy
from .export import SS14ExportPolygonModel
from .material_panel import SS14MaterialPanel
from .properties import register_material_properties, unregister_material_properties


bl_info = {
    "name": "SS14 PolygonModel Exporter",
    "author": "Doctor-Cpu",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "File > Export > SS14 PolygonModel (.yml)",
    "description": "Export mesh as Space Station 14 PolygonModel YAML",
    "category": "Import-Export",
}


def menu_func_export(self, context):
    self.layout.operator(SS14ExportPolygonModel.bl_idname, text="SS14 PolygonModel (.yml)")


def register():
    register_material_properties()

    bpy.utils.register_class(SS14ExportPolygonModel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

    bpy.utils.register_class(SS14MaterialPanel)

def unregister():
    bpy.utils.unregister_class(SS14ExportPolygonModel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    bpy.utils.unregister_class(SS14MaterialPanel)
    
    unregister_material_properties()


if __name__ == "__main__":
    register()
