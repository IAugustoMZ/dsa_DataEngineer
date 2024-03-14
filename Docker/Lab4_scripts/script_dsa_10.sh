#/bin/bash

# Fonte
path_src=/mnt/dsacademy/Lab4_scripts

# Destino
path_dst=/tmp/backup

echo
echo -e "\e[0;33mIniciando o backup dos Scripts do Lab4.\e[0m"



# loop pelos arquivos de origem
for file_src in $path_src/*; do
    cp -a -- "$file_src" "$path_dst/${file_src##*/}-$(date +"%d-%m-%y-%r")"

done

echo
echo -e "\e[0;33mBackup Concluído. Verificando a pasta /tmp/backup\e[0m"
cd $path_dst
ls -la
cd $path_src
echo