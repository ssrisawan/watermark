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

        # Get the image orientation from EXIF (Tag 274)
        # 1: 0 degrees
        # 6: rotate 90 degrees
        # 3: rotate 180 degrees
        # 8: rotate 270 degrees
        orientation = image.getexif().get(274)

        # Transpose the image if width is greater than height while the orientation is either 6 or 8
        if (imageWidth > imageHeight):
            if (orientation == 6):
                image = image.transpose(Image.ROTATE_270)
                imageWidth, imageHeight = imageHeight, imageWidth
            if (orientation == 8):
                image = image.transpose(Image.ROTATE_90)
                imageWidth, imageHeight = imageHeight, imageWidth

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
