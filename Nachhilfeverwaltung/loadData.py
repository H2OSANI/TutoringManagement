import subprocess
import platform

# list of json files to be loaded
json_files = ['faecher_data.json', 'group_data.json', 'user_data.json', 
              'person_detail_data.json', 'personen_faecher_data.json', 
              'sender_data.json', 'settings_content_data.json']

# check the current operating system
current_os = platform.system()

# set the python command based on the operating system
if current_os == 'Windows':
    python_cmd = 'python'
else:
    python_cmd = 'python3'

for json_file in json_files:
    subprocess.run([python_cmd, 'manage.py', 'loaddata', json_file])
    print(f'{json_file} has been loaded successfully')
