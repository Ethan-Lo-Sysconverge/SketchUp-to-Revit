def revit_wall_data(
    height: float,
    baseLine_start: list[float],
    baseLine_end: list[float],
    baseLine_length: float,
    units="mm",
    baseLine_domain_start=0.0,
    baseLine_domain_end=0.0,
    baseOffset=0.0,
    family="Basic Wall",
    type="Wall-Int_12P-100Blk-12P",
    flipped=False,
    level_elevation=0.0,
    level_name="Level 0",
    level_referenceOnly=False,
    phaseCreated="New Construction",
    structural=False,
) -> dict:
    """
    Formats the input data so it can be pushed to Speckle and received as a native Revit wall.

    INPUTS:

        units - Self explanatory.

        baseLine:
            Domain start/end - I dont know why this is important.
            start - [x,y,z] coordinates of the start of the baseline.
            end - [x,y,z] coordinates of the end of the baseline.
            length - [num] length of the baseline.

        baseOffset - [num] offset relative to the assigned level.
        family - [str] name of the wall family.
        type - [str] name of the wall type.
        flipped - [bool] whether the wall is flipped or not.
        height - [num] height of the wall.

        level:
            elevation - [num] elevation of the level.
            name - [str] name of the level.
            referenceOnly - [bool] whether the level is reference only or not.

        phaseCreated - [str] name of the phase created.
        structural - [bool] whether the wall is structural or not.

    """

    from uuid import uuid4

    random_id = uuid4().hex

    outputDict = {
        "id": random_id,
        "speckle_type": "Objects.BuiltElements.Wall:Objects.BuiltElements.Revit.RevitWall",
        "totalChildrenCount": 0,
        "applicationId": None,
        "baseLine": {
            "id": None,
            "speckle_type": "Objects.Geometry.Line",
            "totalChildrenCount": 0,
            "applicationId": None,
            # "area": 0,
            "bbox": None,
            "domain": {
                "id": None,
                "speckle_type": "Objects.Primitive.Interval",
                "totalChildrenCount": 0,
                "applicationId": None,
                "end": baseLine_domain_end,
                "start": baseLine_domain_start,
                "units": units,
            },
            "end": {
                "id": None,
                "speckle_type": "Objects.Geometry.Point",
                "totalChildrenCount": 0,
                "applicationId": None,
                "units": units,
                "x": baseLine_end[0],
                "y": baseLine_end[1],
                "z": baseLine_end[2],
            },
            "length": baseLine_length,
            "start": {
                "id": None,
                "speckle_type": "Objects.Geometry.Point",
                "totalChildrenCount": 0,
                "applicationId": None,
                "units": units,
                "x": baseLine_start[0],
                "y": baseLine_start[1],
                "z": baseLine_start[2],
            },
            "units": units,
        },
        "baseOffset": baseOffset,
        "builtInCategory": "OST_Walls",
        "category": "Walls",
        # "elements": None,
        "family": family,
        "flipped": flipped,
        "height": height,
        # "isRevitLinkedModel": False,
        # "level": {
        #     "id": None,
        #     "speckle_type": "Objects.BuiltElements.Level:Objects.BuiltElements.Revit.RevitLevel",
        #     "totalChildrenCount": 0,
        #     "applicationId": None,
        #     "builtInCategory": "OST_Levels",
        #     "category": "Levels",
        #     "createView": True,
        #     "elementId": None,
        #     "elevation": level_elevation,
        #     "isRevitLinkedModel": False,
        #     "materialQuantities": [],
        #     "name": level_name,
        #     "referenceOnly": level_referenceOnly,
        #     "units": units,
        #     "worksetId": "0",
        # },
        "phaseCreated": phaseCreated,
        "structural": structural,
        # "topLevel": None,
        "topOffset": 0,
        "type": type,
        "units": units,
        # "worksetId": "0",
    }

    return outputDict


def revit_wall_package(*walls) -> dict:
    """
    Formats the input data so it can be pushed to Speckle and received as a native Revit wall.
    INPUTS:

        walls - [list[dict]] list of wall data formatted by revit_wall_data().
    """

    from uuid import uuid4

    random_id = uuid4().hex

    outputPackage = {
        "id": random_id,
        "speckle_type": "Base",
        "totalChildrenCount": 0,
        "applicationId": None,
        "data": list(walls),
        "name": "Walls",
        "units": walls[0]["units"],
    }

    return outputPackage


# def construct_polygon_from_points(points: list):
#     """
#     Constructs a polygon from a list of points. Works only for simple quadrilaterals and V or L shapes.

#     Checks for the number of points (<6 or not) and sorts points by angle relative to reflex point if applicable. Then brute forces a polygon using area minimization, if applicable.
#     """
#     from shapely.geometry.polygon import Polygon

#     if len(points) < 6:
#         return Polygon(Polygon(points).convex_hull.exterior.coords)  # type: ignore

#     else:
#         p = Polygon(points)
#         # Get the missing reflex point
#         polygon_list = list(p.exterior.coords)
#         polygon_convex_hull_list = list(p.convex_hull.exterior.coords)  # type: ignore
#         missing_points = []
#         for i in polygon_list:
#             if i not in polygon_convex_hull_list:
#                 missing_points.append(i)

#         if len(missing_points) != 1:
#             return None

#         reflex_point = missing_points[0]
#         del missing_points

#         # Sort the polygon points by angle relative to the reflex point
#         def angle_from_point(point, center):
#             from math import atan2, degrees, pi

#             gap = atan2(point[1] - center[1], point[0] - center[0])
#             if gap < 0:
#                 gap += 2 * pi
#             return degrees(gap)

#         sorted_points = [
#             [i, angle_from_point(i, reflex_point)] for i in polygon_convex_hull_list
#         ]
#         sorted_points.sort(key=lambda x: x[1])

#         areas = []
#         sorted_points = [i[0] for i in sorted_points]

#         for i in range(len(sorted_points)):
#             temp = sorted_points[:i] + [reflex_point] + sorted_points[i:]
#             if Polygon(temp).is_valid:
#                 areas.append(Polygon(temp).area)

#         sorted_points.insert(areas.index(min(areas)), reflex_point)

#         return Polygon(sorted_points)

def from_list_get(list: list, attribute, position: int = -1) -> list:
    l = []

    if type(attribute) == str:
        for item in list:
            l.append(getattr(item, attribute))

    elif type(attribute) == int and position == -1:
        for item in list:
            if attribute in item:
                l.append(item)

    elif type(attribute) == int and position != -1:
        for item in list:
            try:
                if attribute in item[position]:
                    l.append(item)
            except:
                if attribute == item[position]:
                    l.append(item)
    return l


def get_coordinates_from_list(raw_coords: list) -> list[list[float]]:
    return [raw_coords[i : i + 3] for i in range(0, len(raw_coords), 3)]


def remove_duplicates(l: list) -> list:
    seen = set()
    result = []

    for item in l:
        t = tuple(item)

        if t not in seen:
            seen.add(t)
            result.append(item)

    return result