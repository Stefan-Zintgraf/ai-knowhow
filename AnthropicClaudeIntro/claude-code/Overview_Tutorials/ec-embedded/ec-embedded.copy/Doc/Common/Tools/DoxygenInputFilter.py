import sys
import re

filename = sys.argv[1]
with open(filename, "r") as f:
  for line in f:
    # "struct _XYZ*;" -> "XYZ*;"
    line_filtered = re.sub(r"struct\s+_([A-Za-z0-9_]+)(\s*\*)", r"\1\2", line)
    sys.stdout.write(line_filtered)
    
#    if line != line_filtered:
#      print(f"'{line.strip()}' -> '{line_filtered.strip()}'", file=sys.stderr)
    
