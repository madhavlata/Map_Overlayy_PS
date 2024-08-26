import subprocess
import sys

def run_command(command):
    """Run a shell command and check for errors."""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        sys.exit(result.returncode)
    print(f"Command output: {result.stdout}")

def main():
    # Install packages from requirements.txt
    run_command('pip install -r requirement.txt')
    
    # Run the Python scripts in the specified order
    scripts = [
        'a_tag.py',
        'anchor.py',
        'merge.py',
        'question_generator.py',
        'relevant_link.py'
    ]
    
    for script in scripts:
        run_command(f'python {script}')

if __name__ == "__main__":
    main()
