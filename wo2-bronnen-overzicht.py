#!/usr/bin/env python3
import csv,json,sys,re
from operator import itemgetter

# voor de SQL query: zie data/sql

basename="Bronnenoverzicht Tweede Wereldoorlog"
input_filepath="data/sql/sql-result-combi.csv"
output_json_filepath=f"data/result/{basename}.json"

dict_met_toppen = {} # geindexteerd op ID (dus TOP_ID)

for row in csv.DictReader(open(input_filepath)): # dit is een combinatie van 'CSV uit SQL queries/1,2,3 en 4.csv
	row = dict(row)

	if row["AET"] in ("PAP", "TSCNI"): # aet
		continue

	if not row["TOP_ID"] in dict_met_toppen:

		code = row["TOEGANG_BESCHRIJVING"].split(" ")[0]

		#add 0's to be able to sort on toegangsnummer
		code_splitted = code.split('-')
		code_left = ("0"*4 + code_splitted[0])[-4:]
		code_right = ("0"*4 + (code_splitted[1] if len(code_splitted)>1 else ""))[-4:]
		sortcode = code_left + "-" + code_right

		row["TOEGANG_BESCHRIJVING"] = row["TOEGANG_BESCHRIJVING"].replace(code+" ", "").strip()
		row["TOEGANG_BESCHRIJVING"] = re.sub(r', aanvulling.*| Vanwege .*','',row["TOEGANG_BESCHRIJVING"])

		dict_met_toppen[row["TOP_ID"]] = { 
			"toegangstitel": row["TOEGANG_BESCHRIJVING"],
			"code": code,
			"sortcode": sortcode
		}	

		dict_met_toppen[row["TOP_ID"]]["items"] = {}

	if not row["BOVEN_ID"] in dict_met_toppen[row["TOP_ID"]]["items"]:
		
		# strip rubriek code from title
		rubriek_code = row["BOVENLIGGENDE_BESCHRIJVING"].split(". ")[0]
		rubriek_code += "."
		if rubriek_code[0].isdigit():
			row["BOVENLIGGENDE_BESCHRIJVING"] = row["BOVENLIGGENDE_BESCHRIJVING"].replace(rubriek_code, "").strip()

		dict_met_toppen[row["TOP_ID"]]["items"][row["BOVEN_ID"]] = { 
			"rubriek_code": rubriek_code,
			"bovenliggende_beschrijving": row["BOVENLIGGENDE_BESCHRIJVING"],
			"items": {}
		}

	code = row["STUK_BESCHRIJVING"].split(" ")[0].replace(".","")
	row["STUK_BESCHRIJVING"] = row["STUK_BESCHRIJVING"].replace(code+".", "").strip()

	dict_met_toppen[row["TOP_ID"]]["items"][row["BOVEN_ID"]]["items"][row["ID"]] = {
		"code": code,
		"beschrijving": row["STUK_BESCHRIJVING"],
		"aet": row["AET"], # archiefeenheidsoort
		"GUID": row["GUID"]
	}

# converteer 'dict' met toppen naar een 'list' met toppen om te kunnen sorteren op toegangscode
# dit zou wellicht ook met een OrderedDict kunnen
lijst_met_toppen = []
for top in dict_met_toppen.values():
	lijst_met_toppen.append(top)
lijst_met_toppen = sorted(lijst_met_toppen, key=itemgetter('sortcode')) 

json.dump(lijst_met_toppen, open(output_json_filepath, "w"), indent=2)

print('<link href="style.css" rel="stylesheet">')
print('<main>')
print('<h1>Bronnenoverzicht Tweede Wereldoorlog<br/>Het Utrechts Archief</h1>')

print('<h2>Inhoudsopgave</h2>')
print('<table class="toc" width="100%">')
print('<tr><td class="bold">Toegang</td><td class="bold">Beschrijving</td></tr>')
for top in lijst_met_toppen:
	toegangstitel = top["toegangstitel"]
	code = top["code"]
	print(f'<tr><th><a href="#{code}">{code}</a>.</th><td>{toegangstitel}</td></tr>') # begin top item
print('</table>')

for top in lijst_met_toppen:

	toegangstitel = top["toegangstitel"]
	code = top["code"]
	print(f'<div class="top"><a name="{code}"/><a href="http://hualab.nl/{code}">Toegang {code}</a>. {toegangstitel}</div>') # begin top item

	for boven_key,boven in top["items"].items():
		bovenliggende_beschrijving = boven["bovenliggende_beschrijving"]
		print(f'<div class="bovenliggend">{bovenliggende_beschrijving}</div>') # begin van bovenliggende items

		print('<table class="items" width="100%">')
		for stuk_key,stuk in boven["items"].items():
			stuk_beschrijving = stuk["beschrijving"]
			code = stuk["code"]
			guid = stuk["GUID"]
			print('<tr class="stuk">')
			print(f'<th><a href="https://hetutrechtsarchief.nl/collectie/{guid}">{code}</a>.</th><td>{stuk_beschrijving}</td>')
			print('</tr>')
		print('<table>')

print('</main>')
print('<marquee>einde...</marquee>')
	