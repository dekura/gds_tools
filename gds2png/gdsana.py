import csv
import gdspy
import shutil
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

padding = 300

def gds_polygons_analysis(input_gds_path):
    # Read GDS file
    gdsii = gdspy.GdsLibrary(unit=1e-9)
    gdsii.read_gds(input_gds_path, units='convert')
    cell = gdsii.top_level()[0]

    layer_number = 1
    dtype = 0
    # Only get polygons from layer number 1
    try:
        polyset = cell.get_polygons(by_spec=True)[(layer_number, dtype)]
    except KeyError:
        print(f"\nLayer {layer_number} not found in {input_gds_path}")
        return 0, 0

    total_polygons = len(polyset)

    # Calculate the bounding box
    bbox = cell.get_bounding_box()
    bbox_min_x, bbox_min_y = bbox[0]
    bbox_max_x, bbox_max_y = bbox[1]

    # Define check region with 300 units margin
    check_region_min_x = bbox_min_x + padding
    check_region_min_y = bbox_min_y + padding
    check_region_max_x = bbox_max_x - padding
    check_region_max_y = bbox_max_y - padding

    # Count polygons within the check region
    in_region_polygons = 0
    for polygon in polyset:
        # Calculate the center point of the polygon
        center_x = sum([p[0] for p in polygon]) / len(polygon)
        center_y = sum([p[1] for p in polygon]) / len(polygon)

        # Check if the center point is within the check region
        if (check_region_min_x <= center_x <= check_region_max_x and
            check_region_min_y <= center_y <= check_region_max_y):
            in_region_polygons += 1

    return total_polygons, in_region_polygons

def process_gds_folders(base_folder):
    base_folder = Path(base_folder)
    clip_folders = [folder for folder in base_folder.iterdir() if folder.is_dir()]

    for clip_folder in tqdm(clip_folders, desc='Processing folders'):
        csv_file_path = clip_folder.parent / f'{clip_folder.name}.csv'
        gds_files = list(clip_folder.glob('*.gds'))

        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['filename', 'polygons', 'in region polygons'])

            for gds_file in tqdm(gds_files, desc=f'Processing {clip_folder.name}', leave=False):
                try:
                    total_polygons, in_region_polygons = gds_polygons_analysis(gds_file)
                    csv_writer.writerow([gds_file.name, total_polygons, in_region_polygons])
                except Exception as e:
                    print(f"Error processing file {gds_file}: {e}")


def delete_csv_files(base_folder):
    base_folder = Path(base_folder)
    clip_folders = [folder for folder in base_folder.iterdir() if folder.is_dir()]
    for clip_folder in tqdm(clip_folders, desc='Deleting CSV files in folders'):
        csv_files = list(clip_folder.glob('*.csv'))
        for csv_file in csv_files:
            try:
                csv_file.unlink()  # Delete the CSV file
                print(f'Deleted: {csv_file}')
            except Exception as e:
                print(f'Error deleting file {csv_file}: {e}')


def filter_and_save_csv(base_folder):
    base_folder = Path(base_folder)
    pass_rate = 0.8
    output_csv_path = base_folder / f'clip_all_{pass_rate}.csv'

    with open(output_csv_path, mode='w', newline='') as output_csv_file:
        csv_writer = csv.writer(output_csv_file)
        csv_writer.writerow(['filename', 'polygons', 'in region polygons'])

        for i in range(32):
            clip_csv_path = base_folder / f'clip{i}.csv'
            if clip_csv_path.exists():
                with open(clip_csv_path, mode='r') as input_csv_file:
                    csv_reader = csv.reader(input_csv_file)
                    next(csv_reader)  # Skip the header row

                    for row in csv_reader:
                        filename, num_all, num_in = row
                        num_all = int(num_all)
                        num_in = int(num_in)

                        if num_all > 0 and (num_in / num_all) > pass_rate:
                            csv_writer.writerow([filename, num_all, num_in])


