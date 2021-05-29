#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import zipfile
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tAlgunas dependencias no se pudieron importar (posiblemente no se instalaron)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = """
███████████████████████████████████████████████████████████████████▀█
██▀▄─██▄─▀█▄─▄█─▄▄─█▄─▀█▄─▄█▄─█─▄█▄─▄▄─█▄─▄▄▀█─▄▄─██▀▄─██▄─▄▄▀█─▄▄▄▄█
██─▀─███─█▄▀─██─██─██─█▄▀─███▄─▄███─▄▄▄██─▄─▄█─██─██─▀─███─▄─▄█─██▄─█
▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▀▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀
                                         """
    if ASCII_MODE:
        logo = ""
    version = "Version: "+__VERSION__
    contributors = "Contributors: "+" ".join(__CONTRIBUTORS__)
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    mesgdcrt.SectionMessage(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Se detectó una mala conexión a Internet")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def do_zip_update():
    success = False
    if DEBUG_MODE:
        zip_url = "hloa"
        dir_name = "TBom"
    else:
        zip_url = "hhg"
        dir_name = "TBomb-mas"
    print(ALL_COLORS[0]+"Downloading ZIP ... "+RESET_ALL)
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_content = response.content
        try:
            with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
                for member in zip_file.namelist():
                    filename = os.path.split(member)
                    if not filename[1]:
                        continue
                    new_filename = os.path.join(
                        filename[0].replace(dir_name, "."),
                        filename[1])
                    source = zip_file.open(member)
                    target = open(new_filename, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
            success = True
        except Exception:
            mesgdcrt.FailureMessage("Ocurrió un error al extraer !!")
    if success:
        mesgdcrt.SuccessMessage("SMS-SPAM se actualizó a la última versión")
        mesgdcrt.GeneralMessage(
            "Ejecute el script nuevamente para cargar la última versión.")
    else:
        mesgdcrt.FailureMessage("No se puede actualizar SMS-Spam")
        mesgdcrt.WarningMessage(
            "Grab The Latest one From https://github.com/AnonyProArg/Spam_Sms_mundial.git")

    sys.exit()


def do_git_update():
    success = False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL, end='')
        process = subprocess.Popen("git checkout . && git pull ",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL, end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except Exception:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("SMS-Spam se actualizó a la última versión")
        mesgdcrt.GeneralMessage(
            "Ejecute el script nuevamente para cargar la última versión.")
    else:
        mesgdcrt.FailureMessage("No se puede actualizar.")
        mesgdcrt.WarningMessage("egúrese de instalar 'git' ")
        mesgdcrt.GeneralMessage("Entonces ejecuta el comando:")
        print(
            "git checkout . && "
            "git pull https://github.com/AnonyProArg/Spam_Sms_mundial.git HEAD")
    sys.exit()


def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()


def check_for_updates():
    if DEBUG_MODE:
        mesgdcrt.WarningMessage(
            "MODO DEPURACIÓN habilitado! La verificación de actualización automática está deshabilitada.")
        return
    mesgdcrt.SectionMessage("Comprobando actualizaciones")
    fver = requests.get(
        "https://raw.githubusercontent.com/AnonyProArg/Spam_Sms_mundial/main/.version"
    ).text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("Hay una actualización disponible")
        mesgdcrt.GeneralMessage("Iniciando actualización ")
        update()
    else:
        mesgdcrt.SuccessMessage("SMS-Spam está actualizado")
        mesgdcrt.GeneralMessage("Iniciando SMS-Spam")


def notifyen():
    try:
        if DEBUG_MODE:
            url = "https://raw.githubusercontent.com/AnonyProArg/Spam_Sms_mundial/main/.notify"
        else:
            url = "https://raw.githubusercontent.com/AnonyProArg/Spam_Sms_mundial/main/.notify"
        noti = requests.get(url).text.upper()
        if len(noti) > 10:
            mesgdcrt.SectionMessage("NOTIFICATION: " + noti)
            print()
    except Exception:
        pass


def get_phone_info():
    while True:
        target = ""
        cc = input(mesgdcrt.CommandMessage(
            "Ingrese su código de país (Sin +): "))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "El código de país ({cc}) que ingresó"
                " no es válido o no es compatible".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            "Ingrese el número de destino: +" + cc + " "))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "El número de teléfono ({target})".format(target=target) +
                "que ha introducido no es válido")
            continue
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("Enter target mail: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "El correo ({target})".format(target=target) +
                " que ha introducido no es válido")
            continue
        return target


