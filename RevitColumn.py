def revit_column_data(
    baseLine_start: list[float],
    baseLine_end: list[float],
    baseLine_length: float,
    units="mm",
    baseLine_domain_start=0.0,
    baseLine_domain_end=1.0,
    baseOffset=0.0,
    family="Columns_Rectangular",
    type="450x450mm",
    isSlanted=False,
    level_elevation=0.0,
    level_name="Level 0",
    level_referenceOnly=False,
    phaseCreated="New Construction",
    rotation=0.0,
    comment: str | None = None,
) -> dict:
    """
    Formats SketchUp column data for Revit. Does not create a complete package for Speckle.

    Args:
        baseLine_start (list[float]): [x, y, z] coordinates of the column base line start point.
        baseLine_end (list[float]): [x, y, z] coordinates of the column base line end point.
        baseLine_length (float): Length of the column base line. Functionally the column height (length if slanted).
        units (str, optional): Unit system for dimensions. Defaults to "mm".
        baseLine_domain_start (float, optional): Start value of the domain parameter. Defaults to 0.0.
        baseLine_domain_end (float, optional): End value of the domain parameter. Defaults to 1.0.
        baseOffset (float, optional): Vertical offset from the reference level. Defaults to 0.0.
        family (str, optional): Revit system family name. Defaults to "Columns_Rectangular".
        type (str, optional): Revit system type name. Supports renamed system families specific to project. Defaults to "450x450mm".
        isSlanted (bool, optional): Whether the column is slanted. Defaults to False.
        level_elevation (float, optional): Elevation of the base level. Defaults to 0.0.
        level_name (str, optional): Name of the base level. Will override the reference level name in project. Defaults to "Level 0".
        level_referenceOnly (bool, optional): Whether the level is for reference only. Defaults to False.
        phaseCreated (str, optional): Phase in which the column was created. Defaults to "New Construction".
        rotation (float, optional): Rotation angle of the column in degrees, relative to East direction. Defaults to 0.0.
    Returns:
        dict: Formatted column data for Speckle.
    """

    from uuid import uuid4

    column_data = {
        "id": uuid4().hex,
        "speckle_type": "Objects.BuiltElements.Column:Objects.BuiltElements.Revit.RevitColumn",
        "totalChildrenCount": 0,
        "baseLine": {
            "id": None,
            "speckle_type": "Objects.Geometry.Line",
            "totalChildrenCount": 0,
            "applicationId": None,
            "area": 0,
            "domain": {
                "id": None,
                "speckle_type": "Objects.Primitive.Interval",
                "totalChildrenCount": 0,
                "applicationId": None,
                "end": baseLine_domain_end,
                "start": baseLine_domain_start,
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
        "builtInCategory": "OST_Columns",
        "category": "Columns",
        "family": family,
        "isSlanted": isSlanted,
        "phaseCreated": phaseCreated,
        "rotation": rotation,
        "topOffset": 0,
        "type": type,
        "units": units,
        "level": {
            "id": None,
            "speckle_type": "Objects.BuiltElements.Level:Objects.BuiltElements.Revit.RevitLevel",
            "totalChildrenCount": 0,
            "applicationId": None,
            "elevation": level_elevation,
            "name": level_name,
            "referenceOnly": level_referenceOnly,
        },
        "parameters": {
            "id": None,
            "speckle_type": "Base",
            "totalChildrenCount": 0,
            "ALL_MODEL_INSTANCE_COMMENTS": {
                "id": None,
                "speckle_type": "Objects.BuiltElements.Revit.Parameter",
                "totalChildrenCount": 0,
                "applicationId": None,
                "applicationInternalName": "ALL_MODEL_INSTANCE_COMMENTS",
                "applicationUnit": None,
                "applicationUnitType": None,
                "IsReadOnly": False,
                "isShared": False,
                "isTypeParameter": False,
                "name": "Comments",
                "units": None,
                "value": comment if comment else None,
            },
        },
    }

    return column_data
