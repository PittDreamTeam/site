import pickle
from PIL import Image
import model

def get_im():
    net = pickle.load( open( "net.pickle", "rb" ) )
    im = Image.open("static/upload/picture.jpg")
    return im
