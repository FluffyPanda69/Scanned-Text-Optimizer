# Scanned-Text-Optimizer
Python script that converts images of text to an optimized, true monochrome PDF.
Can make use of Ghostscript ([if installed](https://www.ghostscript.com/download.html)) to compress the resulting files even further.

## Usage
> Input - **Required** - File or directory to convert ("./" for current directory)

> Compression level - Optional - Only used for Ghostscript compression, 0-4, defaults to 4 (max quality)

> Black threshold - Optional - Minimum light level required for a pixel to be black, otherwise it will be white, 0-255, defaults to 127

## Dependencies
Makes use of [Pillow](https://pypi.org/project/Pillow/), [IMG2PDF](https://pypi.org/project/img2pdf/) and [Ghostscript](https://www.ghostscript.com/) 
