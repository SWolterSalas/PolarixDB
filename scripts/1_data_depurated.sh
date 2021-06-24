#!/bin/bash
# En la carpeta que quieres descargar todos los datos actualizados correr:
pwd
cd ..

mkdir antarcticDB

cd antarcticDB

#wget -r -N -l inf ftp://amrc.ssec.wisc.edu/pub/aws/q1h/ #AWS
#wget -r -N -l inf ftp://ftp.bas.ac.uk/src/SCAR_EGOMA/SURFACE/ #SCAR
#wget -r -N -l inf ftp://ftp.bas.ac.uk/src/SCAR_EGOMA/POLENET_AWS/ #POLENET

mkdir Data_Stations
mkdir Metadata_Stations

cd amrc.ssec.wisc.edu/pub/aws

mkdir datos_compilados
mkdir datos_compilados1
mkdir datos_compilados2

cd q1h

rm -r 1987
rm -r 1995
rm -r 1996
rm -r 1997
rm -r 1998
rm -r 1999
rm -r 2000

ls | grep -v 'lista'  > lista_fechas.dat

cat lista_fechas.dat | while read lines 
do
	#echo $lines
	cd $lines
	rm *.dat
	ls | grep -o '^[a-z][a-z][a-z][2][0][0-9][0-9]' | uniq > lista.list
	cat lista.list | while read line; do cat $line* | 
	grep -v -e 'Year' -e 'Lat' >> $line.dat ; done #datos
	mv *.dat ../../datos_compilados1
	rm lista.list
	
	cd ..
done

cd ../datos_compilados1

ls | grep -v 'lista' | grep -o '^[a-z]..' | uniq > lista_estaciones.list

cat lista_estaciones.list | while read line
do
	cat $line* >> $line
	
done

#echo termine1

cat lista_estaciones.list | while read line
do
	mv $line ../datos_compilados2
done

#echo termine2

cd ../datos_compilados2

ls | grep -v 'lista' > lista_estaciones.list

cat lista_estaciones.list | while read line; do 
	#echo $line
	cat $line | awk '{print $1,$3,$4,$5,$6,$7,$8,$9,$10}' | 
	sed 's/ /,/g' |  sed -E 's/(^[0-9]{4},)([0-9],)/\10\2/g' | 
	sed -E 's/([0-9]{4},)([0-9]{2},)([0-9],)/\1\20\3/g' | 
	sed -E 's/([0-9]{4}),([0-9]{2}),([0-9]{2})/\1-\2-\3/g' | 
	sed -E 's/(,[0-9][0-9])([0-9][0-9],)/\1:\2/g' | 
	sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2}),/\1-\2-\3 /g' | 
	sed -E 's/(444.0)//g' | 
	sed -E $'1i\\\nDates,Temperature_(Celsius),Pressure_(hPa),Wind_Speed_(m/s),Wind_Direction,Relative_Humidity_(%)\n' > $line.csv ; done   

mv *.csv ../datos_compilados/ 

cd ../
rm -r datos_compilados2
rm -r datos_compilados1
cd q1h
rm lista_fechas.dat

echo 'Finish Data AWS-1'
##########

cd ../

mkdir metadataAWS

cd q1h/

ls | grep '[2][0][0-9][0-9]' > lista_estaciones.list

cat lista_estaciones.list | while read lines 
do
	#echo $lines
	cd $lines
	ls | grep -o '^[a-z][a-z][a-z][2][0][0-9][0-9]' | uniq > alista.list
	cat alista.list | while read line; 
	do
		co=1
		touch metadataAWS$lines.dat
		for i in 1 2 3 4 5 6 7 8 9 10 11 
		do
			#echo $line
			file1=${line}0${co}q1h.txt
			file2=${line}${co}q1h.txt
			#echo $file2
			if [[ ! -f $file1 ]] && [[ ! -f $file2 ]]
			then
				co=$((co + 1))
				#echo $file1
				#echo $file2
				#echo $co
				continue
			
			elif [[ -f $file1 ]] 
			then
				#echo "encontre1"
				head -n 2 $file1 >> metadataAWS$lines.dat
				#echo $file1
				co=1
				break
			elif [[ -f $file2 ]]
			then
				#echo "encontre2"
				head -n 2 $file2 >> metadataAWS$lines.dat
				co=1
				#echo $file2
				break
			fi
		done
	done #metadata
	#cat alista.list | while read line; do cat $line* | grep -v -e 'Year' -e 'Lat'  >> $line.dat ; done #datos
	mv metadata*.dat ../../metadataAWS/
	cd ..
