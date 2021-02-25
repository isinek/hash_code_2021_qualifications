class Car():
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return str(self.path)


class CityMap():
    def __init__(self):
        self.streets = {}
        self.intersections = {}

    def addIntersection(self, input_line):
        B, E, street_name, L = input_line
        B, E, L = int(B), int(E), int(L)
        self.streets[street_name] = {'duration': L, 'intersections': [B, E], 'traffic_light': 0, 'visitations': {}}

        if not E in self.intersections:
            self.intersections[E] = set()
        self.intersections[E].add(street_name)

    def print_out(self, print_out_file):
        with open(print_out_file + '.out', 'w') as f:
            streets_w_schedule = [s for s in self.streets if self.streets[s]['traffic_light']]
            intersections_w_schedule = {}
            for s in streets_w_schedule:
                if not self.streets[s]['intersections'][1] in intersections_w_schedule:
                    intersections_w_schedule[self.streets[s]['intersections'][1]] = []
                intersections_w_schedule[self.streets[s]['intersections'][1]] += [s]
            f.write('%d\n' % len(intersections_w_schedule))

            for i in intersections_w_schedule:
                f.write('%d\n%d\n' % (i, len(intersections_w_schedule[i])))
                intersections_w_schedule[i].sort(key=lambda x: len(self.streets[s]['visitations']))
                for s in intersections_w_schedule[i]:
                    f.write('%s %d\n' % (s, self.streets[s]['traffic_light']))

    def calc_statistics(self, cars):
        for c in cars:
            for i in range(1, len(c.path)):
                if not c.path[i - 1] in self.streets[c.path[i]]['visitations']:
                    self.streets[c.path[i]]['visitations'][c.path[i - 1]] = 1/i
                else:
                    self.streets[c.path[i]]['visitations'][c.path[i - 1]] += 1/i

    def print_stats(self):
        for s in self.streets:
            print('%s:\tL = %d;\tE = %d;\ttraffic_light = %d' % (s, self.streets[s]['duration'], self.streets[s]['intersections'][1], self.streets[s]['traffic_light']))
            print('\tvisitations:')
            for v in self.streets[s]['visitations']:
                print('\t\t%s %d' % (v, self.streets[s]['visitations'][v]))

    def calc_traffic_lights_from_stats(self):
        tmp_traffic_lights = {}
        for s in self.streets:
            for v in self.streets[s]['visitations']:
                if not v in tmp_traffic_lights:
                    tmp_traffic_lights[v] = self.streets[s]['visitations'][v]
                else:
                    tmp_traffic_lights[v] += self.streets[s]['visitations'][v]

        for i in self.intersections:
            tmp_intersection_times = sum([tmp_traffic_lights[s] for s in self.intersections[i] if s in tmp_traffic_lights])
            for s in self.intersections[i]:
                if s in tmp_traffic_lights:
                    tmp_traffic_lights[s] /= tmp_intersection_times

        for s in self.streets:
            if s in tmp_traffic_lights:
                self.streets[s]['traffic_light'] = round(tmp_traffic_lights[s] + 0.5)
                if self.streets[s]['duration'] < self.streets[s]['traffic_light']:
                    self.streets[s]['traffic_light'] = self.streets[s]['duration']

        return


def input_data(input_file):
    city_map = CityMap()
    cars = []
    with open(input_file) as f:
        D, I, S, V, F = [int(x) for x in f.readline().split()]

        for _ in range(S):
            city_map.addIntersection(f.readline().split())

        for _ in range(V):
            full_path = f.readline().split()[1:]
            path = [full_path[0]]
            path_duration = 0
            for s in full_path[1:]:
                path_duration += city_map.streets[s]['duration']
                if path_duration > D:
                    break
                path += [s]
            cars += [Car(path)]

    return city_map, cars


def solution(f, city_map, cars):
    city_map.calc_statistics(cars)
    city_map.calc_traffic_lights_from_stats()
    # city_map.print_stats()

    city_map.print_out(f)


if __name__ == '__main__':
    for f in ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt', 'f.txt']:
        city_map, cars = input_data(f)
        solution(f, city_map, cars)
