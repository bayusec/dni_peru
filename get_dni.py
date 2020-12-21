#!/usr/bin/env python
# -*- coding: utf-8 -*
# title           :get_dni.py
# description     :python script for get dni number from name (Perú)
# author          :bayusec
# date            :21/12/2020
# version         :0.1
# usage           :python get_dni.py
# url             :https://github.com/bayusec/dni
# python_version  :3.7.5
# ==============================================================================

import shutil
import captcha
import requests
import sys
from bs4 import BeautifulSoup


class Getdni(object):
    def __init__(self, img_path=False):
        self.url = "http://ww4.essalud.gob.pe:7777/acredita/index.jsp"
        self.url_post = "http://ww4.essalud.gob.pe:7777/acredita/servlet/Ctrlwacre"
        self.url_captcha = "http://ww4.essalud.gob.pe:7777/acredita//captcha.jpg"
        self.num_captcha = ""
        self.nombre1 = ""
        self.nombre2 = ""
        self.app = ""
        self.apm = ""

        self.session = requests.session()
        if img_path is not False:
            self.img_path = img_path
        else:
            sys.exit("Path not found")
        self.header = {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/60.0",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       "Accept-Language": "en-US,en;q=0.5",
                       "Accept-Encoding": "gzip, deflate",
                       "Referer": "http://ww4.essalud.gob.pe:7777/acredita/index.jsp"}

    def getsession(self):
        # firt visit for get JSESSIONID
        firstr = self.session.get(self.url, headers=self.header)
        self.get_captcha()

    def get_captcha(self):
        # download captcha
        captchar = self.session.get(self.url_captcha, stream=True, headers=self.header)
        if captchar.status_code == 200:
            with open(self.img_path + "captcha.jpg", 'wb') as f:
                captchar.raw.decode_content = True
                shutil.copyfileobj(captchar.raw, f)

        code = captcha.scanCaptcha()
        config = "config='--psm 10 -c tessedit_char_whitelist=0123456789'"
        self.num_captcha = code.captchaUrl(self.img_path + "captcha.jpg", config)
        try:
            self.num_captcha = code.captchaUrl(self.img_path + "captcha.jpg", config)
        except Exception as e:
            print("Error al romper el captcha")
        print self.num_captcha

    def post_form(self):
        # post data
        data = {"pg": 1,
                "ap": self.app,
                "am": self.apm,
                "n1": self.nombre1,
                "n2": self.nombre2,
                "submit": "Consultar",
                "captchafield_nom": self.num_captcha}

        postr = self.session.post(self.url_post, data=data, headers=self.header)
        self.parse_data(postr)

    def parse_data(self, postr):
        doc_data = BeautifulSoup(postr.text, "lxml")
        nombre = doc_data.find("input", {"name": "nom"})["value"]
        dni = doc_data.find("input", {"name": "ndoc"})["value"]
        autogen = doc_data.find("input", {"name": "auto"})["value"]
        tabla_info= doc_data.findAll("table")[1].findAll("tr")
        tipo_asegurado = str(tabla_info[2].findAll("td")[1].text.strip())
        centro = str(tabla_info[5].findAll("td")[1].text.strip())

        salida = {"dni": dni, "nombre": nombre, "tipo_asegurado": tipo_asegurado, "centro_asistencial": centro, "autogenerado": autogen}
        print(salida)
        # print(tipo_seguro)


    def get_dni(self, app, apm, nombre1, nombre2=""):
        self.getsession()
        self.nombre1 = nombre1.upper()
        self.nombre2 = nombre2.upper()
        self.app = app.upper()
        self.apm = apm.upper()
        self.post_form()


c = Getdni("PATH")
c.get_dni("Apellido Paterno", "Apellido Materno", "Primer Nombre", "Segundo Nombre")
