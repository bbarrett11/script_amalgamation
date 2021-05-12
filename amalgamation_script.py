import argparse
import subprocess
import io
import sys
from os.path import isfile, join
from os import listdir
import re


parser = argparse.ArgumentParser(description='Combine your JS scripts into one.')
parser.add_argument('--auto', action='store_true',default=False,help="Automatically scan html files")
parser.add_argument('--no_amalg', action='store_true',default=False,help="No script amalgamation")

args = parser.parse_args()

script_links = []
amalg_file_dir = "static/amalgamation_files/"
amalg_file_location = join("","static/amalg.js")

rm= f"rm {amalg_file_dir}*.js"
process = subprocess.Popen(rm.split(" "), stdout=subprocess.PIPE)
output, error = process.communicate()

if(not args.no_amalg):
    if(args.auto == True):
        # Automatically scan html files to find script references
        directory = "templates_edit"
        templates = [f for f in listdir(directory) if isfile(join(directory, f)) and join(directory,f).endswith(".html")]
        for template in templates:
            with open(join(directory,template)) as f:
                text = str(f.readlines())
                matches = re.findall("src=\"(.*?.js)\"",text)
                for x in matches:
                    if(x not in script_links):
                        script_links.append(x)
    else:
        # Use list for script references
        with open("scripts_to_amalg.txt") as f:
            script_links = f.readlines()
            script_links = [x.replace("\n","") for x in script_links]
            print("Downloading Scripts")

# Download/Copy scripts
for js_script in script_links:
    script_name = js_script.split("/")[-1]
    if("https:" in js_script.split("/")):
        # Online Scripts
        print(script_name)
        
        process = subprocess.Popen(f"curl -s {js_script} --output ./amalgamation_files/{script_name}".split(" "), stdout=subprocess.PIPE)
        output, error = process.communicate()
    else:
        print(script_name)
        # Local Scripts
        copy = f"cp {js_script} {amalg_file_dir}{script_name}"
        process = subprocess.Popen(copy.split(" "), stdout=subprocess.PIPE)
        output, error = process.communicate()


    # Combine scripts
    combine = f"cat {amalg_file_dir}*.js"
    process = subprocess.Popen(combine.split(" "), stdout=subprocess.PIPE)
    output, error = process.communicate()
    with io.open(f"{amalg_file_location}",'w',encoding='utf-8') as f:
        f.write(str(output,'utf-8'))
    
# Copy from working directory templates_edit to templates
rm= "rm templates/*.html"
copy = "cp templates_edit/*.html templates/"
process = subprocess.Popen(rm.split(" "), stdout=subprocess.PIPE)
output, error = process.communicate()
process = subprocess.Popen(copy.split(" "), stdout=subprocess.PIPE)
output, error = process.communicate()

if(not args.no_amalg):
    # Replace all instances of scripts with combined script
    for script in script_links:
        replace = f"sed -i 's|{script}|{amalg_file_location}|g' templates/*.html"
        process = subprocess.Popen(replace.split(" "), stdout=subprocess.PIPE)
        output, error = process.communicate()
    print(f"Combined into {amalg_file_location}")