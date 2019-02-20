import carLib.thinkland_rpi_car_client as car

ultrsonic = car.carControl()
ultrsonic.connect(('172.16.10.227', 12347))

while True:
    dis = ultrsonic.distance_from_obstacle(0)
    print(type(dis))
    print(dis)