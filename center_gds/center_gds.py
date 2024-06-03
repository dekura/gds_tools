from pathlib import Path
import gdspy

def extract_center_polygon(input_gds, output_gds, layer_numbers):
    # Load the GDS file
    gdsii = gdspy.GdsLibrary(infile=input_gds)

    # Create a new GDSII library for the output
    out_gdsii = gdspy.GdsLibrary()

    # Iterate through all top-level cells in the GDSII file
    for cell in gdsii.top_level():
        # Create a new cell in the output GDSII
        out_cell = out_gdsii.new_cell(cell.name)

        # Define the central rectangle based on layer 7777
        boundary_polygons = cell.get_polygons(by_spec=True).get((7777, 0), [])
        if boundary_polygons:
            minx, miny = boundary_polygons[0].min(axis=0)
            maxx, maxy = boundary_polygons[0].max(axis=0)
            center_x = (maxx + minx) / 2
            center_y = (maxy + miny) / 2
            half_width = 700  # 1400 µm / 2

            # Create the central rectangle
            central_rect = gdspy.Rectangle((center_x - half_width, center_y - half_width),
                                           (center_x + half_width, center_y + half_width))

            for layer in layer_numbers:
                # Get all polygons on the specified layers
                polygons = cell.get_polygons(by_spec=True).get((layer, 0), [])
                
                for polygon in polygons:
                    # Convert the polygon coordinates to micrometers
                    # Intersect the polygon with the central rectangle
                    clipped_polygons = gdspy.boolean([polygon], [central_rect], 'and')
                    
                    # Add the resulting polygons to the output cell with the correct layer
                    if clipped_polygons is not None:
                        out_cell.add(clipped_polygons)

            # Also add the boundary layer 7777 polygons to the output cell
            for boundary_polygon in boundary_polygons:
                # Convert the boundary polygon coordinates to micrometers
                out_cell.add(gdspy.Polygon(boundary_polygon, layer=7777, datatype=0))

    # Write the output GDS file
    out_gdsii.write_gds(output_gds)


# Example usage
basedir = '/Users/guojinc/Downloads/datasets/nvdla-samples/finalclips/'
basedir = Path(basedir)
output_dir = basedir / 'center_gds'
input_gds = basedir / 'gds' / 'clip0-18524.gds'
output_gds = output_dir / 'clip0-18524_center.gds'
layer_numbers = [1, 7777]
extract_center_polygon(input_gds, output_gds, layer_numbers)

# extract_center_polygon(input_gds, output_gds, layer_numbers)
