import json
from random import randint

from pygame import image, transform, Vector2

from simulation.lanes.bus_lane import Bus_Lane
from simulation.lanes.cyclist_lane import Clyclist_Lane
from simulation.intersection import Intersection
from simulation.lanes.car_lane import Car_Lane
from simulation.lanes.pedestrian_lane import Pedestrian_Lane
from simulation.road import Road


class Simulation:
    def __init__(self, width, height):

        self._background = image.load("simulation/images/background.png")
        self._width = width
        self._height = height
        self._background = transform.scale(self._background, (width, height))

        self.intersections = [Intersection("1"), Intersection("2")]

        roadC = Road("C")
        roadC.add_car_lane(Car_Lane(Vector2(968, 365), [Vector2(335, 375), Vector2(285, 434), Vector2(242, 579), Vector2(248, 800)], Vector2(435, 363), spawnable=False))
        roadC.add_car_lane(Car_Lane(Vector2(667, 337), [Vector2(340, 335), Vector2(245, 460), Vector2(215, 579), Vector2(225, 800)], Vector2(435, 337), spawnable=False))
        roadC.add_car_lane(Car_Lane(Vector2(667, 316), [Vector2(-50, 311)], Vector2(435, 316), spawnable=False))
        roadC.add_car_lane(Car_Lane(Vector2(667, 286), [Vector2(-50, 281)], Vector2(435, 286), spawnable=False))

        roadD = Road("D")
        roadD.add_car_lane(Car_Lane(Vector2(925, 420), [Vector2(1000, 400), Vector2(1042, 364), Vector2(1125, 222), Vector2(1138, 0), ], Vector2(975, 420), spawnable=False))
        roadD.add_car_lane(Car_Lane(Vector2(485, 440), [Vector2(1015, 429), Vector2(1072, 364), Vector2(1155, 222), Vector2(1160, 0), ], Vector2(975, 440), spawnable=False))
        roadD.add_car_lane(Car_Lane(Vector2(960, 469), [Vector2(1400, 469)], Vector2(980, 469), spawnable=False))
        roadD.add_car_lane(Car_Lane(Vector2(960, 499), [Vector2(1400, 499)], Vector2(980, 499), spawnable=False))

        roadE = Road("E")
        roadEp1 = Pedestrian_Lane(Vector2(1117, 180), [Vector2(1282, 179),Vector2(1342, 214),Vector2(1420, 211),], Vector2(1126, 180), spawnable=False)
        roadEp2 = Pedestrian_Lane(Vector2(1117, 180), [Vector2(934, 174),Vector2(880, 215),Vector2(-20, 211),], Vector2(1106, 180), spawnable=False)
        roadEp1_actual = Pedestrian_Lane(Vector2(1262, 183), [Vector2(1117, 180)], Vector2(1190, 180), connection=roadEp2, spawnable=False)
        roadEp2_actual = Pedestrian_Lane(Vector2(153, 217), [Vector2(1117, 180)], Vector2(997, 174), inbetween_light_positions=[Vector2(879, 214),Vector2(928, 175),], connection=roadEp1, spawnable=False)
        roadEc1 = Clyclist_Lane(Vector2(1263, 193), [Vector2(1109, 190), Vector2(942, 189),Vector2(941, 188),Vector2(890, 226),Vector2(-39, 212),], Vector2(1200, 192), spawnable=False)
        roadEc2 = Clyclist_Lane(Vector2(150, 219), [Vector2(1109, 190), Vector2(1200, 192),Vector2(1282, 192),Vector2(1343, 228),Vector2(1395, 228),], Vector2(996, 188),inbetween_light_positions=[Vector2(888, 226),Vector2(939, 187),], spawnable=False)
        roadE.add_pedestrian_lane(roadEp1_actual)
        roadE.add_pedestrian_lane(roadEp1)
        roadE.add_pedestrian_lane(roadEp2)
        roadE.add_pedestrian_lane(roadEp2_actual)
        roadE.add_cyclist_lane(roadEc1)
        roadE.add_cyclist_lane(roadEc2)
        roadE.add_car_lane(Car_Lane(Vector2(1060, 0), [Vector2(1077, 262), Vector2(1142, 408), Vector2(1263, 498), Vector2(1400, 501), ], Vector2(1065, 130)))
        roadE.add_car_lane(Car_Lane(Vector2(1040, 0), [Vector2(1025, 310), Vector2(968, 365),], Vector2(1045, 130), connection=roadC.get_car_lanes()[0]))
        roadE.add_car_lane(Car_Lane(Vector2(1020, 0), [Vector2(1000, 252), Vector2(957, 350), Vector2(784, 340), Vector2(667, 337)], Vector2(1022, 130), connection=roadC.get_car_lanes()[1]))
        roadE.add_bus_lane(Bus_Lane(Vector2(1090, 0), [Vector2(1102, 257),Vector2(1156, 379),Vector2(1261, 471),Vector2(1385, 467),],Vector2(1090, 130), linked_inbetween_positions=[Vector2(1025, 310), Vector2(968, 365),], linked_connection=roadC.get_car_lanes()[0], linked_light_position=Vector2(1110, 130)))

        roadF = Road("F")
        roadFp1 = Pedestrian_Lane(Vector2(1242, 410), [Vector2(1205, 790),], Vector2(1239, 428), spawnable=False)
        roadFp2 = Pedestrian_Lane(Vector2(1242, 410), [Vector2(1262, 180),Vector2(1265, 178),Vector2(1289, 179),Vector2(1340, 212),Vector2(1420, 213),], Vector2(1245, 375), spawnable=False)
        roadF.add_pedestrian_lane(Pedestrian_Lane(Vector2(1205, 790), [Vector2(1242, 410),], Vector2(1231, 520), connection=roadFp2))
        roadF.add_pedestrian_lane(roadFp2)
        roadF.add_pedestrian_lane(roadFp1)
        roadF.add_pedestrian_lane(Pedestrian_Lane(Vector2(1440, 211), [Vector2(1242, 410),], Vector2(1259, 223), connection=roadFp1, inbetween_light_positions=[Vector2(1341, 209),Vector2(1294, 185),Vector2(1262, 183),], split=roadEp1_actual))
        roadF.add_car_lane(Car_Lane(Vector2(1400, 357), [Vector2(939, 325), Vector2(667, 316), ], Vector2(1287, 350), connection=roadC.get_car_lanes()[2]))
        roadF.add_car_lane(Car_Lane(Vector2(1400, 337), [Vector2(939, 300), Vector2(667, 286), ], Vector2(1287, 330), connection=roadC.get_car_lanes()[3]))
        roadF.add_car_lane(Car_Lane(Vector2(1400, 310), [Vector2(1180, 266),Vector2(1134, 194),Vector2(1135, 0),], Vector2(1293, 295)))
        roadF.add_car_lane(Car_Lane(Vector2(1400, 275), [Vector2(1208, 231),Vector2(1159, 176),Vector2(1158, 0),], Vector2(1296, 265)))


        roadB = Road("B")
        roadBp1 = Pedestrian_Lane(Vector2(269, 615), [Vector2(110, 615),Vector2(491, 556),Vector2(1394, 566),], Vector2(1460, 566), spawnable=False)
        roadBp2 = Pedestrian_Lane(Vector2(268, 615), [Vector2(461, 612),Vector2(519, 571),Vector2(1450, 585),], Vector2(280, 615), spawnable=False)
        roadBp1_actual = Pedestrian_Lane(Vector2(137, 610), [Vector2(268, 615),], Vector2(196, 615), connection=roadBp2, spawnable=False)
        roadBp2_actual = Pedestrian_Lane(Vector2(460, 615), [Vector2(268, 615),], Vector2(398, 615), connection=roadBp1, spawnable=False)
        roadB.add_pedestrian_lane(roadBp1_actual)
        roadB.add_pedestrian_lane(roadBp1)
        roadB.add_pedestrian_lane(roadBp2)
        roadB.add_pedestrian_lane(roadBp2_actual)
        roadBcl1 = Clyclist_Lane(Vector2(116, 588), [Vector2(269, 591),Vector2(453, 591),Vector2(492, 553),Vector2(1420, 565),], Vector2(180, 594), spawnable=False)
        roadBcl2 = Clyclist_Lane(Vector2(1237, 563), [Vector2(269, 591),Vector2(116, 588),], Vector2(393, 592),inbetween_light_positions=[Vector2(1028, 559),Vector2(504, 555),Vector2(446, 591),], spawnable=False)
        roadB.add_cyclist_lane(roadBcl1)
        roadB.add_cyclist_lane(roadBcl2)
        roadB.add_car_lane(Car_Lane(Vector2(293, 797), [Vector2(289, 575), Vector2(260, 466), Vector2(180, 342), Vector2(107, 314), Vector2(-100, 317)], Vector2(293, 650)))
        roadB.add_car_lane(Car_Lane(Vector2(310, 797), [Vector2(314, 575), Vector2(280, 466), Vector2(183, 312), Vector2(100, 284), Vector2(70, 284), Vector2(-100, 287)], Vector2(315, 650)))
        roadB.add_car_lane(Car_Lane(Vector2(335, 798), [Vector2(342, 520), Vector2(400, 415), Vector2(925, 420)], Vector2(335, 650), connection=roadD.get_car_lanes()[0]))
        roadB.add_car_lane(Car_Lane(Vector2(360, 798), [Vector2(372, 520), Vector2(450, 440), Vector2(485, 440)], Vector2(358, 650), connection=roadD.get_car_lanes()[1]))
        roadB.add_bus_lane(Bus_Lane(Vector2(390, 798), [Vector2(365, 551), Vector2(379, 503), Vector2(450, 440), Vector2(485, 440)], Vector2(381, 650), connection=roadD.get_car_lanes()[1]))

        roadF.add_cyclist_lane(Clyclist_Lane(Vector2(1215, 800), [Vector2(1250, 411), Vector2(1271, 195), Vector2(1342, 226),Vector2(1399, 226),], Vector2(1243, 521), inbetween_light_positions=[Vector2(1237, 563),], split=roadBcl2))
        roadF.add_cyclist_lane(Clyclist_Lane(Vector2(1395, 227), [Vector2(1250, 411), Vector2(1215, 800) ], Vector2(1268, 220), inbetween_light_positions=[Vector2(1340, 227),Vector2(1263, 193),], split=roadEc1))

        roadA = Road("A")
        roadAp1 = Pedestrian_Lane(Vector2(154, 357), [Vector2(131, 608),Vector2(113, 608),Vector2(57, 575),Vector2(-20, 574),], Vector2(149, 412), spawnable=False)
        roadAp2 = Pedestrian_Lane(Vector2(150, 392), [Vector2(187, 0),], Vector2(153, 354), spawnable=False)
        roadAp1_actual = Pedestrian_Lane(Vector2(1, 198), [Vector2(154, 357),], Vector2(163, 257), connection=roadAp1, inbetween_light_positions=[Vector2(153, 217),], split=roadEp2_actual)
        roadAp2_actual = Pedestrian_Lane(Vector2(0, 575), [Vector2(150, 392), ], light_position=Vector2(131, 554), inbetween_light_positions=[Vector2(60, 576), Vector2(116, 611),Vector2(137, 610), ], split=roadBp1_actual, connection=roadAp2)
        roadA.add_cyclist_lane(Clyclist_Lane(Vector2(0, 216), [Vector2(135, 374), Vector2(115, 586),], Vector2(150, 250), inbetween_light_positions=[Vector2(150, 219)], split=roadEc2))
        roadA.add_cyclist_lane(Clyclist_Lane(Vector2(0, 556), [Vector2(135, 374), Vector2(172, 0),], Vector2(120, 550), inbetween_light_positions=[Vector2(60, 557),Vector2(116, 588),], split=roadBcl1))
        roadA.add_pedestrian_lane(roadAp1_actual)
        roadA.add_pedestrian_lane(roadAp2)
        roadA.add_pedestrian_lane(roadAp1)
        roadA.add_pedestrian_lane(roadAp2_actual)
        roadA.add_car_lane(Car_Lane(Vector2(0, 418), [Vector2(442, 450), Vector2(960, 469)], Vector2(80, 427), connection=roadD.get_car_lanes()[2]))
        roadA.add_car_lane(Car_Lane(Vector2(0, 448), [Vector2(442, 480), Vector2(960, 499)], Vector2(80, 457), connection=roadD.get_car_lanes()[3]))
        roadA.add_car_lane(Car_Lane(Vector2(0, 475), [Vector2(185, 514), Vector2(227, 558), Vector2(246, 612), Vector2(240, 774)], Vector2(80, 485)))
        roadA.add_car_lane(Car_Lane(Vector2(0, 500), [Vector2(155, 538), Vector2(210, 572), Vector2(220, 748), ], Vector2(75, 516)))

        self.intersections[0].add_road(roadA)
        self.intersections[0].add_road(roadB)
        self.intersections[0].add_road(roadC)
        self.intersections[1].add_road(roadD)
        self.intersections[1].add_road(roadE)
        self.intersections[1].add_road(roadF)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_background(self):
        return self._background

    def from_json(self, message):
        data = json.loads(message)
        for intersection in self.intersections:
            intersection.from_json(data[intersection.get_name()])

    def to_json(self):

        json_structure = {}
        for intersection in self.intersections:
            json_structure = {**json_structure, **intersection.to_json()}

        return json.dumps(json_structure)