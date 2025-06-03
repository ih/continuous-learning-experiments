import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import sys
import os

def install_dependencies():
    dependencies = ["torch", "torchvision", "wandb", "matplotlib", "nbformat", "nbconvert", "ipykernel"]
    print(f"Installing dependencies: {', '.join(dependencies)}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def run_notebook(notebook_filename="mnist_cnn.ipynb"):
    print(f"Attempting to execute notebook: {notebook_filename}")
    try:
        with open(notebook_filename, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Check for ipykernel, which is needed by ExecutePreprocessor
        try:
            import ipykernel
            print("ipykernel is available.")
        except ImportError:
            print("ipykernel not found. Attempting to install...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ipykernel"])
            print("ipykernel installed. Please re-run the script if necessary.")
            # Depending on the environment, a restart might be needed for kernel to be found.
            # For this script, we'll proceed and hope it's picked up.

        # Configure the preprocessor
        # The kernel_name might need to match what's available in the environment.
        # 'python3' is a common default.
        ep = ExecutePreprocessor(timeout=1800, kernel_name='python3') # 30 minutes timeout

        print(f"Executing notebook: {notebook_filename}")
        # The second argument to preprocess can be used for passing resources, like metadata.
        # We'll pass the directory of the notebook so it can find other files if needed.
        notebook_dir = os.path.dirname(notebook_filename) or '.'
        ep.preprocess(nb, {'metadata': {'path': notebook_dir}})

        print(f"Notebook {notebook_filename} executed successfully!")
        # Optionally, save the executed notebook:
        # with open(f"executed_{notebook_filename}", 'w', encoding='utf-8') as f:
        #     nbformat.write(nb, f)
        return True, None

    except Exception as e:
        print(f"Error executing the notebook {notebook_filename}.")
        print(f"Exception: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        return False, e

if __name__ == "__main__":
    install_dependencies()
    success, error = run_notebook("mnist_cnn.ipynb")
    if success:
        print("Notebook execution test PASSED.")
    else:
        print(f"Notebook execution test FAILED. Error: {error}")
        sys.exit(1)
