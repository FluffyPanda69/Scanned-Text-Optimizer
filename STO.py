from PIL import Image
from shutil import which
import io
import img2pdf
import os
import platform
import sys


# convert image to true monochrome, optimize size, return as byte array
def process_image(file, threshold):
    try:
        img = Image.open(file)
        r = img.convert('L').point(lambda x: 255 if x > threshold else 0, mode='1')

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
    # compression levels provided by GS (not much difference in monochrome, defaults to max)
    levels = ("/screen", "/ebook", "/printer", "/prepress", "/default")
    c_level = 4
    # light threshold for pixel to be considered black (very low values waste space and look noisy)
    thr = 127
    arg = ""
    file_list = []
    image_list = []
    num_args = len(sys.argv)

    if num_args == 1:
        error_exit("No file or directory given")

    if num_args > 4:
        error_exit("Too many arguments given")

    else:
        # Custom compression level
        if num_args == 3:
            try:
                c_level = int(sys.argv[2])
                if c_level not in range(5):
                    raise ValueError
            except ValueError:
                error_exit("Compression level must be a number between 0 and 4")
        # Custom monochrome pixel threshold
        if num_args == 4:
            try:
                thr = int(sys.argv[3])
                if thr not in range(256):
                    raise ValueError
            except ValueError:
                error_exit("BW threshold must be a number between 0 and 255")
        # Input file or directory
        arg = str(sys.argv[1])
        if arg == "./":
            arg = os.curdir
        if os.path.isfile(arg):
            if arg.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                file_list.append(arg)
            else:
                error_exit("Unsupported format provided")
        elif os.path.isdir(arg):
            for f in os.listdir(arg):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    file_list.append(f)
        else:
            error_exit("Argument is neither a valid file or a valid directory")
    if len(file_list) == 0:
        error_exit("Given directory contains no supported files")
    # First an unoptimized PDF is created by direct copy
    if len(file_list) > 1:
        for file in file_list:
            file = os.path.join(arg, file)
            r = process_image(file, thr)
            image_list.append(r)
        fn = os.path.basename(arg) + ".pdf"
        with open(fn, "wb") as f:
            f.write(img2pdf.convert(image_list))
    else:
        r = process_image(file_list[0], thr)
        fn = os.path.splitext(file_list[0])[0] + ".pdf"
        with open(fn, "wb") as f:
            f.write(img2pdf.convert(r))
    # Then, if present, GS is called to optimize the PDF
    os_name = platform.system().lower()
    if os_name == "windows":
        gs_name = "gswin64c "
        move_name = "move /y "
    else:
        gs_name = "gs "
        move_name = "mv -f "
    if which(gs_name[:-1]) is None:
        error_exit("Ghostscript not found. PDF file created but not optimized")
    gs_cmd = "-sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=" + levels[
        c_level] + " -dNOPAUSE -dQUIET -dBATCH -sOutputFile="
    gs_cmd = gs_name + gs_cmd
    gs_cmd = gs_cmd + "temp.pdf \"" + fn + "\""
    # print(gs_cmd)
    move_cmd = move_name + "temp.pdf " + fn
    os.system(gs_cmd)
    os.system(move_cmd)
    print("Ghostscript optimised the PDF. Job done")


if __name__ == "__main__":
    main()
