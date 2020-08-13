from __future__ import print_function
from PIL import Image, ImageDraw
import os
import io
import json



def generate(text):
	try:
		path = os.path.dirname(os.path.abspath(__file__))

		text = text.upper()
		text = text[:40]


		if (text == ""):
			test = " "

		words = []
		letters = []

		letters.append(path + '/src/START (s).jpg')
		i = 0
		for letter in text:
			# letter = letter.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
			if (letter == " "):
				letter = "SPACE"
			if (letter == "."):
				letter = "DOT"
			if (letter == '"'):
				letter = "QUTATION"
			if (letter == "?"):
				letter = "QUESTION"
			if (letter == '\n'):
				letters.append(path + '/src/LINE R (s).jpg')
				words.append(letters)
				letters = []
				letters.append(path + '/src/LINE L (s).jpg')
			else:
				letter_dir = path + '/src/' + letter + ' (s).jpg'
				if (os.path.exists(letter_dir)):
					letters.append(letter_dir)
					i = i + 1
				else:
					text = text[:i] + text[(i+1):]
		letters.append(path + '/src/END (s).jpg')
		words.append(letters)	

		height = 0
		currant_width = 0
		width = 0
		image = []
		images = []
		widths = []
		for word in words:
			image += map(Image.open, word)
			widths_sum, heights = zip(*(i.size for i in image))
			currant_width = sum(widths_sum)
			height += max(heights)
			widths.append(currant_width)
			if (currant_width > width):
				width = currant_width
			images.append(image)
			image = []
		# height -= 84

		width += 100
		height += 100	

		new_im = Image.new('RGB', (width, height))	

		line = Image.open(path + '/src/LINE S (s).jpg')
		h_line = line.size[1]+1	

		ImageDraw.Draw(new_im).rectangle([0, 0, width, height], fill='white', outline=None)	

		x_offset = 50
		y_offset = 50
		i = 0
		x_gap = 0
		for image in images:
			x_gap = (width-widths[i])//2
			ImageDraw.Draw(new_im).rectangle([x_offset, y_offset, x_gap, y_offset+917], fill='white', outline=None)
			x_offset = x_gap
			for im in image:
				if ((im.size[1] == 917) and (x_offset != (width-widths[i])//2)):
					line_sized = line.resize((x_offset, h_line))
					new_im.paste(line_sized, (0, y_offset+833))
				if ((im.size[1] == 917) and (x_offset == (width-widths[i])//2)):
					new_im.paste(im, (x_offset,y_offset+1))
					y_offset+=h_line
				else:
					new_im.paste(im, (x_offset,y_offset))
				x_offset += im.size[0]
			i += 1
			x_offset = 0
			y_offset += 833	

		for letter in text:
			text = text.replace('\n', '')	

		new_im = new_im.save("output/test.jpg");

	except AssertionError as error:
		print(error)


generate("hi")