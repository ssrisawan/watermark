import os
import sys

from PIL import Image

EXTS = ('.jpg', '.png')

if len(sys.argv) < 3:
    print('Usage: watermark.py \'image folder path\' \'logo path\' [topleft, topright, bottomleft, bottomright, center]')
    sys.exit()
elif len(sys.argv) == 4:
    path = sys.argv[1]
    lgo = sys.argv[2]
    pos = sys.argv[3]
else:
    path = sys.argv[1]
    lgo = sys.argv[2]

logo = Image.open(lgo)
logoWidth = logo.width
logoHeight = logo.height

# Set small gap around 10% of the logo size between the logo and the edge
gapWidth = int(logoWidth / 10)
gapHeight = int(logoHeight / 10)

for filename in os.listdir(path):
    if any([filename.lower().endswith(ext) for ext in EXTS]) and filename != lgo:
        image = Image.open(path + '/' + filename)
        imageWidth = image.width
        imageHeight = image.height

        try:
            if pos == 'topleft':
                image.paste(logo, (0, 0), logo)
            elif pos == 'topright':
                image.paste(logo, (imageWidth - logoWidth - gapWidth, gapHeight), logo)
            elif pos == 'bottomleft':
                image.paste(logo, (gapWidth, imageHeight - logoHeight - gapHeight), logo)
            elif pos == 'bottomright':
                image.paste(logo, (imageWidth - logoWidth - gapWidth, imageHeight - logoHeight - gapHeight), logo)
            elif pos == 'center':
                image.paste(logo, ((imageWidth - logoWidth)/2, (imageHeight - logoHeight)/2), logo)
            else:
                print('Error: ' + pos + ' is not a valid position')
                print('Usage: watermark.py \'image path\' \'logo path\' [topleft, topright, bottomleft, bottomright, center]')

            image.save(path + '/' + filename)
            print('Added watermark to ' + path + '/' + filename)

        except:
            image.paste(logo, ((imageWidth - logoWidth)/2, (imageHeight - logoHeight)/2), logo)
            image.save(path + '/' + filename)
            print('Added default watermark to ' + path + '/' + filename)
