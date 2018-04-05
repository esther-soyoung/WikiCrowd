import pronto

f = open('doid.json', 'w')
o = open('doid.obo', 'w')

ont = pronto.Ontology('https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.owl')

o.write(ont.obo)
f.write(ont.json)

f.close()
o.close()
