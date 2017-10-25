import re
import subprocess
import math
from sys import platform

def slicedweight(pathtofile, density):  
    if platform == 'win32':
        cmd = r'cd C:\Program Files\Cura 2.7 && CuraEngine slice -v -j "C:\Program Files\Cura 2.7\resources\definitions\fdmprinter.def.json" -o "C:\Users\abbro\Documents\Visual Studio 2017\Projects\Cubic3D\Cubic3D\output.gcode" -s machine_height=175 -s machine_depth=200 -s machine_width=200 -s material_diameter=1.75 -s center_object=true -s adhesion_type=skirt -s infill_line_distance=2.4 -s support_enable=true -l "{0}"'.format(pathtofile)
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        string = result.decode('utf-8')
        search = re.compile('(?<=Filament:\s)[0-9]+')
        filamentvolume = search.findall(string)
        mass = int(filamentvolume[0])*density/1000
        roundmass = int(math.ceil(mass))
        return (string,roundmass)
    else:
        cmd = r'cd app && chmod -R a+rwx CuraEngine && cd CuraEngine/build && CuraEngine slice -v -j "../resources/definitions/fdmprinter.def.json" -o "../output.gcode" -s machine_width=200 -s material_diameter=1.75 -s center_object=true -s adhesion_type=skirt -s infill_line_distance=2.4 -s support_enable=true -l "{0}"'.format(pathtofile)
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        string = result.decode('utf-8')
        print(string)
        search = re.compile('(?<=Filament:\s)[0-9]+')
        filamentvolume = search.findall(string)
        mass = int(filamentvolume[0])*density/1000
        roundmass = int(math.ceil(mass))
        return (string,roundmass)