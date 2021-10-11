import eel
from auto_listing_sub import *


@eel.expose
def auto_listing_sub(speed_rate):
    main(speed_rate)

eel.init("web")
eel.start("main.html",size=(500, 450))