done

cd ../metadataAWS

ls | grep -v '_list.list' > metadata_list.list 

cat metadata_list.list | while read lines; do 
	cat $lines | 
	sed -E 's/(Year:.*)(ID:)/\2/g' | 
	sed -E 's/(ID:) (...)(.*)(Name:)/\2,\4/g' | 
	sed -E 's/(Name:) (.*[a-z])/\2,/g' | 
	sed -E 's/(Name:) (.*[A-Z].*[0-9])/\2,/g' | 
	sed -E 's/(Name:) (.*[A-Z])/\2,/g' | 
	sed -E 's/(Lat:) (......)(.*)(Lon:)/\2,\4/g' | 
	sed -E 's/(Lon:) (.*[EW]).*(Elev:)/\2,/g' | 
	sed -E 's/(...,)([A-Z].*) ([A-Z].*)/\1\2_\3/g' | 
	sed 's/ //g' | sed -E 's/(.*[A-Z]{4},)(.*)/\1/g' | 
	sed 's/(//g' | sed 's/)//g' | sed 's/TT!//g' | 
	sed -E 's/([A-Z]{3},.*,)/\1/g' |  tr -d '\n' | 
	tr -d '\r\n'  >> metadataAWS.dat; done

cat metadataAWS.dat | sed -E 's/([0-9]m)([A-Z]{3},)/\1\n\2/g' > metadataAWS.det

cat metadataAWS.det | sort -u | sed 's/,/\t/g' | 
awk '!a[$1]++' | sed $'1i\\\nID,Name,Latitude,Longitude,Altitude\n' | 
sed 's/\t/,/g' > metadataAWS.txt

rm *.dat
rm *.det
rm *.list
cd ../q1h
rm *.dat
rm *.list

echo 'Finish Data AWS-2'
#######

cd ../datos_compilados

for file in *  
do 
	basename=$(tr '[:lower:]' '[:upper:]' <<< "${file%.*}") 
   	#echo $basename
   	mv "$file" "$basename"
done

for file in *  
do 
   	#echo $file
   	newname=$(grep -m 1 "${file}" ../metadataAWS/metadataAWS.txt | 
   	sed 's/,/\t/g' | 
   	sed 's/\.//g' | 
   	sed 's/?//g' | 
   	awk '{print $2}')
   	#echo $newname
   	mv "$file" "$newname.csv"
done

cd ..

mv datos_compilados AWS
mv AWS ../../../Data_Stations

cd metadataAWS
mv metadataAWS.txt ../../../../Metadata_Stations/

cd ..

rm -r metadataAWS
#cd ../../../../../
#mv antarcticDB/amrc.ssec.wisc.edu/pub/aws/

echo 'Finish Data AWS-3'
#####

cd ../../../ftp.bas.ac.uk/src/SCAR_EGOMA/SURFACE
mkdir SCAR

for archivo in *.dat
do
	TEXTO=${archivo%.dat}
	tail -n +8 $TEXTO\.dat | 
	sed -E 's/([0-9]{4}) ([0-9]{2}) ([0-9]{2})/\1-\2-\3/g' | 
	sed 's/ /,/g' | sed -E 's/(,[0-9][0-9]),([0-9][0-9],)/\1:\2/g' | 
	sed -E 's/(-[0-9][0-9]-[0-9][0-9]),([0-9][0-9]:[0-9][0-9],)/\1 \2/g' | 
	sed -E 's/([0-9],),*,([0-9])/\1\2/g' | 
	sed -E 's/([0-9],),*,(-[0-9])/\1\2/g' | 
	sed 's/,,*,/,/g' |  
	#sed 's/-999//g' | #sed 's/(-999)//g' |
	sed 's/,/\t/g' | awk '{printf "%s %s %.2f %.2f %.2f %i\n", $1,$2,$5,$4,$6*0.514444,$7}' | 
	sed 's/-999.00//g'| sed -E 's/-513.93//g'| sed 's/-999//g'| 
	sed -E $'1i\\\nDates,Temperature_(Celsius),Pressure_(hPa),Wind_Speed_(m/s),Wind_Direction\n' | 
	sed 's/ /,/g' | sed -E 's/(-[0-9][0-9]-[0-9][0-9]),([0-9][0-9]:[0-9][0-9],)/\1 \2/g' > $TEXTO\.csv
	mv $TEXTO\.csv ./SCAR
