from PIL import Image, ImageDraw, ImageOps

file = ''
ext = ''
width = 0
height = 0

def load(file_name):
    global file, ext, width, height
    (file, ext) = file_name.rsplit('.', 1)

    im = Image.open(file_name)
    width, height = im.size
    return im
        
def extract_gray(image):
  pixels = ImageOps.grayscale(image).load()
  width, height = im.size

  pix_list = []
  for x in range(width):
    for y in range(height):
      cpixel = pixels[x, y]
      pix_list.append(cpixel)

  return pix_list, width, height

SOBEL = 1
PREWITT = 2

def edge(pix_l, w, h, method = SOBEL):
  kernel_x = []
  kernel_y = []

  if method==SOBEL:
    #Sobel
    kernel_x = [-1,0,1,-2,0,2,-1,0,1]
    kernel_y = [1,2,1,0,0,0,-1,-2,-1]
  elif method==PREWITT:
    #Prewitt
    kernel_x = [-1,0,1,-1,0,1,-1,0,1]
    kernel_y = [1,1,1,0,0,0,-1,-1,-1]
        
  magnitude = []
  #magnitude_x = []
  #magnitude_y = []
    
  for x in range(w):
    for y in range(h):
      sides = get_grid(3,all_pixels, x,y, w, h)
      
      magx = sum(map(lambda a,b: a*b, sides, kernel_x))
      magy = sum(map(lambda a,b: a*b, sides, kernel_y))
      mag = pow(pow(magx,2) + pow(magy,2), 0.5)
      
      #magnitude_x.append(magx)
      #magnitude_y.append(magy)
      magnitude.append(mag)
      
  return map(int,magnitude)

def canny(pix_l, w, h):
	kernel_x = [-1,0,1,-2,0,2,-1,0,1]
	kernel_y = [1,2,1,0,0,0,-1,-2,-1]
	
	magnitude = []
	#magnitude_x = []
	#magnitude_y = []
	angle = []
    
	for x in range(w):
    for y in range(h):
      sides = get_grid(3, pix_l, x, y, w, h)

      magx = sum(map(lambda a,b: a*b, sides, kernel_x))
      magy = sum(map(lambda a,b: a*b, sides, kernel_y))

      mag = pow(pow(magx,2) + pow(magy,2), 0.5)
      
      #magnitude_x.append(magx)
      #magnitude_y.append(magy)
      
      magnitude.append(mag)

      def direction(x,y):
	      r = math.atan2(x,y)
	      if r < 0:
          r = 2*math.pi + r
	      r = r/(2*math.pi)
	      return r
      angle.append(direction(magx,magy))

  d = [0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0]
  mag2 = magnitude
  for x in range(w):
    for y in range(h):
      r = angle[x*h+y]
      diff = 2.0
      close = 2.0
      for n in d:
        diff_t = abs(n - r)
        if diff_t < diff:
          diff = diff_t
          close = n

      get = lambda x,y: int(x>=0 and x<w and y>=0 and y<h and magnitude[x*h+y])
      
      #N-S gradient
      if close == 0.0 or close == 0.5 or close == 1.0:
        sides = [get(x-1,y), get(x+1,y)]
      #E-W gradient
      elif close == 0.25 or close == 0.75:
        sides = [get(x,y-1), get(x,y+1)]
      #NW-SE gradient
      elif close == 0.125 or close == 0.625:
        sides = [get(x+1,y-1), get(x-1,y+1)]
      #NE-SW gradient
      elif close == 0.375 or close == 0.875:
        sides = [get(x-1,y-1), get(x+1,y+1)]

      if magnitude[x*h+y] < sides[0] or magnitude[x*h+y] < sides[1]:
        mag2[x*h+y] = 0
	magnitude = mag2

	return map(int, magnitude)
	#return map(int,magnitude_x), map(int,magnitude_y)

