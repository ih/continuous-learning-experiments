import json
import subprocess
import sys

def execute_notebook_cells(notebook_path):
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            print(f"Executing cell {i+1}...")
            # Write cell source to a temporary .py file
            with open('temp_cell.py', 'w') as temp_f:
                # Filter out IPython magics and other non-Python lines
                source_lines = [line for line in cell['source'] if not line.startswith(('!', '%'))]
                temp_f.write("".join(source_lines))

            # Execute the temporary file
            # Use sys.executable to ensure we're using the same Python interpreter
            process = subprocess.run([sys.executable, 'temp_cell.py'], capture_output=True, text=True)

            if process.returncode != 0:
                print(f"Error executing cell {i+1}:")
                print(process.stdout)
                print(process.stderr)
                return False
            else:
                print(f"Cell {i+1} executed successfully.")
                if process.stdout:
                    print("Output:\n", process.stdout)
            print("-" * 30)
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python execute_notebook.py <notebook_path>")
        sys.exit(1)

    notebook_path = sys.argv[1]
    if execute_notebook_cells(notebook_path):
        print("Notebook executed successfully!")
    else:
        print("Notebook execution failed.")
        sys.exit(1)
