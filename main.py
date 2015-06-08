import TYImage

file = 'test1.jpg'

image = TYImage.load(file)

pix_l, w, h = TYImage.extract_gray(image)

pix_l = TYImage.gaussian(pix_l, w, h, 5, 1)
red, blue = TYImage.emboss(pix_l, w, h)

rgb = []
for i in range(w):
  for j in range(h):
    pos = i*h+j
    rgb.append((red[pos]+125,125+(red[pos]+blue[pos])/2, blue[pos]+125))
		
TYImage.draw(rgb,image)

TYImage.save(image)
		
