import re
import subprocess
import math
from sys import platform
import numpy
from stl import mesh

def slicedweight(pathtofile, density):  
    if platform == 'win32':
        cmd = r'cd C:\Program Files\Ultimaker Cura 3.6 && CuraEngine slice -v -j "C:\Program Files\Ultimaker Cura 3.6\resources\definitions\wanhao_d6.def.json" -o "C:\Users\abbro\Documents\Visual Studio 2017\Projects\Cubic3D\Cubic3D\output.gcode" -s center_object=true -s adhesion_type=skirt -s infill_line_distance=2.4 -s support_enable=false -l "{0}"'.format(pathtofile)
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        string = result.decode('utf-8')
        search = re.compile('(?<=Filament\s[(]mm\^3[)]:\s)[0-9]+')
        filamentvolume = search.findall(string)
        mass = int(filamentvolume[0])*density/1000
        roundmass = int(math.ceil(mass))
        return (string,roundmass)
    else:
        cmd = r'cd /home/curafiles/CuraEngine/build && ./CuraEngine slice -v -j "../resources/definitions/wanhao_d6.def.json" -o "/home/cubic/media/test.gcode" -s center_object=true -s adhesion_type=skirt -s infill_line_distance=2.4 -s support_enable=false -l "{0}"'.format(pathtofile)
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        string = result.decode('utf-8')
        search = re.compile('(?<=Filament\s[(]mm\^3[)]:\s)[0-9]+')
        filamentvolume = search.findall(string)
        mass = int(filamentvolume[0])*density/1000
        roundmass = int(math.ceil(mass))
        return (string,roundmass)

def setscale(path,current,required):
    my_mesh = mesh.Mesh.from_file(path)
    my_mesh.vectors=required*my_mesh.vectors/current
    my_mesh.save(path)