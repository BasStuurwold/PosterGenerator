from PIL import Image, ImageDraw, ImageFont
import requests
import shutil

class newImage:

    def __init__(self):
        # Set file size in pixel and fonts
        self.W, self.H = (1191,1684)
        self.fontsizeTitle = 125
        self.fontsizeBody = 75
        self.fontTitle = ImageFont.truetype('fonts/MYRIADPRO-BOLD.otf', size=self.fontsizeTitle)
        self.fontBody = ImageFont.truetype('fonts/MYRIADPRO-BOLD.otf', size=self.fontsizeBody)
        self.fontBodyRegular = ImageFont.truetype('fonts/MYRIADPRO-REGULAR.otf', size=100)

        # Set inputs
        self.title = input('Hoe heet het evenement? ')
        self.date = input('Wanneer is het? ')
        self.time = input('Van en tot wanneer is het? ')
        self.adress = input('Wat is het adres? (Straat + huisnummer) ')
        self.price = input('Hoeveel kost het? (Voor leden en niet-leden) ')
        self.image_url_bg = input('Achtergrondfoto (URL naar foto) ').strip()
        self.image_url_icon = input('Icon (URL naar foto) ').strip()

        # Create new file
        self.image = Image.new('RGBA', (self.W, self.H), color = 'black')
        
    def fetchImage(self):
        # Fetch image from URL
        resp = requests.get(self.image_url_bg, stream=True)
        local_file = open('achtergrond.jpg', 'wb')
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, local_file)
        del resp

    def fetchIcon(self):
        # Fetch icon from URL
        resp = requests.get(self.image_url_icon, stream=True)
        local_file = open('icon.png', 'wb')
        resp.raw.decode_contect = True
        shutil.copyfileobj(resp.raw, local_file)
        del resp
        
    def pasteBackground(self):
        # Paste background image
        self.fetchImage()
        self.image2 = Image.open('achtergrond.jpg').convert('RGBA')
        w, h = self.image2.size
        self.image2 = self.image2.resize((round((self.W*2)), self.H))
        self.image.paste(self.image2)

        # Paste black filter
        self.image5 = Image.open('zwart.png').convert('RGBA')
        w, h = self.image5.size
        self.image.paste(self.image5, (0, 0), self.image5)

        # Paste icon
        self.fetchIcon()
        self.image4 = Image.open('icon.png').convert('RGBA')
        self.image4 = self.image4.resize((300, 300))
        w, h = self.image4.size
        self.image.paste(self.image4, ((round((self.W-w)/2),round((self.H-h)/2-200))), self.image4)

        # Paste white mask over icon
        self.image6 = Image.new('RGBA', (300,300), color='white')
        w, h = self.image6.size
        self.image.paste(self.image6, ((round((self.W-w)/2),round((self.H-h)/2-200))), self.image4)
        
    def pasteDecorations(self):
        # Paste logo, socials and gradient.
        self.image3 = Image.open('logo-social-gradient.png').convert('RGBA')
        self.image3 = self.image3.resize((self.W, self.H))
        self.image.paste(self.image3, (0, 0), self.image3)

    def inputText(self):
        # Putting in the text
        draw = ImageDraw.Draw(self.image)
        w1, h1 = draw.textsize(self.title, font=self.fontTitle)
        w, h = draw.textsize(self.date, font=self.fontBody)
        w, h = draw.textsize(self.time, font=self.fontBody)
        w, h = draw.textsize(self.adress, font=self.fontBody)
        w, h = draw.textsize(self.price, font=self.fontBody)
        value = 0

        # Set dictionary for inputs
        words = dict()
        words[100] = self.date
        words[200] = self.time
        words[300] = self.adress
        words[400] = self.price

        draw.text(((self.W-w1)/2,(self.H-h1)/2-500), self.title, fill="white", font=self.fontTitle)

        # Iterate through dictionary
        for key in words.keys():
            value = value + 100
            print(words[value])
            # draw.text(((self.W-w)/2-450,(self.H-h)/2+value+180), words[value], fill="white", font=self.fontBody)
            draw.text((75,(self.H-h)/2+value+200), words[value], fill="white", font=self.fontBody)

    def saveImage(self):
        self.newImage = self.image.convert('RGB')
        self.newImage.save(self.title + '.pdf')
        self.newImage.save(self.title + '.png')
        
image = newImage()
image.pasteBackground()
image.pasteDecorations()
image.inputText()
image.saveImage()