def emboss(pix_l, w, h):
  kernel_x = [-1,0,1,-2,0,2,-1,0,1]
  kernel_y = [1,2,1,0,0,0,-1,-2,-1]

  magnitude_x = []
  magnitude_y = []
  
  for x in range(w):
    for y in range(h):
      sides = get_grid(3, pix_l, x, y, w, h)

      magx = sum(map(lambda a,b: a*b, sides, kernel_x))
      magy = sum(map(lambda a,b: a*b, sides, kernel_y))

      mag = pow(pow(magx,2) + pow(magy,2), 0.5)
      
      magnitude_x.append(magx)
      magnitude_y.append(magy)

  return map(int,magnitude_x), map(int,magnitude_y)	

def gaussian(pix_l, w, h, s, p):
  k = int((s-1)/2)
  grid = []
  for i in range(1,s+1):
    for j in range(1,s+1):
      n = math.exp(-(pow(i-k-1,2)+pow(j-k-1,2))/(2.0*pow(p,2)))
      #n = math.exp(-(pow(i-k-1,2)+pow(j-k-1,2)))#/(2.0*pow(p,2)))
      d = 2.0*3.141592*pow(p,2)
      grid.append(n/d)

  s = sum(grid)
  filt = map(lambda a: a/s, grid)
  
  grayscale_out = []
  for x in range(w):
    for y in range(h):
      sides = get_grid(5,pix_l,x,y,w,h)
  
      mag = sum(map(lambda a,b: a*b, sides, filt))
  
      grayscale_out.append(int(mag))
  
  return grayscale_out

def threshold(pix_l, thresh):
  return map(lambda a: a >= thresh, pix_l)

def get_grid(size, pix_l, x, y, w, h):
  get = lambda x,y: int(x>=0 and x<w and y>=0 and y<h and pix_l[x*h+y])
  r = int((size - 1) / 2)
  grid = [get(xi,yi) for xi in range(x-r,x+r+1) for yi in range(y-r,y+r+1)]
  return grid

"""
[0,1,2,
 3,4,5,
 6,7,8,]

 ->

[6,3,0,
 7,4,1
 8,5,2]
"""
#rotates the token matrix clockwise by 90*deg
def token_rot(token, deg):
    for i in range(deg):
        token_n = []
        token_n.append(token[6])
        token_n.append(token[3])
        token_n.append(token[0])
        token_n.append(token[7])
        token_n.append(token[4])
        token_n.append(token[1])
        token_n.append(token[8])
        token_n.append(token[5])
        token_n.append(token[2])
        token = token_n
    return token

#compares the base to all rotations of the token
def token_comp(base, token):
    
  for i in range(4):
    base_r = token_rot(base,i)
    match = True
    for i in range(9):
      if token[i] >= 0 and token[i] != base_r[i]:
        match = False
        break
    if match == True:
      break
  return match

def thin(pix_l,w,h):
	change = 0
	notdone = True
	mask = map(lambda a: int(a > 0 and 1), pix_l)
	while notdone:
		change_t = 0
		notdone = False
		for x in range(w):
			for y in range(h):
				if mask[x*h+y] == 1
					sides = get_grid(3,mask,x,y,w,h)

					token1 = [0,0,0,-1,1,-1,1,1,1]
					token2 = [-1,0,0,1,1,0,-1,1,-1]

					match = token_comp(sides, token1)
					if not match:
						match = token_comp(sides, token2)
				else:
					match = 0
					
				

				change_t += match

				if match:
					mask[x*height+y] = 0
				
				if match > notdone: notdone = match
				change_t += match
		change += change_t
		#print change, '; ', change_t

	return map(lambda a: a > 0 and 255, mask)

def draw(rgb, im):
	drawing = ImageDraw.Draw(im)
	for x in range(width):
		for y in range(height):
			pos = x*height+y
			drawing.point((x,y),fill=rgb[pos])

def save(im):
	im.save(file + ".out." + ext)
	print 'done'
                

        
