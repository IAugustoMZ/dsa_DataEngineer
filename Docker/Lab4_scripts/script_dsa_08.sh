#/bin/bash
clear
echo ""
echo -e "\e[31;43m***** Nome do Hostname *****\e[0m"
hostname
echo ""
echo -e "\e[31;43m***** Plataforma (32 ou 64 bits) *****\e[0m"
uname -i
echo ""
echo -e "\e[31;43m***** Versão Linux *****\e[0m"
cat /etc/os-release | grep -e PRETTY_NAME -e VERSION=
echo ""
echo -e "\e[31;43m***** Espaço Usado em Disco *****\e[0m"
df -H | grep -ve '^tmpfs|cdrom'
echo ""
echo -e "\e[31;43m***** Uso de Memória RAM *****\e[0m"
free
echo ""
echo -e "\e[31;43m***** System Uptime e Load *****\e[0m"
uptime
echo ""
echo -e "\e[31;43m***** Top 5 Processos por Uso de Memória *****\e[0m"
ps -eo %mem,%cpu,comm --sort=-%mem | head -n 6
echo ""