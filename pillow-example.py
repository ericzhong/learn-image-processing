#!/usr/bin/env python3

from PIL import Image

im = Image.open('dog.jpg')
w, h = im.size
print('Original: %sx%s' % (w, h))

im.thumbnail((w//2, h//2))
print('Resized: %sx%s' % (w//2, h//2))

im.save('tmp_dog.jpg', 'jpeg')
