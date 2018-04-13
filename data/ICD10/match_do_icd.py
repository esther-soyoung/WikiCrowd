import json
from requests import *

#- Functions -#
""" Reqeusts ICD information to ICD10 API
    Return ICD name of input ICD code
"""
def requestICD(icd_code):
  part1 = "http://icd10api.com/?code="
  part2 = "&desc=short&r=json"
  address = part1 + icd_code[9:] + part2
  r = requests.get(address)
  r.raise_for_status()
  icd_name = r["Description"]
  return icd_name

""" Define a function that parse ICD json file
    Return name of given icd code

def parseICDjson(input_json_file, icd_code):
  f = open(input_json_file, 'r')
  icd_dict = json.load(f)
  f.close()
  for key, value in icd_dict.items():
    if (value == icd_code[8:]):
      icd_name = value["Description"]
  return icd_name
"""


""" Compare DO name and ICD name by string compare
    Return appropriate message in string
"""
def compareName(do_name, icd_name, do_syns):
  icd_name.lower()
  do_name.lower()
  if icd_name == do_name:
    exact_match = True
  else:
    exact_match = False
  for do_syn in do_syns:
    do_syn.lower()
    if icd_name == do_sym:
      exact_match = True
  if (exact_match):
    return "Exact Match"
  return "Not an Exact Match"
  

#- Main -#
d = open('doid_parsed.txt', 'r')
#doid_parsed = d.read()

i = open('icd10cm_index_2018.json', 'r')
icd_data = json.load(i)
i.close()

w = open('match_do_icd.json', 'w')
w.write("{\n")

part1 = "http://icd10api.com/?code="
part2 = "&desc=short&r=json"

for line in d:
  #- Extract targets from doid_parsed
  icd_codes = []
  do_syns = []
  done = False
  if line == "\n":
    continue;
  if line[:4] == "DOID":
    do_code = line
  elif line[:6] == "[Name]":
    do_name = line[7:]
  elif line[:10] == "[Synonyms]":
    line = line[10:]
    do_syns = str.split(line, "\t")
  elif line[:7] == "[Xrefs]":
    line = line[8:]
    icd_codes = str.split(line, "\t")
    done = True

  if done:
    w.write("\t" + do_code + ":{\n")
    w.write("\t\tDO name: " + do_name + ",\n")
    w.write("\t\tSynonyms:[\n")
    for do_syn in do_syns:
      w.write("\t\t\t" + do_syn + ",\n")
    w.write("\t\t],\n")
    w.write("\t\tICD match:[\n")
    for icd_code in icd_codes:
      icd_name = requestICD(icd_code)
      w.write("\t\t\t{\n")
      w.write("\t\t\t\tICD code: " + icd_code + ",\n")
      w.write("\t\t\t\tICD name: " + icd_name + ",\n")
      w.write("\t\t\t\tMatch Type: " + compareName(do_name, icd_name, do_syns) + "\n")
      w.write("\t\t\t},\n")
    w.write("\t\t]\n")
    w.write("\t}\n")
    done = False


"""
#  if len(icd_codes)==0:
#    print ("Shit")
  for icd_code in icd_codes:
    #- Request icd_code information and write on json file
    address = part1 + icd_code[9:] + part2
    r = requests.get(address)
    r.raise_for_status()
#    r.jason()
    icd_name = r["Description"]
    w.write("[DO code] " + do_code + "\n")
    w.write("[DO name] " + do_name + "\n")
    w.write("[DO synonyms] ")
    for do_syn in do_syns:
      w.write(do_syn + "\t")
    w.write("\n" + "[ICD code] " + icd_code + "\n")
    w.write("[ICD name] " + icd_name + "\n")
    #- Compare icd_name with do_name and do_syns
    exact_match = False
    icd_name.lower()
    do_name.lower()
    if icd_name == do_name:
      exact_match = True
    for do_syn in do_syns:
      do_syn.lower()
      if icd_name == do_sym:
        exact_match = True
    #- Write match information on w
    w.write("[Match] ")
    if exact_match:
      w.write("Exact Match\n")
    else:
      w.write("Not an Exact Match\n")
    w.write("\n")
"""

 
w.write("}")
w.close()
d.close()
