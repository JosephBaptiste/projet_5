from PIL import Image


# Les objets qui ne sont pas liés à Flask

def testfunc():
	return 0

class OpenGraphImage:

	def __init__(self):
		background = self.base()
		background.show()

	def base(self):
		img = Image.new('RGB', (1200, 630), '#18BC9C')
		return img
    
	def print_on_img(self, img, text, size, height):
		pass