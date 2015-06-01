from PIL import Image, ImageDraw, ImageOps

def tup_add(a,b): return tuple(map(lambda x, y: x + y, a,b))
def tup_sub(a,b): return tuple(map(lambda x, y: x - y, a,b))
def tup_hash(a): return 

file = "test1"
ext = "jpg"
im = Image.open(file + "." + ext)
im.thumbnail((500,500))

pixels = ImageOps.grayscale(im).load()
width, height = im.size

all_pixels = []
for x in range(width):
    for y in range(height):
        cpixel = pixels[x, y]
        all_pixels.append(cpixel)
        
def mag(k):
    return (abs((k[0]+2*k[1]+k[2]) - (k[6]+2*k[7]+k[8])) +
            abs((k[2]+2*k[5]+k[8]) - (k[0]+2*k[3]+k[6])))

mask = []
image = []

for x in range(width):
    for y in range(height):
        pos = x*height+y
        pixel = all_pixels[pos]
        sides = []
        
        #pulling 3x3 grid around point

        #[-1,-1]
        if x > 0 and y > 0:
            sides.append(all_pixels[ (x-1)*height+(y-1)] )
        else:
            sides.append(0)

        #[-1,0]   
        if x > 0:
            sides.append(all_pixels[ (x-1)*height+y] )
        else:
            sides.append(0)

        #[-1,+1]  
        if x > 0 and y < height - 1:
            sides.append(all_pixels[ (x-1)*height+(y+1)] )
        else:
            sides.append(0)

        #[0,-1]
        if y > 0:
            sides.append(all_pixels[ x*height+(y-1)] )
        else:
            sides.append(0)

        #[0,0]
        sides.append(all_pixels[pos])

        #[0,+1]
        if y < height - 1:
            sides.append(all_pixels[ x*height+(y+1)] )
        else:
            sides.append(0)

        #[+1,-1]
        if x < width - 1 and y > 0:
            sides.append(all_pixels[ (x+1)*height+(y-1)] )
        else:
            sides.append(0)

        #[+1,0]                       
        if x < width - 1:
            sides.append(all_pixels[ (x+1)*height+y] )
        else:
            sides.append(0)
        
        #[+1,+1]
        if x < width - 1 and y < height - 1:
            sides.append(all_pixels[ (x+1)*height+(y+1)] )
        else:
            sides.append(0)

        magnitude = mag(sides)
        image.append(magnitude)
        mask.append(magnitude > 120)

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

mask1 = mask
mask2 = mask


change = 0

notdone = True

mask2_t = mask2

while notdone:
    change_t = 0
    notdone = False
    #mask2_t = mask2
    #mask2 = []
    for x in range(width):
        for y in range(height):
            pos = x*height+y
            pixel = mask2_t[pos]
            sides = []

            if pixel == 1:

                #pulling 3x3 grid around point

                #[-1,-1]
                if x > 0 and y > 0:
                    sides.append(mask2_t[ (x-1)*height+(y-1)] )
                else:
                    sides.append(0)

                #[-1,0]   
                if x > 0:
                    sides.append(mask2_t[ (x-1)*height+y] )
                else:
                    sides.append(0)

                #[-1,+1]  
                if x > 0 and y < height - 1:
                    sides.append(mask2_t[ (x-1)*height+(y+1)] )
                else:
                    sides.append(0)

                #[0,-1]
                if y > 0:
                    sides.append(mask2_t[ x*height+(y-1)] )
                else:
                    sides.append(0)

                #[0,0]
                sides.append(1)

                #[0,+1]
                if y < height - 1:
                    sides.append(mask2_t[ x*height+(y+1)] )
                else:
                    sides.append(0)

                #[+1,-1]
                if x < width - 1 and y > 0:
                    sides.append(mask2_t[ (x+1)*height+(y-1)] )
                else:
                    sides.append(0)

                #[+1,0]                       
                if x < width - 1:
                    sides.append(mask2_t[ (x+1)*height+y] )
                else:
                    sides.append(0)
                
                #[+1,+1]
                if x < width - 1 and y < height - 1:
                    sides.append(mask2_t[ (x+1)*height+(y+1)] )
                else:
                    sides.append(0)

                token1 = [0,0,0,-1,1,-1,1,1,1]
                token2 = [-1,0,0,1,1,0,-1,1,-1]

                match = token_comp(sides, token1)
                if not match:
                    match = token_comp(sides, token2)
            else:
                match = 0
                
            

            change_t += match

            if match:
                mask2_t[pos] = 0
            else:
                mask2_t[pos] = pixel
            
            if match > notdone: notdone = match

    change += change_t
    print change, '; ', change_t

    
            
print change

draw = ImageDraw.Draw(im)

draw.rectangle([0,0,width,height], fill=0)

for x in range(width):
    for y in range(height):
        pos = x*height+y
        
        #draw.point((x,y),fill=(image[pos],image[pos],image[pos]))
        
        #if mask[pos] == 1:
        #    draw.point((x,y), fill=(255,255,255))
        
        if mask2_t[pos] == 1:
            draw.point((x,y), fill=(255,255,255))

im.save(file + ".out." + ext)
print 'done'
                

        
