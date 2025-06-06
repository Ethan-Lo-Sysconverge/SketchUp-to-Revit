# SketchUp to Revit Automate Function - Python

This function aims to import SketchUp models as native Revit elements using Speckle. Instead of translating the model from SketchUp to Revit, the function pulls the necessary data from the SketchUp Speckle model, and reconstructs a native Revit element and creates a new version of the model. Revit walls are defined by a baseline, while SketchUp walls are meshes. Pygeoops centerline feature is used to create this baseline from the SketchUp mesh. This Specklepy created version is ready to import to Revit like any other Speckle object. 

## Usage

Using the V2 legacy mappers in SketchUp, you can specify what type of element to export (Only Direct Shapes are supported) and what Revit type. In the 'Name' field of the mapper, individual objects can be given a Revit type (it must be the exact spelling of a Revit type in the project you plan to import it into. Works with renamed system family types).

### Supported elements

- Simple walls:
    - Must be exported / sent to Speckle with the category 'Walls'
    - Walls must be perfectly vertical (no slants)
    - Walls cannot have doors, windows, cutouts, extrusions, etc.
    - Wall must be a group or component in SketchUp when exporting to Speckle
    - Wall must not have a perfect square base
    - Walls can be 'bent' or have multiple 'arms' (L, N, M shapes, etc. Avoid K, Y, X shapes, etc.)
        - Arms must be >3x wall width to ensure accuracy
    - Works best with walls of constant width
    - Must have no (even slightly) curved sections
    - Can be elevated / vertically offset
    - Comments will note that it was created through Speckle Automate and either had or did not have a type specified

- Simple structural columns:
    - Must be exported / sent to Speckle with the category 'Columns' or 'StructuralColumns'
    - Columns can be slanted, but top and bottom faces of the column must be parallel to the ground
    - Columns can be elevated / vertically offset
    - All columns will be imported to Revit as a rectangular column by default
        - If a non-rectangular column is imported, it will have a comment specifying it is a placeholder
    - Comments will also note that it was created through Speckle Automate and either had or did not have a type specified
    - Column dimensions will be ignored
        - In Revit, column dimensions are dependent on the type
        - Please model columns in SketchUp to be as close to the desired Revit type dimensions as possible for best results


Please be reasonable with what you are trying to import. If needed, split complex elements into simple ones.
