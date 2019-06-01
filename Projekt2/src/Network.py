from xml.dom import minidom
import math


class Node:
    def __init__(self, uid, x, y):
        """
        pojedynczy wezel przedstawia jedno miasto
        :param uid: nazwa miasta
        :param x: wspolrzedna x na mapie
        :param y: wspolrzedna y na mapie
        """
        self.uid = uid
        self.x = x
        self.y = y
        self.linklist = []
        self.demand_list = []


class Link:
    def __init__(self, uid, source, target, capacity):
        """
        krawedz laczaca dwa miasta
        :param uid: identyfikator krawedzi
        :param source: miasto startowe
        :param target: miasto docelowe
        :param capacity: pojemnosc danej krawedzi
        """
        self.uid = uid
        self.source = source
        self.target = target
        self.capacity = capacity


class Demand:
    def __init__(self, uid, source, destination, demand_value, lambda_number):
        self.uid = uid
        self.source = source
        self.destination = destination
        self.demandValue = demand_value
        self.lambda_number = lambda_number
        self.admissiblePaths = []


class DemandPath:
    def __init__(self, uid):
        self.uid = uid
        self.links = []


class Network:
    def __init__(self, net_name="polska.xml", link_capacity=96, lambda_capacity=100):
        """
        Inicjalizacja sieci DWDM
        :param net_name: nazwa sieci, ktora chcemy zaladowac
        :param link_capacity: dopuszczalna ilosc lambd na danej krawedzi
        :param lambda_capacity: maksymalna ilosc danych przesylana przez jedna dlugosc fali
        """
        self.net_name = net_name
        self.link_capacity = link_capacity
        self.links_amount = 0
        self.demand_amount = 0
        self.demand_path_amount = 0
        self.lambda_capacity = lambda_capacity
        self.node_map = self.create_network()

    def create_network(self):
        """
        funkcja pobiera dane z pliku xml i na ich podstawie tworzy mape sieci
        :return: mapa sieci
        """
        read_data = minidom.parse(self.net_name)
        node_map = {}

        nodelist = read_data.getElementsByTagName("node")
        for node in nodelist:
            node_id = node.getAttribute("id")
            x_coordinates = node.getElementsByTagName('x')[0]
            x_coordinates = x_coordinates.childNodes[0].data
            y_coordinates = node.getElementsByTagName('y')[0]
            y_coordinates = y_coordinates.childNodes[0].data
            node_map[node_id] = Node(node_id, x_coordinates, y_coordinates)
            # print("%s : %s %s" % (node.getAttribute("id"), x_coordinates, y_coordinates))

        linklist = read_data.getElementsByTagName("link")
        for link in linklist:
            self.links_amount += 1
            link_id = link.getAttribute("id")
            source = link.getElementsByTagName('source')[0]
            source = source.childNodes[0].data
            destination = link.getElementsByTagName('target')[0]
            destination = destination.childNodes[0].data
            # Capacity = link.getElementsByTagName('capacity')[0]
            # Capacity = Capacity.childNodes[0].data
            linkobj = Link(link_id, source, destination, self.link_capacity)
            if source in node_map:
                node_map[source].linklist.append(linkobj)
            # if destination in node_map:
            #     node_map[destination].linklist.append(linkobj)

            # print("%s - %s to %s: %s" % (
            #     link.getAttribute("id"), source, destination, Capacity))
        demand_list = read_data.getElementsByTagName("demand")
        for demand in demand_list:
            self.demand_amount += 1
            demand_id = demand.getAttribute("id")
            source = demand.getElementsByTagName('source')[0]
            source = source.childNodes[0].data
            destination = demand.getElementsByTagName('target')[0]
            destination = destination.childNodes[0].data
            demand_val = demand.getElementsByTagName('demandValue')[0]
            demand_val = demand_val.childNodes[0].data
            lambda_number = int(math.ceil(float(demand_val) / float(self.lambda_capacity)))
            self.demand_path_amount += lambda_number
            demand_obj = Demand(demand_id, source, destination, demand_val, lambda_number)
            demand_path_list = demand.getElementsByTagName("admissiblePath")
            for demand_path in demand_path_list:
                demand_path_id = demand_path.getAttribute("id")
                link_id = demand_path.getElementsByTagName('linkId')
                demand_path_obj = DemandPath(demand_path_id)
                # print(demand_path_id)
                for i in link_id:
                    demand_path_obj.links.append(i.childNodes[0].data)
                    # print(i.childNodes[0].data)
                demand_obj.admissiblePaths.append(demand_path_obj)

            if source in node_map:
                node_map[source].demand_list.append(demand_obj)
            # if destination in node_map:
            #     node_map[destination].demand_list.append(demand_obj)

            # print("%s needs %s" % (demand.getAttribute("id"), demandval))

        return node_map

    def get_link_dictionary(self):
        node_map = self.node_map
        link_dict = {}
        for node in node_map:
            for link in node_map[node].linklist:
                link_dict[link.uid] = 0

        return link_dict

    def print_demand_paths(self):
        """
        funkcja wypisuje w terminalu mozliwe sciezki kazdego wymagania
        :return:
        """
        network = self.node_map
        i = 0
        for net in network:
            print(net)
            for demand in network[net].demand_list:
                i += 1
                print("%s - %s to %s: Value = %s" % (demand.uid, demand.source, demand.destination, demand.demandValue))
                for demand_path in demand.admissiblePaths:
                    print("\t%s" % demand_path.uid)
                    for link in demand_path.links:
                        print("\t\t%s" % link)

        print (i)
        print (self.demand_path_amount)

