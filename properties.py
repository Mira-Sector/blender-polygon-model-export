import bpy
from .polygons import get_polygon_enum_items, get_polygon_types

BLENDER_PROP_MAP = {
    "color": lambda p: bpy.props.FloatVectorProperty(
        name=p.label,
        description=p.description,
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=p.default
    ),
    "float": lambda p: bpy.props.FloatProperty(
        name=p.label,
        description=p.description,
        min=0.0,
        max=1.0,
        default=p.default
    ),
    "int": lambda p: bpy.props.IntProperty(
        name=p.label,
        description=p.description,
        default=p.default
    ),
}

def register_material_properties():
    if not hasattr(bpy.types.Material, "ss14_polygon_type"):
        bpy.types.Material.ss14_polygon_type = bpy.props.EnumProperty(
            name="Polygon Type",
            items = get_polygon_enum_items
        )

    for cls in get_polygon_types():
        for prop in cls.get_properties():
            if hasattr(bpy.types.Material, prop.name):
                continue

            constructor = BLENDER_PROP_MAP.get(prop.type)
            if constructor:
                setattr(bpy.types.Material, prop.name, constructor(prop))

def unregister_material_properties():
    if hasattr(bpy.types.Material, "ss14_polygon_type"):
        del bpy.types.Material.ss14_polygon_type

    for cls in get_polygon_types():
        for prop in cls.get_properties():
            if hasattr(bpy.types.Material, prop.name):
                delattr(bpy.types.Material, prop.name)
