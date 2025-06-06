"""This module contains the function's main logic."""

from pydantic import Field
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from RevitWall import *


class FunctionInputs(AutomateBase):
    """These are function author-defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    tolerance: float = Field(
        default=1e-6,
        title="Tolerance 📏",
        description=(
            "The tolerance used to determine if two values are equal. Values that differ by less than this tolerance will be considered equal."
        ),
        ge=0.0,  # Ensure tolerance is non-negative
        le=1e6,  # Arbitrary upper limit for tolerance
        multiple_of=1e-6,  # Ensure tolerance is a multiple of 1e-6
    )

    reference_level: str = Field(
        default="Level 0",
        title="Reference Level Name 🏗️",
        description=(
            "The name of the base / reference level with 0 elevation in Revit. The default is 'Level 0' for a new project. "
            "All elements will be created relative to this level's elevation. If you do not change the name, it WILL OVERRIDE the "
            "the reference level name in the Revit project."
        ),
        min_length=1,  # Ensure the level name is not empty
        max_length=200,  # Arbitrary upper limit for level name length
    )


def SketchUp_to_Revit(
    automate_context: AutomationContext, function_inputs: FunctionInputs
) -> None:
    """Main function to run the automation."""

    try:
        import json
        from specklepy.serialization.base_object_serializer import (
            BaseObjectSerializer,
            Base,
        )
        from Speckle_SketchUp_mapper import mapping_categories

        raw_speckle_data = automate_context.receive_version()

        speckle_data = json.loads(
            BaseObjectSerializer().write_json(raw_speckle_data)[1]
        )
        failed = False

        # Create the Revit friendly data to push to Speckle
        if "name" in speckle_data and speckle_data["name"] == "Sketchup Model":

            columns = []
            walls = []
            tol = function_inputs.tolerance

            for element in speckle_data["elements"]:
                if element["speckle_type"] == "Objects.BuiltElements.Revit.DirectShape":

                    match mapping_categories[
                        speckle_data["elements"][0]["category"]
                    ]:  # switch for different types of elements

                        case "Walls":

                            from shapely.geometry.polygon import Polygon
                            from pygeoops import centerline  

                            errors = []

                            vertices = remove_duplicates(
                                list(
                                    get_coordinates_from_list(
                                        element["baseGeometries"][0]["vertices"]
                                    )
                                ),
                                tol,
                            )

                            # Getting the coordinates of the vertices
                            vertices.sort(key=lambda x: x[2])

                            base_polygon = []
                            for (
                                vertex
                            ) in vertices:  # Only get the base polygon of the wall
                                if (
                                    vertex[2] > vertices[0][2] - tol
                                    and vertex[2] < vertices[-1][2] + tol
                                ):
                                    base_polygon.append(vertex[0:2])

                            # Get the centerline of the polygon to use as the baseLine
                            try:
                                from shapely import concave_hull

                                base_polygon = concave_hull(Polygon(base_polygon))

                                baseLine_raw = centerline(base_polygon, extend=True)
                                baseLine_cooked = list(baseLine_raw.coords)  # type: ignore

                                # Split the baseLine into straight line segments for Revit
                                baseLines = []
                                for segment in range(len(baseLine_cooked) - 1):
                                    baseLines.append(
                                        [
                                            baseLine_cooked[segment],
                                            baseLine_cooked[segment + 1],
                                        ]
                                    )

                                for (
                                    baseLine
                                ) in baseLines:  # Loop for multiple baseLines

                                    # Add the Revit formatted data to the walls list
                                    walls.append(
                                        revit_wall_data(
                                            units=element["units"],
                                            baseLine_start=[
                                                baseLine[0][0],
                                                baseLine[0][1],
                                                vertices[0][2],
                                            ],
                                            baseLine_end=[
                                                baseLine[1][0],
                                                baseLine[1][1],
                                                vertices[0][2],
                                            ],
                                            baseLine_length=baseLine_raw.length,  # type: ignore
                                            baseOffset=vertices[0][2],
                                            height=vertices[-1][2] - vertices[0][2],
                                            type=(  # Use default value if name is not provided
                                                element["name"]
                                                if (
                                                    "name" in element
                                                    and (
                                                        element["name"] != "<Mixed>"
                                                        or not str(
                                                            element["name"]
                                                        ).isspace()
                                                    )
                                                    and element["name"] != ""
                                                )
                                                else "Wall-Int_12P-100Blk-12P"
                                            ),
                                            level_name=function_inputs.reference_level,
                                            comment=(
                                                "[Speckle Automate]: Type specified."
                                                if (
                                                    "name" in element
                                                    and (
                                                        element["name"] != "<Mixed>"
                                                        or not str(
                                                            element["name"]
                                                        ).isspace()
                                                    )
                                                    and element["name"] != ""
                                                )
                                                else "[Speckle Automate]: Type not specified, default used."
                                            ),
                                        )
                                    )
                            except Exception as e:
                                from traceback import format_exc

                                errors.append(
                                    {
                                        "Error": "There was an error while creating the Revit data.",
                                        "Element": element,
                                        "Error Message": f"{e}",
                                        "Traceback": str(format_exc()),
                                        "Base Polygon": base_polygon,
                                    }
                                )
                                failed = True

                        case "Columns" | "StructuralColumns":

                            errors = []

                            # Get and sort the vertices by z-coordinate
                            vertices = remove_duplicates(
                                list(
                                    get_coordinates_from_list(
                                        element["baseGeometries"][0]["vertices"]
                                    )
                                ),
                                tol,
                            )
                            vertices.sort(key=lambda x: x[2])

                            try:
                                from shapely.geometry.polygon import Polygon
                                from shapely import force_2d
                                from RevitColumn import revit_column_data

                                # Get center points / baseLine points from top and bottom polygons
                                bottom_polygon = Polygon(
                                    [
                                        vertex
                                        for vertex in vertices
                                        if vertex[2] > vertices[0][2] - tol
                                        and vertex[2] < vertices[0][2] + tol
                                    ]
                                ).convex_hull
                                top_polygon = Polygon(
                                    [
                                        vertex
                                        for vertex in vertices
                                        if vertex[2] > vertices[-1][2] - tol
                                        and vertex[2] < vertices[-1][2] + tol
                                    ]
                                ).convex_hull

                                if len(bottom_polygon.boundary.coords) > 5:
                                    is_placeholder = (
                                        "PLACEHOLDER, this column is not rectangular. "
                                    )
                                else:
                                    is_placeholder = ""

                                baseLine_start = list(bottom_polygon.centroid.coords[0])
                                baseLine_end = list(top_polygon.centroid.coords[0])

                                columns.append(
                                    revit_column_data(
                                        units=element["units"],
                                        baseLine_start=baseLine_start
                                        + [vertices[0][2]],
                                        baseLine_end=baseLine_end + [vertices[-1][2]],
                                        baseLine_length=vertices[-1][2]
                                        - vertices[0][2],
                                        baseOffset=vertices[0][2],
                                        type=(  # Use default value if name is not provided
                                            element["name"]
                                            if (
                                                "name" in element
                                                and (
                                                    element["name"] != "<Mixed>"
                                                    or not str(
                                                        element["name"]
                                                    ).isspace()
                                                )
                                                and element["name"] != ""
                                            )
                                            else "450x450mm"
                                        ),
                                        level_name=function_inputs.reference_level,
                                        isSlanted=(  # Check if the column is vertically slanted
                                            not force_2d(bottom_polygon).equals_exact(
                                                force_2d(top_polygon), tol
                                            )
                                        ),
                                        comment=(
                                            f"[Speckle Automate]: {is_placeholder}Type specified."
                                            if (
                                                "name" in element
                                                and (
                                                    element["name"] != "<Mixed>"
                                                    or not str(
                                                        element["name"]
                                                    ).isspace()
                                                )
                                                and element["name"] != ""
                                            )
                                            else f"[Speckle Automate]: {is_placeholder}Type not specified, default used."
                                        ),
                                    )
                                )

                            except Exception as e:
                                from traceback import format_exc

                                errors.append(
                                    {
                                        "Error": "There was an error while creating the Revit data.",
                                        "Element": element,
                                        "Error Message": f"{e}",
                                        "Traceback": str(format_exc()),
                                        "Vertices": vertices,
                                    }
                                )
                                failed = True

                        case _:
                            pass

            revit_data = [*(walls if walls else []), *(columns if columns else [])]
            if not revit_data:
                revit_data = errors

            revit_data = speckle_data_package(*revit_data)

            # Push the Revit data to Speckle
            automate_context.create_new_version_in_project(
                root_object=Base(**revit_data),
                model_name="Speckle Automate: SketchUp to Revit",
                version_message="Speckle Automate created version for:"
                + str(raw_speckle_data.id),
            )

        automate_context.mark_run_success(
            "Automation completed successfully.\n"
            + str(automate_context.automation_run_data)
        )

    except Exception as e:
        from traceback import format_exc

        automate_context.mark_run_failed(
            "Automation failed: \n" f"Error: {e}\nTraceback: {str(format_exc())}"
        )

    finally:
        if failed:
            from traceback import format_exc

            automate_context.mark_run_exception(
                f"There were errors creating the Revit data from the objects.\n\nError: {errors}\nTraceback: {str(format_exc())}"
            )


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!

    execute_automate_function(SketchUp_to_Revit, FunctionInputs)
