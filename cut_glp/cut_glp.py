import os

def modify_and_save_glp_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.glp'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as file:
                content = file.read()
            
            modified_content = modify_glp_content(content)
            
            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, 'w') as file:
                file.write(modified_content)

def modify_glp_content(content):
    lines = content.split('\n')
    modified_lines = []

    for line in lines:
        if any(char.isdigit() for char in line):
            modified_line = ' '.join([str(min(1700, max(300, int(word)))) if word.isdigit() else word for word in line.split()])
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    return '\n'.join(modified_lines)

input_directory = '/Users/guojinc/intern/github/DiffOPC/benchmark/nvdla'
output_directory = '/Users/guojinc/intern/github/DiffOPC/benchmark/nvdla_cut'

modify_and_save_glp_files(input_directory, output_directory)