done

mv SCAR ../../../../Data_Stations

ls | grep -v 'list' > lista.list
cat lista.list | while read lines ; do head -n 3 $lines >> metadataSCAR.temp.txt; done
cat metadataSCAR.temp.txt | grep -v 'Operated*' | sed 's/latitude//g' | sed 's/longitude//g' | sed 's/height//g' | sed 's/ /,/g' | sed 's/,,/,/g' | sed -E 's/(.*[0-9]m).*/\1,/g' | tr -d '\n' | sed -E 's/([0-9]m),/\1 /g' | sed 's/ /\n/g' | sed 's/-999m/No_data/g' | sed $'1i\\\nName,Latitude,Longitude,Altitude\n' > metadataSCAR.txt

mv metadataSCAR.txt ../../../../Metadata_Stations/

echo 'Finish Data SCAR'

cd ../POLENET_AWS
mkdir POLENET

for archivo in *.dat
do
	TEXTO=${archivo%.dat}
	tail -n +8 $TEXTO\.dat | 
	sed -E 's/([0-9]{4}) ([0-9]{2}) ([0-9]{2})/\1-\2-\3/g' | 
	sed 's/ /,/g' | sed -E 's/(,[0-9][0-9]),([0-9][0-9],)/\1:\2/g' | 
	sed -E 's/(-[0-9][0-9]-[0-9][0-9]),([0-9][0-9]:[0-9][0-9],)/\1 \2/g' | 
	sed -E 's/([0-9],),*,([0-9])/\1\2/g' | 
	sed -E 's/([0-9],),*,(-[0-9])/\1\2/g' | 
	sed 's/,,*,/,/g' |  
	#sed 's/-999//g' | #sed 's/(-999)//g' |
	sed 's/,/\t/g' | awk '{printf "%s %s %.2f %.2f %.2f %i\n", $1,$2,$5,$4,$6*0.514444,$7}' | 
	sed 's/-999.00//g'| sed -E 's/-513.93//g'| sed 's/-999//g'| 
	sed -E $'1i\\\nDates,Temperature_(Celsius),Pressure_(hPa),Wind_Speed_(m/s),Wind_Direction\n' | 
	sed 's/ /,/g' | sed -E 's/(-[0-9][0-9]-[0-9][0-9]),([0-9][0-9]:[0-9][0-9],)/\1 \2/g' > $TEXTO\.csv
	mv $TEXTO\.csv ./POLENET
done

mv POLENET ../../../../Data_Stations

ls | grep -v 'list' > lista.list
cat lista.list | while read lines ; do head -n 3 $lines >> metadataPOLENET.temp.txt; done
cat metadataPOLENET.temp.txt | grep -v 'Operated*' | sed 's/latitude//g' | sed 's/longitude//g' | sed 's/height//g' | sed 's/ /,/g' | sed 's/,,/,/g' | sed -E 's/(.*[0-9]m).*/\1,/g' | tr -d '\n' | sed -E 's/([0-9]m),/\1 /g' | sed 's/ /\n/g' | sed 's/-999m/No_data/g' | sed $'1i\\\nName,Latitude,Longitude,Altitude\n' > metadataPOLENET.txt

mv metadataPOLENET.txt ../../../../Metadata_Stations/

echo 'Finish Data POLENET'

pwd 

#cd ../../../

mv ../../../../Data_Stations/ ../../../../../
mv ../../../../Metadata_Stations/ ../../../../../

echo 'Finished'