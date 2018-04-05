import json
import requests

d = open('doid_parsed.txt', 'r')
doid_parsed = d.read()
d.close()

i = open('icd10cm_index_2018.json', 'r')
icd_data = json.load(i)
i.close()

w = ('match_do_icd.txt', 'w')

dataset = extractDict(icd_data.items(), 'letter', 'mainTerm')

part1 = "http://icd10api.com/?code="
part2 = "&desc=short&r=json"

for line in doid_parsed:
  #- Extract targets from doid_parsed
  if line == "\n":
    continue;
  if line[:4] == "DOID":
    do_code = line
  elif line[:7] == "[Name]":
    do_name = line[7:]
  elif line[:10] == "[Synonyms]":
    line = line[10:]
    do_syns = line.split("\t")
  elif line[:8] == "[Xrefs]":
    line = line[8:]
    icd_codes = line.split("\t")
  for icd_code in icd_codes:
    #- Request icd_code information and write on json file
    address = part1 + icd_code[8:] + part2
    r = requests.get(address)
    r.raise_for_status()
    r.jason()
    icd_name = r["Description"]
    w.write("[DO code] " + do_code + "\n")
    w.write("[DO name] " + do_name + "\n")
    w.write("[DO synonyms] ")
    for do_syn in do_syns:
      w.write(do_syn + "\t")
    w.write("\n" + "[ICD code] " + icd_code + "\n")
    w.write("ICD name] " + icd_name + "\n")
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
      w.write("No Match\n")
    w.write("\n")
  
w.close()

#- Functions -#
""" Define a function to extract mainTerm from icd10cm_index_2018.jason
    Return a list of dictionaries
"""
def extractDict(list_of_dict_pair, target_key1, target_key2):
  for key, value in list_of_dict_pair:
    if key == target_key1:
      for each_dict in value:
        for key2, value2 in each_dict:
          if key2 == target_key2:
            dict_list = value2
  return dict_list
  
""" Define a function that reqeusts ICD information to ICD10 API
    Write responses on file
"""
def requestICD(icd_code, output_file):
  part1 = "http://icd10api.com/?code="
  part2 = "&desc=short&r=json"
  address = part1 + icd_code[8:] + part2
  r = requests.get(address)
  r.raise_for_status()
  r.jason()
  with open(output_file, 'a') as outfile:
    json.dump(r, outfile)
  outfile.close()

""" Define a function that parse ICD json file
    Return name of given icd code
"""
def parseICDjson(input_json_file, icd_code):
  f = open(input_json_file, 'r')
  icd_dict = json.load(f)
  f.close()
  for key, value in icd_dict.items():
    if (value == icd_code[8:]):
      icd_name = value["Description"]
  return icd_name
