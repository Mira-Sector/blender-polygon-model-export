from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class SS14PolygonProperty:
    name: str
    type: str
    label: str
    description: str
    default: object = None

class SS14BasePolygon(ABC):
    @classmethod
    @abstractmethod
    def polygon_type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def description(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_properties(cls) -> dict:
        pass

    @classmethod
    def draw_properties(cls, layout, mat):
        for prop in cls.get_properties():
            if not hasattr(mat, prop.name):
                continue

            layout.prop(
                mat,
                prop.name,
                text=prop.label,
            )

class SS14ColoredPolygon(SS14BasePolygon):
    @classmethod
    def polygon_type(cls):
        return "ColoredPolygon"

    @classmethod
    def name(cls):
        return "Colored Polygon"

    @classmethod
    def description(cls):
        return "Allow specifying a color to modulate by on an unshaded polygon."

    @classmethod
    def get_properties(cls):
        return [
            SS14PolygonProperty(
                name="color",
                type="color",
                label="Color",
                description="The base color of the polygon.",
                default=(1.0, 1.0, 1.0)
            )
        ]

class SS14FlatShadedPolygon(SS14ColoredPolygon):
    @classmethod
    def polygon_type(cls):
        return "FlatShadedPolygon"

    @classmethod
    def name(cls):
        return "Flat Shaded Polygon"

    @classmethod
    def description(cls):
        return "Shades the color of the polygon based on the angle towards the camera for primitive depth perception."

    @classmethod
    def get_properties(cls):
        props = super().get_properties().copy()
        # Add its own
        props.append(
            SS14PolygonProperty(
                name="minBrightness",
                type="float",
                label="Minimum Brightness",
                description="Minimum brightness for shading.",
                default=0.2
            )
        )
        return props

def get_polygon_types():
    subclasses = set()

    def recurse(cls):
        for sub in cls.__subclasses__():
            subclasses.add(sub)
            recurse(sub)

    recurse(SS14BasePolygon)
    return subclasses

def get_polygon_enum_items(self, context):
    items = []
    for cls in get_polygon_types():
        items.append((cls.polygon_type(), cls.name(), cls.description()))
    return items
