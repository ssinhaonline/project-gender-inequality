#!/bin/bash
for file in ../fixtures/all_jsons/*.json
do
	echo "Mongo Import: ${file}"
	mongoimport --db rmpdb --collection profs --file "$file"
done