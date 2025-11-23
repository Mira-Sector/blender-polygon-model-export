from bpy.types import Panel
from .polygons import get_polygon_types

class SS14MaterialPanel(Panel):
    bl_label = "SS14 Polygon Data"
    bl_idname = "SS14_material_data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    def draw(self, context):
        layout = self.layout
        mat = context.material

        if not mat:
            return

        layout.prop(mat, "ss14_polygon_type")

        polygon_classes = {cls.polygon_type(): cls for cls in get_polygon_types()}
        ui_class = polygon_classes.get(mat.ss14_polygon_type)
        if ui_class:
            ui_class.draw_properties(layout, mat)
