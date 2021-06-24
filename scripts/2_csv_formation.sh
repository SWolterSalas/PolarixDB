#!/bin/bash
#INPUT1=$1 #"*.dat"

#echo 'quede 1'

cd ../
mkdir Data_Stations
mkdir Metadata_Stations

cd antarcticDB/ftp.bas.ac.uk/src/SCAR_EGOMA/SURFACE
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

mv metadataSCAR.txt ../../../../Metadata_Stations

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

mv metadataPOLENET.txt ../../../../Metadata_Stations

#rm -r /mnt/c/Users/Wolter/Desktop/Data/Estaciones_Totales/AWS
#mv /mnt/c/Users/Wolter/Desktop/Data/Procesamiento_Datos/AWS/csv /mnt/c/Users/Wolter/Desktop/Data/Estaciones_Totales/AWS

#echo 'quede 2'
#pwd

#cd ../POLANET
#mkdir csv

#for archivo in $INPUT1
#do
#	TEXTO=${archivo%.dat}
#	tail -n +8 $TEXTO\.dat | sed -E 's/([0-9]{4}) ([0-9]{2}) ([0-9]{2})/\1-\2-\3/g' | awk -e '$1_~"([0-9]{4}-[0-9]{2}-[0-9]{2})" && $4$5$6$7_~"([[:digit:]])" {print $1,$2,$3,$4,$5,$6,$7}' | sed -E 's/ /,/g' | sed -E 's/(-999)//g' | sed '1i Dates,Temperature,Pressure,Wind Speed,Wind Direction' | sed -E 's/,([0-9][0-9]),([0-9][0-9])/\1:\2/g' | sed -E 's/([0-9][0-9])([0-9][0-9]:[0-9][0-9])/\1 \2/g' > $TEXTO\.csv
#	mv $TEXTO\.csv ./csv
#done

#cd csv

#for filename in *.csv; 
#do 
#    [ -f "$filename" ] || continue
#    mv "$filename" "${filename//polenet_/}";

#done

#rm -r /mnt/c/Users/Wolter/Desktop/Data/Estaciones_Totales/POLENET
#mv /mnt/c/Users/Wolter/Desktop/Data/Procesamiento_Datos/POLANET/csv /mnt/c/Users/Wolter/Desktop/Data/Estaciones_Totales/POLENET

#echo 'quede 3'
#pwd

#cd ../SCAR
#mkdir csv

#for archivo in $INPUT1
#do
#	TEXTO=${archivo%.dat}
#	tail -n +8 $TEXTO\.dat | sed -E 's/([0-9]{4}) ([0-9]{2}) ([0-9]{2})/\1-\2-\3/g' | awk -e '$1_~"([0-9]{4}-[0-9]{2}-[0-9]{2})" && $4$5$6$7_~"([[:digit:]])" {print $1,$2,$3,$4,$5,$6,$7}' | sed -E 's/ /,/g' | sed -E 's/(-999)//g' | sed '1i Dates,Temperature,Pressure,Wind Speed,Wind Direction' | sed -E 's/,([0-9][0-9]),([0-9][0-9])/\1:\2/g' | sed -E 's/([0-9][0-9])([0-9][0-9]:[0-9][0-9])/\1 \2/g' > $TEXTO\.csv
#	mv $TEXTO\.csv ./csv
#done

#cd csv

#for filename in *.csv; 
#do 
#    [ -f "$filename" ] || continue
#    mv "$filename" "${filename//_surface/}";

#done
#
#rm -r /mnt/c/Users/Wolter/Desktop/Data/Estaciones_Totales/SCAR
#mv /mnt/c/Users/Wolter/Desktop/Data/Procesamiento_Datos/SCAR/csv /mnt/c/Users/Wolter/Desktop/Data/Estaciones_Totales/SCAR

