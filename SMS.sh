#!/bin/bash

detect_distro() {
    if [[ "$OSTYPE" == linux-android* ]]; then
            distro="termux"
    fi

    if [ -z "$distro" ]; then
        distro=$(ls /etc | awk 'match($0, "(.+?)[-_](?:release|version)", groups) {if(groups[1] != "os") {print groups[1]}}')
    fi

    if [ -z "$distro" ]; then
        if [ -f "/etc/os-release" ]; then
            distro="$(source /etc/os-release && echo $ID)"
        elif [ "$OSTYPE" == "darwin" ]; then
            distro="darwin"
        else 
            distro="Incorrecto"
        fi
    fi
}

pause() {
    read -n1 -r -p "Pulse cualquier tecla para continuar..." key
}
banner() {
    clear
    echo -e "\e[1;31m"
    if ! [ -x "$(command -v figlet)" ]; then
        echo 'Introduciendo Sms-Spam'
    else
        figlet SMS-SPAM
    fi
    if ! [ -x "$(command -v toilet)" ]; then
        echo -e "\e[4;34m Este SPAM fue creado por \e[1;32mAnonyProArg \e[0m"
    else
        echo -e "\e[1;34mCreated By \e[1;34m"
        toilet -f mono12 -F border AnonyProArg
    fi
    echo -e "\e[1;34m Compatible con termux!!!\e[0m"
    echo -e "\e[1;32m         Usar para molestar amigos \e[0m"
    echo -e "\e[4;32m   Repositoros/AnonyProArg \e[0m"
    echo " "
    echo "NOTE: Por favor, muévase a la versión PIP de SMS-SPAM para mayor estabilidad.."
    echo " "
}

init_environ(){
    declare -A backends; backends=(
        ["arch"]="pacman -S --noconfirm"
        ["debian"]="apt-get -y install"
        ["ubuntu"]="apt -y install"
        ["termux"]="apt -y install"
        ["fedora"]="yum -y install"
        ["redhat"]="yum -y install"
        ["SuSE"]="zypper -n install"
        ["sles"]="zypper -n install"
        ["darwin"]="brew install"
        ["alpine"]="apk add"
    )

    INSTALL="${backends[$distro]}"

    if [ "$distro" == "termux" ]; then
        PYTHON="python"
        SUDO=""
    else
        PYTHON="python3"
        SUDO="sudo"
    fi
    PIP="$PYTHON -m pip"
}

install_deps(){
    
    packages=(openssl git $PYTHON $PYTHON-pip figlet toilet)
    if [ -n "$INSTALL" ];then
        for package in ${packages[@]}; do
            $SUDO $INSTALL $package
        done
        $PIP install -r requirements.txt
    else
        echo "No pudimos instalar dependencias."
        echo "Asegúrese de tener git, python3, pip3 y los requisitos instalados."
        echo "Entonces puedes ejecutar SMS Spam."
        exit
    fi
}

banner
pause
detect_distro
init_environ
if [ -f .update ];then
    echo "Todos los requisitos encontrados...."
else
    echo 'Requisitos de instalación....'
    echo .
    echo .
    install_deps
    echo Este guión fue creado por AnonyProArg > .update
    echo 'Requisitos instalados....'
    pause
fi
while :
do
    banner
    echo -e "\e[4;31m Lea atentamente las instrucciones !!! \e[0m"
    echo " "
    echo "1) Iniciar SMS  Spam "
    echo "2) Iniciar Llamadas Spam "
    echo "3) Iniciar MAIL Spam (aún no disponible)"
    echo "4) para actualizar (funciona en Linux y emuladores de Linux) "
    echo "5) Salir "
    read ch
    clear
    if [ $ch -eq 1 ];then
        $PYTHON SMS-SPAM.py --sms
        exit
    elif [ $ch -eq 2 ];then
        $PYTHON SMS-SPAM.py --call
        exit
    elif [ $ch -eq 3 ];then
        $PYTHON SMS-SPAM.py --mail
        exit
    elif [ $ch -eq 4 ];then
        echo -e "\e[1;34m Descarga de archivos más recientes..."
        rm -f .update
        $PYTHON SMS-SPAM.py --update
        echo -e "\e[1;34m inciar SMS-SPAM otra vez"
        pause
        exit
    elif [ $ch -eq 5 ];then
        banner
        exit
    else
        echo -e "\e[4;32m opcion incorrecta !!! \e[0m"
        pause
    fi
done
