# WikiCrowd
## Synopsis

Wikidata is a community-maintained database, and we have been loading data on biomedical topics (primarily genes, drugs, and diseases).  One data source is the Disease Ontology (DO), which defines diseases and their relationships to other diseases. DO also maintains links to other disease terminologies like the International Classification of Disease (ICD) (which has two commonly-used versions, ICD-9 and ICD-10).  The links in DO to ICD are typically maintained as non-specific cross-references (also known as “dbxrefs”), but in some cases, the ICD entry is more general or specific than the linked DO entry.  We would like to create a web interface that allows Wikidata members to make these mappings more precise by specifying one of three mapping types -- “exact match”, “broad match” and “narrow match”.

## Project details
Straw man workflow
This workflow is roughly based on what’s available from the Wikidata Mix-n-match tool.

Extract all DO mappings to ICD (from Wikidata or from the DO OWL file; use latest releases here)
For cases where DO name exactly matches ICD name, infer an “exact match” link (ICD data here: ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2018/ICD-10-CM-Codes-Tables-and-Index-2018.zip) 
Use remaining cases to populate a web portal
User logs in using Wikidata oauth
User is shown information about one DO entry and its mapping to ICD (show name, description, aliases, parents, childrens, and “exclusions”)
User selects “exact match”, “broad match”, or “narrow match” (with an optional comment on why)
Web app writes new statement to Wikidata
User is shown next 

An existing Wikidata monitoring application would then detect that addition and create a monthly report for review by DO curators for possible inclusion in the official DO release.

## Implementation details
Use a JSON file format as intermediate that has all the relevant info in step #3b above  
  
[  
{  
  “Id”: “DOID:1234”,  
  “Parent”: [“DOID:23445”,”DOID:987987”],  
   “Description”: “swollen left big toe”,  
   “Aliases”:   
},  
…  
]  
### Examples

systemic lupus erythematosus  
DOID:9074 (Link)  
Maps to ICD-10-CM Diagnosis Codes  
M32: Systemic lupus erythematosus (SLE)  
M32.9: Systemic lupus erythematosus, unspecified  
Desired outcome: generic “dbxref” changed to “exact match” for M32  
  
Brunner Syndrome  
DOID:0060693 (link)  
Maps to ICD-10-CM Diagnosis Code E70.8  
Name: Other disorders of aromatic amino-acid metabolism  
Desired outcome: generic “dbxref” changed to “broad match”  
  
Later extensions  
Can also be applied to DO mappings to MeSH  
Can also extract mappings from Wikidata (there are many that are in there, not from DO) For example from syphilis, a lot of ICD9 mappings from english wikipedia  
  
### An example for a proposed feature:
Currently on the syphilis wikidata item, there are several ICD9 mappings. Many, however are not exact matches to syphilis, but are narrower. Take, for example 090, which is "Early syphilis symptomatic". It would be nice, for when a user selects that a term is a narrowMatch, it would present the user a list of diseases that are children of the current disease, and asks if any of them are a better match. So, for example, with "Early syphilis symptomatic", it would present all the children of syphilis (either from the DO browser (link), or from a sparql query (link)), and the user would see: primary syphilis (alias: early symptomatic syphilis), which is a better match than syphilis.


