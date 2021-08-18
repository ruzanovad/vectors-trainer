import igraph
import bs4

from random import shuffle, uniform, randint, choice
from os import path
from decimal import Decimal


def resource_path(relative_path):
    return path.join(path.abspath(path.dirname(__file__)), relative_path)


class Task:
    """
    Class for creating task with solution and predefined files for displaying.
    """

    def __init__(self, complexity: int, taskname: str, n: int):
        self.complexity = complexity
        self.taskname = taskname
        self.number_of_task = n

    def produce(self):  # producing task
        if self.taskname == 'Формальные описания реальных объектов и процессов_ОГЭ':  # randomizing values for each level
            if self.complexity == 0:  # setup complexity
                count = 5
                count_paths = randint(6, 8)
            elif self.complexity == 1:
                count = randint(5, 6)
                count_paths = randint((count * (count - 1) // 3.5) + 3, (count * (count - 1) // 2) - 2)
            else:
                count = randint(6, 9)
                count_paths = randint((count * (count - 1) // 3), (count * (count - 1) // 2) - 2)

            cities = []

            all_available_cities = [chr(i) for i in range(65, 90)]

            for i in range(count):  # setting available cities (random latin letters)
                internal_choice = choice(all_available_cities)
                all_available_cities.remove(internal_choice)
                cities.append(internal_choice)

            cities = sorted(cities)  # sorting alphabetically

            self.whattosolve = sorted([cities[0], cities[-1]])  # choosing couple of required cities

            self.graph = igraph.Graph.Erdos_Renyi(n=len(cities), m=count_paths,
                                                  directed=None, loops=False)  # creating Erdos-Renyi modelled graph
            pseudo = cities.copy()  # creating copy of list with cities' letters
            shuffle(pseudo)

            self.graph.vs["label"] = pseudo  # setup vertices' labels and names for plot
            self.graph.vs["name"] = pseudo

            # verifying if required cities' vertices have only one edge
            # and creating additional edges if required
            if self.graph.degree(pseudo.index(self.whattosolve[0])) < 2:
                for i in range(len(pseudo)):
                    if (pseudo.index(self.whattosolve[0]),
                        i) not in self.graph.get_edgelist() and (
                            (i, pseudo.index(self.whattosolve[0])) not in self.graph.get_edgelist()) \
                            and (i != pseudo.index(self.whattosolve[0])):
                        self.graph.add_edges([(i, pseudo.index(self.whattosolve[0]))])
                    break

            if self.graph.degree(pseudo.index(self.whattosolve[1])) < 2:
                for i in range(len(pseudo)):
                    if (pseudo.index(self.whattosolve[1]),
                        i) not in self.graph.get_edgelist() and (
                            (i, pseudo.index(self.whattosolve[1])) not in self.graph.get_edgelist()) \
                            and i != pseudo.index(self.whattosolve[1]):
                        self.graph.add_edges([(i, pseudo.index(self.whattosolve[1]))])
                    break

            # randomizing weights for edges based on level
            if self.complexity == 0:
                weights = [Decimal(str(uniform(1, 7))).quantize(Decimal("1.0")) for i in
                           range(self.graph.ecount())]
            elif self.complexity == 1:
                weights = [randint(1, 7) for i in range(self.graph.ecount())]
            else:
                weights = [randint(1, 20) for i in range(self.graph.ecount())]

            name = self.graph.get_edgelist()  # creating list with names of edges in dependence of vertices' letters
            for i in range(len(name)):
                name[i] = (self.graph.vs["name"][name[i][0]], self.graph.vs["name"][name[i][1]])

            self.graph.es["name"] = name  # setting names
            self.graph.es["label"] = weights  # setting labels for plot
            self.graph.es["weight"] = weights  # setting weights

            self.graph.vs['whattosolve'] = 'm'

            self.graph.vs[pseudo.index(self.whattosolve[0])]["whattosolve"] = 'f'
            self.graph.vs[pseudo.index(self.whattosolve[1])]["whattosolve"] = 'f'

            color_dict = {"m": "white", "f": "pink"}
            self.graph.vs["color"] = [color_dict[color] for color in
                                      self.graph.vs["whattosolve"]]  # coloring required cities in another color

            table = [['' for i in range(len(cities) + 1)] for j in range(len(cities) + 1)]  # table for html
            for i in range(len(table)):
                for j in range(len(table)):
                    if i == j:  # because such edges as "AA", "BB" don't exist
                        table[i][j] = '#4C514A'  # in table their cells will be colored in dark grey
                    elif i == 0 and j != 0:
                        table[i][j] = cities[j - 1]  # filling 1st row
                    elif i != 0 and j == 0:
                        table[i][j] = cities[i - 1]  # filling 1st column
                    elif (table[0][j], table[i][0]) in self.graph.es['name']:  # filling cell with connected weight
                        table[i][j] = self.graph.es['weight'][self.graph.es['name'].index((table[0][j], table[i][0]))]
                    elif (table[i][0], table[0][j]) in self.graph.es['name']:
                        table[i][j] = self.graph.es['weight'][self.graph.es['name'].index((table[i][0], table[0][j]))]

                    else:
                        table[i][j] = '#C0C0C0'  # if edge doesn't exist, its cell will be colored in light grey

            pseudo_table = table.copy()
            for i in range(len(pseudo_table)):
                pseudo_table[i].reverse()

            pseudo_table.reverse()  # reversing table for correct display

            with open(resource_path('{}.html'.format(self.taskname)), 'r', encoding='utf-8') as example:
                html = bs4.BeautifulSoup(example.read(), features="lxml")  # opening example file

            self.html_table = html.find('table')

            for i in range(len(pseudo_table)):  # filling html table
                a = html.new_tag('tr')
                for j in range(len(pseudo_table[i])):
                    x = len(cities)
                    if (i == x and j != x) or (i != x and j == x) or (j == i == x):
                        b = html.new_tag('th')
                    else:
                        b = html.new_tag('td')
                    if pseudo_table[i][j] == '#4C514A':
                        b.attrs['class'] = 'invalid'
                    elif pseudo_table[i][j] == '#C0C0C0':
                        b.attrs['class'] = 'empty'
                    else:
                        b.string = str(pseudo_table[i][j])
                    a.insert(0, b)
                self.html_table.insert(0, a)

            cities_h, whattosolve1, whattosolve2 = html.find_all('i')  # finding tags for filling concern information

            # replacing
            cities_h.replaceWith(', '.join([cities[i] for i in range(len(cities) - 1)]) + ' и {}'.format(cities[-1]))
            whattosolve1.replaceWith(self.whattosolve[0])
            whattosolve2.replaceWith(self.whattosolve[1])

            html.find('h1').insert(0, self.taskname)

            with open(resource_path("{}_{}.html".format(self.taskname, str(self.number_of_task))), "w",
                      encoding='utf-8') as file:
                file.write(str(html))  # writing new file
        elif self.taskname == 'Анализирование информации, представленной в виде схем_ОГЭ':

            if self.complexity == 0:  # setup complexity
                count = 5
            elif self.complexity == 1:
                count = randint(5, 6)
            else:
                count = randint(6, 9)

            cities = set()

            while len(cities) != count:  # setting available cities (random latin letters)
                cities.add(chr(randint(65, 90)))
            cities = sorted(list(cities))  # sorting alphabetically

            self.whattosolve = sorted([cities[0], cities[-1]])  # choosing couple of required cities

            self.graph = igraph.Graph(directed=True)
            self.graph.add_vertices(len(cities))

            for i in range(0, len(cities) - 1):
                x = randint(1, len(cities))
                c = cities[i + 1:len(cities)]
                count = 0
                while count != x and len(c) != 0:
                    a = choice(c)
                    c.remove(a)
                    if ((i, cities.index(a)) and (cities.index(a), i) not in self.graph.get_edgelist()) and str(
                            cities.index(
                                a)) != str(i):
                        self.graph.add_edge(i, cities.index(a))
                    count += 1

            self.graph.vs["label"] = cities  # setup vertices' labels and names for plot
            self.graph.vs["name"] = cities

            # verifying if required cities' vertices have only one edge
            # and creating additional edges if required
            if self.graph.degree(cities.index(self.whattosolve[0])) < 2:
                for i in range(len(cities)):
                    if (cities.index(self.whattosolve[0]),
                        i) not in self.graph.get_edgelist() and (
                            (i, cities.index(self.whattosolve[0])) not in self.graph.get_edgelist()) \
                            and i != cities.index(self.whattosolve[0]):
                        self.graph.add_edges([(i, cities.index(self.whattosolve[0]))])
                    break

            if self.graph.degree(cities.index(self.whattosolve[1])) < 2:
                for i in range(len(cities)):
                    if (cities.index(self.whattosolve[1]),
                        i) not in self.graph.get_edgelist() and (
                            (i, cities.index(self.whattosolve[1])) not in self.graph.get_edgelist()) \
                            and i != cities.index(self.whattosolve[1]):
                        self.graph.add_edges([(i, cities.index(self.whattosolve[1]))])
                    break

            name = self.graph.get_edgelist()  # creating list with names of edges in dependence of vertices' letters
            for i in range(len(name)):
                name[i] = (self.graph.vs["name"][name[i][0]], self.graph.vs["name"][name[i][1]])

            self.graph.es["name"] = name  # setting names

            self.graph.vs['whattosolve'] = 'm'

            self.graph.vs[cities.index(self.whattosolve[0])]["whattosolve"] = 'f'
            self.graph.vs[cities.index(self.whattosolve[1])]["whattosolve"] = 'f'

            additional = choice([choice(cities[1:-2]), None])
            if additional is not None:
                self.whattosolve.append(additional)
                self.graph.vs[cities.index(self.whattosolve[2])]["whattosolve"] = 'f'

            color_dict = {"m": "white", "f": "pink"}
            self.graph.vs["color"] = [color_dict[color] for color in
                                      self.graph.vs["whattosolve"]]  # coloring required cities in another color

            with open(resource_path('{0}.html'.format(self.taskname)), 'r', encoding='utf-8') as example:
                html = bs4.BeautifulSoup(example.read(), features="lxml")  # opening example file

            cities_h, whattosolve1, whattosolve2 = html.find_all('i')
            cities_h.replace_with(', '.join(cities))
            whattosolve1.replace_with(self.whattosolve[0])
            if additional is not None:
                whattosolve2.replace_with('{0} через город {1}'.format(self.whattosolve[1], self.whattosolve[2]))
            else:
                whattosolve2.replace_with(self.whattosolve[1])

            igraph.plot(self.graph, resource_path("{0}_{1}.svg".format(self.taskname, self.number_of_task)),
                        layout=self.graph.layout("kk"))

            attrs = html.find('img').attrs
            attrs['src'] = "{0}_{1}.svg".format(self.taskname, self.number_of_task)
            html.find('img').attrs.update(attrs)

            html.find('h1').insert(0, self.taskname)

            with open(resource_path("{0}_{1}.html".format(self.taskname, str(self.number_of_task))), "w",
                      encoding='utf-8') as file:
                file.write(str(html))  # writing new file

    def solve(self):
        if self.taskname == 'Формальные описания реальных объектов и процессов_ОГЭ':

            l = []
            l_other = []
            l_solution = []
            for i in range(self.graph.ecount()):
                a = self.graph.vs[self.graph.get_edgelist()[i][0]]["label"]
                b = self.graph.vs[self.graph.get_edgelist()[i][1]]["label"]
                if (a is self.whattosolve[0] or b is self.whattosolve[0]) is False:
                    l_other.append('{0}{1}'.format(a, b))
                else:
                    l_solution.append('{0}{1}'.format(a, b))
                l.append('{0}{1}'.format(a, b))

            self.ways = {}
            temp = ''
            visited = dict(zip(self.graph.vs["name"], [False for j in range(len(self.graph.vs["name"]))]))
            self.findways(self.graph, self.whattosolve[0], self.whattosolve[1], self.ways, visited, temp, l)

            for i in self.ways.keys():
                list_for = [(i[j], i[j + 1]) for j in range(len(i) - 1)]
                weight = 0
                for j in list_for:
                    try:
                        weight += self.graph.es["weight"][self.graph.es["name"].index(j)]
                    except Exception:
                        j = (j[1], j[0])
                        weight += self.graph.es["weight"][self.graph.es["name"].index(j)]
                self.ways[i] = weight

        elif self.taskname == 'Анализирование информации, представленной в виде схем_ОГЭ':

            list_of_paths_reversed = [[j for j in self.graph.get_edgelist() if j[1] == i] for i in
                                      range(self.graph.vcount() - 1, -1, -1)]

            dict_of_paths = {}
            for i in range(len(self.graph.vs["name"])):
                x = []
                if list_of_paths_reversed[i] is not []:
                    for j in range(len(list_of_paths_reversed[i])):
                        if list_of_paths_reversed[i][j].index(len(self.graph.vs["name"]) - 1 - i) == 0:
                            x.append(self.graph.vs["name"][list_of_paths_reversed[i][j][1]])
                        else:
                            x.append(self.graph.vs["name"][list_of_paths_reversed[i][j][0]])
                    dict_of_paths[self.graph.vs["name"][len(self.graph.vs["name"]) - 1 - i]] = x

            self.dict_of_paths = dict_of_paths

    def display(self):
        if self.taskname == 'Формальные описания реальных объектов и процессов_ОГЭ':
            with open(resource_path('{0}_answer.html'.format(self.taskname)), 'r',
                      encoding='utf-8') as html_answer:
                html = bs4.BeautifulSoup(html_answer.read(), features="lxml")  # opening example file

            attrs = html.find('table').attrs
            html.find('table').replace_with(self.html_table)
            html.find('table').attrs.update(attrs)

            whattosolve_answer, list_of_paths, string_route, weight_route, answer = html.find_all('i')
            whattosolve_answer.replaceWith('{0} в {1}'.format(self.whattosolve[0], self.whattosolve[1]))
            ways_items = sorted(self.ways.items(), key=lambda x: x[1], reverse=True)

            if len(ways_items) > 11:
                displayed_items = ways_items[-10:-1]
            else:
                displayed_items = ways_items

            for i in displayed_items:
                list_of_paths.append('Длина маршрута {0} равна {1} км.'.format(i[0], i[1]))
                list_of_paths.append(html.new_tag('br'))

            string_route.replaceWith(displayed_items[-1][0])
            weight_route.replaceWith(str(displayed_items[-1][1]))
            answer.replaceWith(str(displayed_items[-1][1]))

            self.answer = str(displayed_items[-1][1])

            igraph.plot(self.graph, resource_path("{0}_{1}.svg".format(self.taskname, str(self.number_of_task))),
                        layout=self.graph.layout("kk"))

            attrs = html.find('img').attrs
            attrs['src'] = "{0}_{1}.svg".format(self.taskname, str(self.number_of_task))
            html.find('img').attrs.update(attrs)

            html.find('h1').insert(0, self.taskname)

            with open(resource_path("{0}_answer_{1}.html".format(self.taskname, str(self.number_of_task))), "w",
                      encoding='utf-8') as file:
                file.write(str(html))  # writing new file
        elif self.taskname == 'Анализирование информации, представленной в виде схем_ОГЭ':
            with open(resource_path('{0}_answer.html'.format(self.taskname)), 'r',
                      encoding='utf-8') as html_answer:
                html = bs4.BeautifulSoup(html_answer.read(), features="lxml")  # opening example file

            html.find('h1').insert(0, self.taskname)

            step_by_step_tag = html.new_tag('i')
            s_s_tag_add = step_by_step_tag.append
            if len(self.whattosolve) > 2:
                for i in sorted(self.dict_of_paths.items(), key=lambda x: str(x[0])):
                    step_tag = html.new_tag('i')
                    s_tag_add = step_tag.append
                    if i[0] == self.whattosolve[2]:
                        if len(i[1]) is 0:
                            first = html.new_tag('font')
                            first.string = i[0]
                            second = html.new_tag('font')
                            second.string = i[0]
                            s_tag_add(first)
                            s_tag_add(' = ')
                            s_tag_add(second)
                        else:
                            first = html.new_tag('font')
                            first.string = i[0]
                            s_tag_add(first)
                            s_tag_add(' = {0}'.format(' + '.join(i[1])))
                    elif self.whattosolve[2] in i[1]:
                        if i[1] == [self.whattosolve[2]]:
                            additional = html.new_tag('font')
                            additional.string = self.whattosolve[2]
                            s_tag_add('{0} = '.format(i[0]))
                            s_tag_add(additional)
                        else:
                            additional_tag = html.new_tag('font')
                            additional_tag.string = self.whattosolve[2]
                            list_with_tags = [i[1][j // 2] if j % 2 == 0 else ' + ' for j in range(2 * len(i[1]) - 1)]
                            for j in range(len(list_with_tags)):
                                if list_with_tags[j] == self.whattosolve[2]:
                                    list_with_tags[j] = additional_tag.__copy__()
                            s_tag_add('{0} = '.format(i[0]))
                            for j in list_with_tags:
                                s_tag_add(j)
                    else:
                        if len(i[1]) != 0:
                            s_tag_add('{0} = {1}'.format(i[0], ' + '.join(i[1])))
                        else:
                            s_tag_add('{0} = {1}'.format(i[0], i[0]))
                    s_s_tag_add(step_tag)
                    br = html.new_tag('br')
                    s_s_tag_add(br)
                a = self.findpaths(self.dict_of_paths, self.whattosolve[0], self.whattosolve[2])
                b = self.findpaths(self.dict_of_paths, self.whattosolve[2], self.whattosolve[1])
                additional_tag = html.new_tag('font')
                additional_tag.string = self.whattosolve[2]
                s_s_tag_add('{0} = '.format(self.whattosolve[1]))
                list_with_additionals = [additional_tag.__copy__() if i % 2 == 0 else ' + ' for i in
                                         range(2 * len(b) - 1)]
                for i in list_with_additionals:
                    s_s_tag_add(i)
                s_s_tag_add(html.new_tag('br'))
                s_s_tag_add(additional_tag.__copy__())
                s_s_tag_add(' = {0}'.format(' + '.join([self.whattosolve[0] for i in range(len(a))])))
                s_s_tag_add(html.new_tag('br'))
                s_s_tag_add(
                    'Умножим {0} на {1} => {2} * {3} = {4}.'.format(self.whattosolve[1], self.whattosolve[2],
                                                               str(len(b)), str(len(a)), len(b) * len(a)))
                self.answer = str(len(b) * len(a))
            else:
                for i in sorted(self.dict_of_paths.items(), key=lambda x: str(x[0])):
                    step_tag = html.new_tag('i')
                    s_tag_add = step_tag.append
                    if len(i[1]) == 0:
                        s_tag_add('{0} = {1}'.format(i[0], i[0]))
                    else:
                        s_tag_add('{0} = {1}'.format(i[0], ' + '.join(i[1])))
                    s_s_tag_add(step_tag)
                    br = html.new_tag('br')
                    s_s_tag_add(br)
                a = self.findpaths(self.dict_of_paths, self.whattosolve[0], self.whattosolve[1])
                s_s_tag_add(
                    '{0} = {1}'.format(self.whattosolve[1], ' + '.join([self.whattosolve[0] for i in range(len(a))])))
                s_s_tag_add(html.new_tag('br'))
                self.answer = str(len(a))
                s_s_tag_add(
                    'Количество путей равно {0}.'.format(self.answer))

            steps, answer = html.find_all('i')
            steps.replace_with(step_by_step_tag)
            answer.replace_with(self.answer)
            attrs = html.find('img').attrs
            attrs['src'] = "{0}_{1}.svg".format(self.taskname, str(self.number_of_task))
            html.find('img').attrs.update(attrs)

            with open(resource_path("{0}_answer_{1}.html".format(self.taskname, str(self.number_of_task))), "w",
                      encoding='utf-8') as file:
                file.write(str(html))  # writing new file

    @staticmethod
    def findways(graph: igraph.Graph, v1: str, v2: str, ways: dict, visited: dict, temp: str, edgelist: list):
        # generator for ways from 1st city to last city
        if v1 == v2:
            temp = '{0}{1}'.format(temp, v1)
            ways[temp] = False
            return True

        visited[v1] = True
        temp = '{0}{1}'.format(temp, v1)

        for i in range(len(graph.vs["name"])):
            if ('{0}{1}'.format(graph.vs["name"][i], graph.vs.find(name=v1)["name"]) in edgelist) and visited[
                graph.vs["name"][i]] is False:
                Task.findways(graph, graph.vs["name"][i], v2, ways, visited, temp, edgelist)
            elif ('{0}{1}'.format(graph.vs.find(name=v1)["name"], graph.vs["name"][i]) in edgelist) and visited[
                graph.vs["name"][i]] is False:
                Task.findways(graph, graph.vs["name"][i], v2, ways, visited, temp, edgelist)

        visited[v1] = False

    @staticmethod
    def findpaths(d: dict, source: str, target: str):

        try:
            d.pop(source)
        except KeyError:
            x = ''
            return x
        list_of_empty = []
        for i in d.items():
            if len(i[1]) == 0:
                list_of_empty.append(i[0])
        for i in list_of_empty:
            d.pop(i)
        try:
            x = ''.join(d[target].copy())
        except KeyError:
            x = ''
            return x
        for j in range(len(d.keys()) ** 2):
            for i in x:
                try:
                    update = ''.join(d[i].copy())
                    x = x.replace(i, update)
                except:
                    continue
        list_of_empty = []
        add = {i: x.count(i) for i in list(set([x[i] for i in range(len(x))]))}
        for i in add.items():
            if i[0] != source:
                list_of_empty.append(i[0])
        for i in list_of_empty:
            add.pop(i)
        x = ''.join([source for i in range(add[source])])
        return x


TASKS = ['Анализирование информации, представленной в виде схем_ОГЭ',
         'Формальные описания реальных объектов и процессов_ОГЭ']

if __name__ == '__main__':
    obj = Task(1, 'Анализирование информации, представленной в виде схем_ОГЭ', 0)
    obj.produce()
    obj.solve()
    obj.display()
