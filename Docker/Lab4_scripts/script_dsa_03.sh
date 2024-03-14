#!/bin/bash
# Input do Usuário
clear
echo "Digite seu primeiro nome: "
read FIRSTNAME
echo "Digite seu sobrenome: "
read LASTNAME
echo ""
echo "Seu nome completo: $FIRSTNAME $LASTNAME"
echo ""
echo "Digite sua idade: "
read USERAGE
echo "Em 10 anos você estará com `expr $USERAGE + 10` anos."