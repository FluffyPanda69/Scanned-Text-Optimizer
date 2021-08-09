# Scanned-Text-Optimizer
Platform-independent Python script that converts images of text to an optimized, true monochrome PDF.
New version has a file/directory picker and automatically chooses the black/white threshold.
Source files will be modified, but only lossless compression is applied.
Only JPEG and PNG files are supported. Scans yield the best results.

## Dependencies
Needs [Pillow](https://pypi.org/project/Pillow/), [IMG2PDF](https://pypi.org/project/img2pdf/) and [EasyGUI](https://pypi.org/project/easygui/).
Can make use of [ExifTool](https://exiftool.org/), [Pngcrush](https://pmt.sourceforge.io/pngcrush/), [Jpegoptim](https://github.com/tjko/jpegoptim) and [Ghostscript](https://www.ghostscript.com/) if they are installed.