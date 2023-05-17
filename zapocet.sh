#!/bin/bash

# Funkce pro vytvoření skupiny
create_group() {
  local group_name=$1
  if grep -q "^$group_name:" /etc/group; then
    echo "Skupina $group_name již existuje."
  else
    sudo groupadd $group_name
    echo "Skupina $group_name byla úspěšně vytvořena."
    grep "^$group_name:" /etc/group
  fi
}

# Získání názvu skupiny od uživatele
read -p "Zadejte název skupiny: " group_name
create_group $group_name

# Funkce pro vytvoření uživatele s atributy
create_user() {
  local username=$1
  local group=$2
  local rank=$3
  local name=$4
  local surname=$5
  local address=$6

  if id -u $username >/dev/null 2>&1; then
    echo "Uživatel $username již existuje."
  else
    sudo useradd -G users,sudo,$group -s /bin/bash -m -p "" -c "$rank, $name $surname, $address" $username
    echo "Uživatel $username byl úspěšně vytvořen."
    grep "^$username:" /etc/passwd
  fi
}

# Získání názvu souboru s uživateli od uživatele
read -p "Zadejte název souboru s uživateli: " filename

# Zkontrolovat a vytvořit uživatele ze seznamu
if [ -f $filename ]; then
  while IFS= read -r line; do
    surname=$(echo $line | cut -d',' -f1)
    firstname=$(echo $line | cut -d',' -f2)
    rank=$(echo $line | cut -d',' -f3)
    name=$(echo $line | cut -d',' -f4)
    address=$(echo $line | cut -d',' -f5)
    username=$(echo "${surname:0:1}${firstname}" | tr '[:upper:]' '[:lower:]')
    create_user $username $group_name "$rank" "$name" "$surname" "$address"
  done < $filename
else
  echo "Soubor $filename neexistuje."
fi