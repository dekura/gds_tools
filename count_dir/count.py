import os
import shutil
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Count the number of files corresponding to a certain X value
def count_files_for_x(x, base_path):
    file_count = 0
    pattern = re.compile(rf'clip{x}-\d+\.gds')
    for filename in os.listdir(base_path):
        if pattern.match(filename):
            file_count += 1
    return x, file_count

def stat():
    base_path = "/Users/guojinc/Downloads/datasets/nvdla"
    x_range = range(0, 32)
    results = {}

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_x = {executor.submit(count_files_for_x, x, base_path): x for x in x_range}
        for future in as_completed(future_to_x):
            x = future_to_x[future]
            try:
                x, file_count = future.result()
                results[x] = file_count
            except Exception as exc:
                print(f'X={x} generated an exception: {exc}')

    for x in sorted(results.keys()):
        print(f'clip{x}: {results[x]} files')


# Copy 100 randomly selected files from the clipX directory to the destination directory.
def sample_and_copy_files(x, base_path, sample_path, sample_size=100):
    pattern = f'clip{x}-'
    files = [f for f in os.listdir(base_path) if f.startswith(pattern) and f.endswith('.gds')]
    sampled_files = random.sample(files, sample_size)
    for file in sampled_files:
        src_file = os.path.join(base_path, file)
        dst_file = os.path.join(sample_path, file)
        shutil.copyfile(src_file, dst_file)
    return x, len(sampled_files)

def sample():
    base_path = "/Users/guojinc/Downloads/datasets/nvdla"
    sample_path = "/Users/guojinc/Downloads/datasets/nvdla-samples"
    os.makedirs(sample_path, exist_ok=True)
    x_range = range(0, 32)

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_x = {executor.submit(sample_and_copy_files, x, base_path, sample_path): x for x in x_range}

        for future in as_completed(future_to_x):
            x = future_to_x[future]
            try:
                x, sampled_count = future.result()
                print(f'clip{x}: Sampled and copied {sampled_count} files')
            except Exception as exc:
                print(f'X={x} generated an exception: {exc}')


# Move the file to the corresponding clipX folder
def move_files_to_clip_folders(x, base_path):
    pattern = re.compile(rf'clip{x}-\d+\.gds')
    clip_folder = os.path.join(base_path, f'clip{x}')
    os.makedirs(clip_folder, exist_ok=True)

    for filename in os.listdir(base_path):
        if pattern.match(filename):
            src_file = os.path.join(base_path, filename)
            dst_file = os.path.join(clip_folder, filename)
            shutil.move(src_file, dst_file)
    return x

def move():
    base_path = "/Users/guojinc/Downloads/datasets/nvdla-samples"
    x_range = range(0, 32)

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_x = {executor.submit(move_files_to_clip_folders, x, base_path): x for x in x_range}

        for future in as_completed(future_to_x):
            x = future_to_x[future]
            try:
                future.result()
                print(f'clip{x}: Files moved successfully')
            except Exception as exc:
                print(f'X={x} generated an exception: {exc}')

if __name__ == "__main__":
    move()
