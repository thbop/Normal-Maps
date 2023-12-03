from PIL import Image
from pygame.math import Vector3

# Load height map
base_image = Image.open('heightmap.png')
pix = base_image.load()

normal_image = Image.new('RGB', base_image.size)
npix = normal_image.load()


def rgb_to_v(color):
    return color[0] * 0.2126 + color[1] * 0.7152 + color[2] * 0.0722

def v_to_color(v):
    return max(min(round(v * 255), 255), 0)

def nvec_to_color(vec):
    return (
        v_to_color(vec.x),
        v_to_color(vec.y),
        v_to_color(vec.z)
    )

def four_h_to_vec(v1, v2, v3, v4):
    return Vector3(
            -(v4 - v2) * ((y - 1) - (y + 1)),
            -((x - 1) - (x + 1)) * (v1 - v3),
            ((x - 1) - (x + 1)) - ((y - 1) - (y + 1))
        )

for x in range(base_image.size[0]):
    for y in range(base_image.size[1]):
        border_pixel = x == 0 or x == base_image.size[0] - 1 or y == 0 or y == base_image.size[1] - 1
        if not border_pixel:
            v1 = rgb_to_v(pix[x, y - 1])
            v2 = rgb_to_v(pix[x + 1, y])
            v3 = rgb_to_v(pix[x, y + 1])
            v4 = rgb_to_v(pix[x - 1, y])
            c1 = rgb_to_v(pix[x - 1, y - 1])
            c2 = rgb_to_v(pix[x + 1, y - 1])
            c3 = rgb_to_v(pix[x + 1, y + 1])
            c4 = rgb_to_v(pix[x - 1, y + 1])
            
            normal = four_h_to_vec(v1, v2, v3, v4) + four_h_to_vec(c1, c2, c3, c4)
            if normal.length() != 0:
                normal = normal.normalize()
            else:
                normal = Vector3(0, 1, 0)

            # Lambertian
            # value = v_to_color( normal.dot(Vector3(.5, -1, 0)) ) 
            # npix[x, y] = (value, value, value)
            
            # Just normal
            npix[x, y] = nvec_to_color(normal)


normal_image.save('normalmap.png')