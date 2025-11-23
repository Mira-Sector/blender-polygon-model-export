from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
import yaml

class SS14ExportPolygonModel(Operator, ExportHelper):
    bl_idname = "export_scene.ss14_polygon_model"
    bl_label = "Export SS14 PolygonModel"
    bl_options = {'PRESET'}

    filename_ext = ".yml"

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        output = { "polygons": [] }

        for poly in mesh.polygons:
            verts = [
                mesh.vertices[i].co[:] for i in poly.vertices
            ]
            
            poly_type = obj.get("ss14_polygon_type", "Polygon")
            data = {
                "type": poly_type,
                "vertices": verts
            }

            output["polygons"].append(data)

        with open(self.filepath, 'w') as f:
            yaml.dump(output, f)

        return {'FINISHED'}

