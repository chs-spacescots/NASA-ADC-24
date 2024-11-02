import ursina
import platform
import os

# hacky way to add the font folder to ursina
ursina.application._model_path.append_path(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts'))
# actually displaying custom fonts
_FONTPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
FONTLIST = [file for file in os.listdir(ursina.application.fonts_folder) if file.endswith(".ttf") or file.endswith(".otf")]
print("Custom Fontlist:\n\t"+"\n\t".join(FONTLIST))

FONTSIZE_REG = .6
FONTSIZE_SMALL = .9
FONTSIZE_BIG = 1.2
# ursina.Text.default_resolution = 2048 * ursina.Text.size