def pretty_print(cc, target, success, failed):
    requested = success+failed
    mesgdcrt.SectionMessage("El SPAM está en curso. Tenga paciencia.")
    mesgdcrt.GeneralMessage(
        "Manténgase conectado a Internet durante el SPAM")
    mesgdcrt.GeneralMessage("Objetivo       : " + cc + " " + target)
    mesgdcrt.GeneralMessage("Enviando        : " + str(requested))
    mesgdcrt.GeneralMessage("Exitoso   : " + str(success))
    mesgdcrt.GeneralMessage("Fallido      : " + str(failed))
    mesgdcrt.WarningMessage(
        "Esta herramienta se creó solo con fines divertidos y de investigación.")
    mesgdcrt.SuccessMessage("SMS-Spam fue creado by AnonyProArg")


def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    mesgdcrt.SectionMessage("Preparando el Spam: tenga pacienciat")
    mesgdcrt.GeneralMessage(
        "Manténgase conectado a Internet durante el Spam.")
    mesgdcrt.GeneralMessage("Versión API   : " + api.api_version)
    mesgdcrt.GeneralMessage("Objetivo        : " + cc + target)
    mesgdcrt.GeneralMessage("Cantidad        : " + str(count))
    mesgdcrt.GeneralMessage("Procesos      : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("Retraso         : " + str(delay) +
                            " Segundos")
    mesgdcrt.WarningMessage(
        "Esta herramienta se creó solo con fines divertidos y de investigación.")
    print()
    input(mesgdcrt.CommandMessage(
        "Presione [CTRL + Z] para suspender el Spam o [ENTER] para reanudarlo"))

    if len(APIProvider.api_providers) == 0:
        mesgdcrt.FailureMessage("Su país / objetivo aún no es compatible")
        mesgdcrt.GeneralMessage("Siéntase libre de llegar a nosotros")
        input(mesgdcrt.CommandMessage("Presione [ENTER] para salir"))
        bann_text()
        sys.exit()

    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    mesgdcrt.FailureMessage(
                        "Se alcanzó el límite de Spam para tu objetivo.")
                    mesgdcrt.GeneralMessage("Inténtelo de nuevo más tarde!!")
                    input(mesgdcrt.CommandMessage("Presione [ENTER] para salir"))
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                pretty_print(cc, target, success, failed)
    print("\n")
    mesgdcrt.SuccessMessage("SPAM Completo!")
    time.sleep(1.5)
    bann_text()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        notifyen()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                message = ("Ingrese el número de {type}".format(type=mode.upper()) +
                           " enviar (Max {limit}): ".format(limit=limit))
                count = int(input(mesgdcrt.CommandMessage(message)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("Tú lo pediste " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "Limitando automáticamente el valor"
                        " a {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage("Ingrese el tiempo de retraso (en segundos): "))
                    .strip())
                # delay = 0
                max_thread_limit = (count//10) if (count//10) > 0 else 1
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        "Ingrese el número de procesos (recomendado: {max_limit}): "
                        .format(max_limit=max_thread_limit)))
                    .strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("Lea las instrucciones atentamente !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Llamada INTR recibida - Saliendo ....")
        sys.exit()


mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("funcionará solo en Python v3")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    update()


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['SpeedX', 't0xic0der', 'scpketer', 'Stefan']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

ASCII_MODE = False
DEBUG_MODE = False

description = """SMS-Spam: aplicación amigable para spam

SMS-Spam: se puede utilizar para muchos propósitos que incluyen:
\t Exponer las API vulnerables a través de Internet
\t Spam amistoso
\t Probar su detector de spam y más ...
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Coded by SpeedX !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="start TBomb with SMS Bomb mode")
parser.add_argument("-call", "--call", action="store_true",
                    help="start TBomb with CALL Bomb mode")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="start TBomb with MAIL Bomb mode")
parser.add_argument("-ascii", "--ascii", action="store_true",
                    help="show only characters of standard ASCII set")
parser.add_argument("-u", "--update", action="store_true",
                    help="update TBomb")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="show current TBomb contributors")
parser.add_argument("-v", "--version", action="store_true",
                    help="show current TBomb version")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.ascii:
        ASCII_MODE = True
        mesgdcrt = MessageDecorator("stat")
    if args.version:
        print("Version: ", __VERSION__)
    elif args.contributors:
        print("Contributors: ", " ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {
            "1": "SMS",
            "2": "CALL",
            "3": "MAIL"
        }
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print("Available Options:\n")
                for key, value in avail_choice.items():
                    print("[ {key} ] {value} SPAM:".format(key=key,
                                                          value=value))
                print()
                choice = input(mesgdcrt.CommandMessage("Ingrese Elección : "))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("Llamada INTR recibida - Saliendo")
            sys.exit()
    sys.exit()