def count_in_region_polygons(input_csv_path):
    count_dict = defaultdict(int)

    with open(input_csv_path, mode='r') as input_csv_file:
        csv_reader = csv.reader(input_csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            filename, num_all, num_in = row
            num_in = int(num_in)
            count_dict[num_in] += 1

    # Print the results
    for num_in, count in sorted(count_dict.items()):
        print(f'in region polygons number = {num_in} has {count} occurrences')



def select_and_copy_examples(input_csv_path, png_base_path, output_dir):
    # Define the selection criteria
    selection_criteria = {
        3: 8,
        4: 4,
        5: 4,
        6: 4
    }

    # Create a dictionary to store the selected examples
    selected_examples = defaultdict(list)

    with open(input_csv_path, mode='r') as input_csv_file:
        csv_reader = csv.reader(input_csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            filename, num_all, num_in = row
            num_in = int(num_in)

            if num_in in selection_criteria and len(selected_examples[num_in]) < selection_criteria[num_in]:
                selected_examples[num_in].append(filename)

    # Print selected filenames
    for num_in, files in selected_examples.items():
        print(f'in region polygons number = {num_in} examples:')
        for file in files:
            print(file)

    # Copy selected examples to the final directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for num_in, files in selected_examples.items():
        for file in files:
            clip_folder = file.split('-')[0]  # e.g., clip0 from clip0-y.gds
            src_file_path = Path(png_base_path) / clip_folder / (file)
            dest_file_path = output_dir / 'gds' / (file)

            try:
                shutil.copy(src_file_path, dest_file_path)
                print(f'Copied {src_file_path} to {dest_file_path}')
            except Exception as e:
                print(f'Error copying {src_file_path}: {e}')


from pathlib import Path
import shutil

def copy_and_rename_glp_files(source_dir, target_dir, mapping_filename='name_mapping.txt'):
    """
    Copies .glp files from source_dir to target_dir, renames them, and records the name mapping.
    
    :param source_dir: Path to the source directory
    :param target_dir: Path to the target directory
    :param mapping_filename: Filename for the name mapping file
    """
    # Ensure paths are Path objects and expand user directory symbols
    source_dir = Path(source_dir).expanduser()
    target_dir = Path(target_dir).expanduser()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Define the path for the mapping file
    mapping_file = target_dir.parent / mapping_filename

    # Initialize the counter
    counter = 1

    # Open the mapping file for writing
    with mapping_file.open('w') as f:
        # Iterate over all .glp files in the source directory
        for glp_file in source_dir.glob('*.glp'):
            # Define the new filename
            new_filename = f'M1_test{counter}.glp'
            new_filepath = target_dir / new_filename

            # Copy and rename the file
            shutil.copy(glp_file, new_filepath)

            # Record the name mapping
            f.write(f'{glp_file.name} -> {new_filename}\n')

            # Update the counter
            counter += 1

    print('Files copied and renamed. Name mapping saved to', mapping_file)



if __name__ == "__main__":
    # base_folder = '/Users/guojinc/Downloads/datasets/nvdla-samples'
    # process_gds_folders(base_folder)

    # Example usage
    # base_folder = '/Users/guojinc/Downloads/datasets/nvdla-samples'
    # delete_csv_files(base_folder)
    # Example usage
    # base_folder = '/Users/guojinc/Downloads/datasets/nvdla-samples'
    # filter_and_save_csv(base_folder)


    # Example usage
    # input_csv_path = '/Users/guojinc/Downloads/datasets/nvdla-samples/clip_all_0.8.csv'
    # count_in_region_polygons(input_csv_path)

    # Example usage
    # input_csv_path = '/Users/guojinc/Downloads/datasets/nvdla-samples/clip_all_0.8.csv'
    # png_base_path = '/Users/guojinc/Downloads/datasets/nvdla-samples-png'
    # gds_base_path = '/Users/guojinc/Downloads/datasets/nvdla-samples'
    # output_dir = '/Users/guojinc/Downloads/datasets/nvdla-samples-png/finalclips'
    # output_dir = '/Users/guojinc/Downloads/datasets/nvdla-samples/finalclips'

    # select_and_copy_examples(input_csv_path, gds_base_path, output_dir)

    # Example call
    glp_folder = '/Users/guojinc/Downloads/datasets/nvdla-samples/finalclips/glp'
    nvdla_folder = '/Users/guojinc/Downloads/datasets/nvdla-samples/finalclips/nvdla'
    copy_and_rename_glp_files(glp_folder, nvdla_folder)
