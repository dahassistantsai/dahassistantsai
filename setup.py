import subprocess
import sys
import os

def install_requirements():
    print('Installing dependencies from requirements.txt...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def run_app():
    print('Starting Flask app...')
    subprocess.check_call([sys.executable, 'app.py'])

if __name__ == '__main__':
    install_requirements()
    run_app()
