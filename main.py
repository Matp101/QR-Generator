import qrcode
from PIL import Image, ImageColor


# image which user wants in the QR code center
Logo_link = 'Picture.png'   # Path to the logo image
Logo_size = 100
Logo_background_color = 'transparent'  # Optional background color for the logo (Can be a name such as 'Black' or hex such as '#000000')

# url or text
url = 'https://www.example.com'

# color (can be a name or hex)
fill_color = ''  # Fill color of the QR code (Can be a name such as 'Black' or hex such as '#000000')
background_color = 'transparent'  # Background color of the QR code, 'transparent' for transparent background (Can be a name such as 'Black' or hex such as '#000000')

# Function to validate and convert color name or hex to RGBA tuple
def get_color_rgba(color):
    if color.lower() == 'transparent':
        return (255, 255, 255, 0)  # Fully transparent
    elif color.startswith('#'):
        # Convert hex to RGBA
        h = color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)  # Opaque color
    else:
        # Convert color name to RGBA
        return ImageColor.getrgb(color) + (255,)  # Opaque color

# Load and prepare the logo
logo = Image.open(Logo_link)
if logo.mode != 'RGBA':
    logo = logo.convert('RGBA')
logo = logo.resize((Logo_size, Logo_size), Image.Resampling.LANCZOS)

# Create QR code
QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
QRcode.add_data(url)
QRcode.make()

# Generate QR code image with a temporary solid background for conversion
temp_back_color = 'white' if background_color == 'transparent' else background_color
QRimg = QRcode.make_image(fill_color=fill_color, back_color=temp_back_color).convert('RGBA')

# If background should be transparent, manually adjust it
if background_color == 'transparent':
    datas = QRimg.getdata()
    newData = []
    for item in datas:
        # Change all white (also temporary background) to transparent
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    QRimg.putdata(newData)

# Paste the logo onto the QR code with transparency
pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos, mask=logo)

# Save the QR code with a transparent background
output_file = 'QR_code.png'
QRimg.save(output_file, format='PNG')

print('QR code generated!')