from PIL import Image
from PIL import ImageStat
from sys import exit
import easygui
import io
import img2pdf
import os
import platform
import shutil
import subprocess
import sys


# convert image to true monochrome, optimize size, return as byte array
def process_image(file):
    try:
        if shutil.which("exiftool") is not None:
            exiftool = "exiftool -All= -overwrite_original " + file
            exiftool = exiftool.split(" ", 3)
            subprocess.run(exiftool, stdout=subprocess.DEVNULL)
        if file.lower().endswith(".png") and shutil.which("pngcrush") is not None:
            pngcrush = "pngcrush -ow -rem allb -reduce " + file
            pngcrush = pngcrush.split(" ", 5)
            subprocess.run(pngcrush, stdout=subprocess.DEVNULL)
            print("Optimized input file : " + file)
        if file.lower().endswith((".jpg", ".jpeg")) and shutil.which("jpegoptim") is not None:
            jpegoptim = "jpegoptim " + file
            jpegoptim = jpegoptim.split(" ", 1)
            subprocess.run(jpegoptim, stdout=subprocess.DEVNULL)
            print("Optimized input file : " + file)
        img = Image.open(file)
        r = img.convert('L')
        threshold = int(ImageStat.Stat(r).mean[0])
        threshold = max(threshold, 127)
        threshold = min(threshold, 223)
        r = r.point(lambda x: 255 if x > threshold else 0, mode='1')
        imgByteArr = io.BytesIO()
        r.save(imgByteArr, mode='1', format='PNG', optimize=True)
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr
    except Exception as e:
        print("Could not process " + file)
        print(e)
        exit(1)


def error_exit(message):
    print(message)
    exit(1)


def main():
    img_formats = (".png", ".jpg", ".jpeg")
    arg = ""
    file_list = []
    image_list = []
    num_args = len(sys.argv)

    # GUI
    if num_args == 1:
        choice = easygui.ccbox("What are you converting?", "STO", ["Single file", "Directory"])
        if choice:
            arg = str(easygui.fileopenbox(default="./", filetypes=img_formats))
        else:
            arg = str(easygui.diropenbox(default="./"))

    if num_args > 2:
        error_exit("Too many arguments given")

    else:
        # Input file or directory
        if arg is None:
            arg = str(sys.argv[1])
        if arg == "./":
            arg = os.curdir
        if os.path.isfile(arg):
            if arg.lower().endswith(img_formats):
                file_list.append(arg)
            else:
                error_exit("Unsupported format provided")
        elif os.path.isdir(arg):
            for f in os.listdir(arg):
                if f.lower().endswith(img_formats):
                    file_list.append(f)
        else:
            error_exit("Argument is neither a valid file or a valid directory")
    if len(file_list) == 0:
        error_exit("Given directory contains no supported files")
    # First an unoptimized PDF is created by direct copy
    if len(file_list) > 1:
        for file in file_list:
            file = os.path.join(arg, file)
            r = process_image(file)
            image_list.append(r)
        if arg == os.path.curdir:
            here = os.getcwd()
            fn = os.path.join(here, os.path.basename(here)) + ".pdf"
        else:
            fn = os.path.basename(arg) + ".pdf"
        with open(fn, "wb") as f:
            f.write(img2pdf.convert(image_list))
    else:
        r = process_image(file_list[0])
        fn = os.path.splitext(file_list[0])[0] + ".pdf"
        with open(fn, "wb") as f:
            f.write(img2pdf.convert(r))
    # Then, if present, GS is called to optimize the PDF
    os_name = platform.system().lower()
    if os_name == "windows":
        gs_name = "gswin64c "
    else:
        gs_name = "gs "
    if shutil.which(gs_name[:-1]) is None:
        error_exit("Ghostscript not found. PDF file created but not optimized")
    gs_cmd = "-sDEVICE=pdfwrite -dNOPAUSE -dQUIET -dBATCH -sOutputFile="
    gs_cmd = gs_name + gs_cmd
    gs_cmd = gs_cmd + "temp.pdf \"" + fn + "\""
    gs_cmd = gs_cmd.split(" ", 6)
    subprocess.run(gs_cmd)
    shutil.move("temp.pdf", fn)
    print("Ghostscript optimized the PDF. Job done")


if __name__ == "__main__":
    main()
