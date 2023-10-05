import subprocess
import platform
import os

# check the current operating system
current_os = platform.system()

# set the python command based on the operating system
if current_os == 'Windows':
    commands1 = ['py -3 -m venv venv',
            'venv\\scripts\\activate']
    commands2 = ['python manage.py migrate', 'python loadData.py', 'python manage.py runserver']
else:
    commands1 = ['python3 -m venv venv',
            'source venv/bin/activate']
    commands2 = ['python3 manage.py migrate', 'python3 loadData.py', 'python3 manage.py runserver']

os.chdir('Nachhilfeverwaltung')

for command in commands1:
    try:
        subprocess.run(command, shell=True)
        print(f'Command "{command}" executed successfully')
    except:
        print("Error executing Script")
        break

os.chdir('nachhilfeverwaltung')
subprocess.run('pip install -r requirements.txt', shell=True)
os.chdir('..')

for command in commands2:
    try:
        subprocess.run(command, shell=True)
        print(f'Command "{command}" executed successfully')
    except:
        print("Error executing Script")
        break
