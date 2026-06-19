import re
import math
import subprocess
import tempfile
import os
from sys import platform

PRUSA_SLICER   = '/usr/bin/prusa-slicer'
PRINTER_CONFIG = '/home/curafiles/cubic3d_prusa.ini'

# PrusaSlicer appends these comment lines near the end of the gcode file:
#   ; filament used [g] = 13.35
#   ; filament used [cm3] = 10.68
_GRAMS_RE = re.compile(r';\s*filament used \[g\]\s*=\s*([0-9]+(?:\.[0-9]+)?)')
_CM3_RE   = re.compile(r';\s*filament used \[cm3\]\s*=\s*([0-9]+(?:\.[0-9]+)?)')

_TAIL_BYTES = 16384   # stats block always fits in last 16 KB


def slicedweight(pathtofile, density):
    """
    Slice *pathtofile* (STL) with PrusaSlicer and return (log_string, mass_grams).

    density  – material density in g/cm³ (same as g/mL).
    mass is in grams, rounded up to the nearest gram.

    Return signature is identical to the old implementation so all callers
    in models.py continue to work without change.
    """
    if platform in ('win32', 'darwin'):
        # Local dev fallback: estimate mass from mesh volume
        from stl import mesh
        my_mesh = mesh.Mesh.from_file(pathtofile)
        volume_mm3 = float(abs(my_mesh.get_mass_properties()[0]))
        mass = volume_mm3 * density / 1000.0
        return ('local-dev-estimate', int(math.ceil(mass)))

    # Write gcode to a temp file so we don't pollute media/
    gcode_out = tempfile.mktemp(suffix='.gcode')
    try:
        result = subprocess.run(
            [
                PRUSA_SLICER,
                '--export-gcode',
                '--load', PRINTER_CONFIG,
                '--filament-density', str(density),
                '--output', gcode_out,
                pathtofile,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        output = result.stdout.decode('utf-8', errors='replace')

        if result.returncode != 0:
            raise RuntimeError(
                'PrusaSlicer exited with code {}.\nOutput:\n{}'.format(
                    result.returncode, output))

        # PrusaSlicer writes filament stats near the END of the gcode file
        file_size = os.path.getsize(gcode_out)
        read_from = max(0, file_size - _TAIL_BYTES)
        with open(gcode_out, 'r', errors='replace') as f:
            f.seek(read_from)
            gcode_tail = f.read()

        # Prefer the direct grams value; fall back to cm³ × density
        m = _GRAMS_RE.search(gcode_tail)
        if m:
            mass = float(m.group(1))
        else:
            m = _CM3_RE.search(gcode_tail)
            if not m:
                raise RuntimeError(
                    'PrusaSlicer did not report filament volume.\nOutput:\n{}'.format(output))
            mass = float(m.group(1)) * density

        return (output, int(math.ceil(mass)))

    finally:
        try:
            os.unlink(gcode_out)
        except OSError:
            pass


def getmass(pathtofile, density):
    """Convenience wrapper used by ThingOrders.thing_price()."""
    _, mass = slicedweight(pathtofile, density)
    return mass


def setscale(path, current, required):
    from stl import mesh
    my_mesh = mesh.Mesh.from_file(path)
    my_mesh.vectors = required * my_mesh.vectors / current
    my_mesh.save(path)
