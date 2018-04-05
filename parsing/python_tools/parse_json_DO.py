import json

f = open('doid.json', 'r')
doid_dict = json.load(f)
f.close()

w = open('doid_parsed.txt', 'w')
o = open('task_summary.txt', 'w')
l = open('task_list.txt', 'w')
icd_count = 0
total_icd_count = 0
do_count = 0
has_icd_link = False

for key, value in doid_dict.items():
  xrefs = []
  if key[:4] == 'DOID':
    do_count += 1
    key_ = key.encode('ascii')
    value_name = value['name'].encode('ascii')
    w.write(key_ + "\n")
    w.write("[Name] " + value_name + "\n")
    for key2, value2 in value['other'].items():
      if key2 == 'xref':
	has_icd_link = False
        for i in range(len(value2)):
  	  if value2[i][:5] == "ICD10":
	    total_icd_count += 1
	    has_icd_link = True
	    icd = value2[i].encode('ascii')
	    xrefs.append(icd)
  	if (len(xrefs) > 0):
          w.write("[Xrefs]\t")
	  for icd in xrefs:
            w.write(icd + "\t")
	    l.write(key_ + ": " + icd + "\n")
	w.write("\n")
      if key2 == 'hasExactSynonym':
        w.write("[Synonyms] ")
        for j in range(len(value2)):
          syn = value2[j].encode('utf-8')
          w.write(syn + "\t")
	w.write("\n")
    if has_icd_link == True:
      icd_count += 1
  w.write("\n")

l.close();
w.close();

o.write("How many DOIDs in total: " + str(do_count) + "\n")
o.write("How many DOID has ICD10 links: " + str(icd_count) + "\n")
o.write("How many ICD10 links in total: " + str(total_icd_count) + "\n")
o.close();
