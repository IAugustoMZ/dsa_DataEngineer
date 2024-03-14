#!/bin/bash
# Extrai a data corrente do sistema
# use date --help para verificar as opções
horario_corrente=$(date +"%H%M%S")

# cria um backup da pasta usando a data corrente no nome do arquivo
tar -czf dados_$horario_corrente.tar.gz /root/dados/ml-latest-small

# move o arquivo para outra pasta
mv dados_$horario_corrente.tar.gz /tmp