import re, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from performance_tagging import tag_line, MANUAL_OVERRIDES
ROOT = pathlib.Path(__file__).resolve().parents[1]
CASE = ROOT / chr(103)+chr(97)+chr(109)+chr(101) / chr(99)+chr(97)+chr(115)+chr(101)+chr(52)+chr(95)+chr(53)+chr(95)+chr(98)+chr(111)+chr(97)+chr(116)+chr(46)+chr(114)+chr(112)+chr(121)
