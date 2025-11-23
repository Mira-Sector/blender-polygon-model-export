from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from .polygons import get_polygon_types
import yaml

SERIALIZE_MAP = {
    "color": lambda val: "#{:02x}{:02x}{:02x}".format(
        int(val[0]*255), int(val[1]*255), int(val[2]*255)
    ) if val else "#ffffff"
}

class SS14PolygonTag:
    def __init__(self, type_name, data):
        self.type_name = type_name
        self.data = data

def polygon_representer(dumper, polygon):
        return dumper.represent_mapping(f"!type:{polygon.type_name}", polygon.data)

class SS14ExportPolygonDumper(yaml.SafeDumper):
    pass

SS14ExportPolygonDumper.add_representer(SS14PolygonTag, polygon_representer)

class SS14ExportPolygonModel(Operator, ExportHelper):
    bl_idname = "export_scene.ss14_polygon_model"
    bl_label = "Export SS14 PolygonModel"
    bl_options = {'PRESET'}

    filename_ext = ".yml"

    def execute(self, context):
        output = []
        invalid_objects = []
        for obj in context.scene.objects:
            if obj.type != "MESH":  # skip lights cameras
                continue

            mat = obj.active_material
            if not mat:
                continue

            poly_type = getattr(mat, "ss14_polygon_type", None)
            if poly_type is None:
                continue
            
            polygon_classes = {cls.polygon_type(): cls for cls in get_polygon_types()}
            cls = polygon_classes.get(poly_type)

            mesh = obj.data
            obj_output = {
                "type": "polygonModel",
                "id": obj.name,
                "polygons": []
            }
            for poly in mesh.polygons:
                verts = [
                    "{:.6f}, {:.6f}, {:.6f}".format(*mesh.vertices[i].co)
                    for i in poly.vertices
                ]

                if len(verts) != 3:
                    invalid_objects.append(obj.name)
                    break
                
                data = {
                    "vertices": verts
                }

                if cls:
                    for prop in cls.get_properties():
                        if not hasattr(obj, prop.name):
                            continue

                        value = getattr(obj, prop.name)
                        serializer = SERIALIZE_MAP.get(prop.type, lambda v: v)
                        data[prop.name] = serializer(value)

                
                obj_output["polygons"].append(SS14PolygonTag(poly_type, data))
            output.append(obj_output)

        if invalid_objects:
            self.report({'ERROR'}, "Objects with non-triangle faces: " + ", ".join(invalid_objects))
            return {'CANCELLED'}

        with open(self.filepath, 'w') as f:
            yaml.dump(output, f, Dumper=SS14ExportPolygonDumper, sort_keys=False)

        return {'FINISHED'}

