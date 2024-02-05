import qrcode
from PIL import Image
 
# taking image which user wants
# in the QR code center
Logo_link = ''

# taking url or text
url = ''

# color
color = 'Black'


logo = Image.open(Logo_link)
#if png and background is transparent, replace with white
if Logo_link.endswith('.png') and logo.mode in ('RGBA', 'LA'):
    name = Logo_link.split('.')[0]
    new_logo = Image.new("RGBA", logo.size, "WHITE") # Create a white rgba background
    new_logo.paste(logo, (0, 0), logo)              # Paste the image on the background. Go to the links given below for details.
    new_logo.convert('RGB').save(name+'.jpg', "JPEG")  # Save as JPEG
    logo = Image.open(name+'.jpg')

# taking base width
basewidth = 100
 
# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
 

 
# adding URL or text to QRcode
QRcode.add_data(url)
 
# generating QR code
QRcode.make()
 
# taking color name from user
QRcolor = color
 
# adding color to QR code
QRimg = QRcode.make_image(
    fill_color=QRcolor, back_color="white").convert('RGB')
 
# set size of QR code
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)
 
# save the QR code generated
QRimg.save('QR_out.png')
 
print('QR code generated!')
