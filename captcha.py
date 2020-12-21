import os
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


class scanCaptcha(object):
    """Clase que toma una imagen de un captcha como entrada y retorna un string del texto del captcha

    Attributes:
        img_path: Direccion de la imagen en el sistema de archivos.
        img_str: Representacion de la imagen en string.
    """

    def __init__(self):
        self.pytes = pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    def captchaUrl(self, path, config=False):
        try:
            os.path.isfile(path)
        except:
            print "File not exist"
            return False
        if config is not False:
            try:
                return pytesseract.image_to_string(Image.open(path), lang="eng", config=config)
            except Exception as e:
                print e
                return False

        try:
            return pytesseract.image_to_string(Image.open(path))
        except:
            return False

    def captchaStr(self, string):
        return False