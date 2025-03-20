class Habitacion:
    def __init__(self, description="", north=0, east=0, south=0, west=0):
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west


def main():
    room_list = []
    room = Habitacion("Estás en un jardin enorme, todo verde, tienes una casa enorme de frente, con dos "
                      "puertas,una al oeste de la fachada, la principal, y otra grande, del daraje al "
                      "este", None, None, None, None)
    room_list.append(room)
    room = Habitacion("Llegas a la entrada, hay una mesita, con un cajon, y hay tres puertas, una al norte, una al este y "
                      "otra al oeste.", None, None, None, 1)
    room_list.append(room)
    room = Habitacion("Llegas al garaje, hay tres coches: un 240SX, un Skyline R34 y un BMW M3 E46. También hay dos puertas,"
                      " una al norte y otra al oeste", None, 1, None, 0)
    room_list.append(room)
    current_room = 0
    done = False
