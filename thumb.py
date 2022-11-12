from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip

width = 1920
height = 1080

title = input('Title:')

message = "(SLOWED+REVERB)"


clip = VideoFileClip("Result[Slowed+Reverb].mp4")
clip.save_frame(r"image.jpg", t=1.00)

img = Image.open(r"image.jpg")

font = ImageFont.truetype("font/brush.ttf", size=190)
font2 = ImageFont.truetype("font/ayar.ttf", size=60)

imgDraw = ImageDraw.Draw(img)

textWidth, textHeight = imgDraw.textsize(title, font=font)
xText1 = (width - textWidth) / 2
textWidth, textHeight = imgDraw.textsize(message, font=font2)
xText2 = (width - textWidth) / 2


imgDraw.text((xText1, 350), title, font=font, fill=(255, 255, 255))
imgDraw.text((xText2, 700), message, font=font2, fill=(255, 255, 255))

img.save('Thumb.jpg')