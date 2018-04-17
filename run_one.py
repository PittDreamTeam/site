import pickle
from PIL import Image
import model

def get_im():
    net = pickle.load( open( "net.pickle", "rb" ) )
    im = Image.open("static/upload/picture.jpg")
    cars = model.find_cars(net, im)
    new_im = model.mark_cars(net, im)
    return new_im
