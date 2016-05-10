#!/usr/bin/env python3

import sys
import heapq

class Vertex:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited        
        self.visited = False  
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_coor(self):
        return tuple([self.x,self.y])

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.x) + ',' + str(self.y) + ' adjacent: ' + str([coor for coor in self.adjacent])

    def __gt__(self,other):
        return self.get_distance() > other.get_distance()

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, x, y):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(x, y)
        self.vert_dict[tuple([x,y])] = new_vertex
        return new_vertex

    def get_vertex(self, x, y):
        if tuple([x,y]) in self.vert_dict:
            return self.vert_dict[tuple([x,y])]
        else:
            return None

    def add_edge(self, frm_x, frm_y, to_x, to_y, cost = 0):
        if tuple([frm_x,frm_y]) not in self.vert_dict:
            self.add_vertex(frm_x, frm_y)
        if tuple([to_x,to_y]) not in self.vert_dict:
            self.add_vertex(to_x, to_y)

        self.vert_dict[tuple([frm_x,frm_y])].add_neighbor(self.vert_dict[tuple([to_x,to_y])], cost)
        self.vert_dict[tuple([to_x,to_y])].add_neighbor(self.vert_dict[tuple([frm_x,frm_y])], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_coor())
        shortest(v.previous, path)
    return

def dijkstra(aGraph, start):
    print("Dijkstra's shortest path")
    # Set the distance for the start node to zero 
    #print(start)
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]

    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                '''
                print ('updated : current = %s next = %s new_dist = %s' \
                        %(current.get_coor(), next.get_coor(), next.get_distance()))
                '''
            else:
                '''
                print ('not updated : current = %s next = %s new_dist = %s' \
                        %(current.get_coor(), next.get_coor(), next.get_distance()))
                '''

        # Rebuild heap
        # 1. Pop every item
        '''
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        '''
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


def importGraph(filename, g,src,dest):
    with open(filename, 'r') as fptr:
        array = fptr.readlines()
        
    if int(array[src[1]][src[0]]) != 1:
        raise ValueError("source coordinates is not valid!")
    elif int(array[dest[1]][dest[0]]) != 1:
        raise ValueError("destination coordinates is not valid!")

    row = 0; col = 0;
    for item in array:
        array[row] = [int(x) for x in item.rstrip('\n')]
        row += 1

    max_row = len(array)
    max_col = len(array[0])
    '''
    ind_row = 0
    print_array = []
    while ind_row < 6:
        ind_col = 0
        while ind_col < 6:
            print_array.append(array[ind_row][ind_col])
            ind_col += 1
        ind_row += 1
        print(print_array)
        print_array=[]
    '''
    print(max_row);print(max_col)

    row = 0
    while row < max_row:
        col = 0
        while col < max_col:
            if array[row][col] == 1:
                g.add_vertex(col,row)
                adjacent_lst = get_adjacent(col,row,max_col,max_row,array)
                for item in adjacent_lst:
                    dest_col,dest_row = item
                    g.add_edge(col,row,dest_col,dest_row,1)
            col += 1
        row += 1


def get_adjacent(col,row,max_col,max_row,array):
    rtn_lst = []
    if col-1 >= 0 and row-1 >= 0:
        if array[row-1][col-1] == 1:
            rtn_lst.append(tuple([col-1,row-1]))
    if col >= 0 and row-1 >= 0:
        if array[row-1][col] == 1:
            rtn_lst.append(tuple([col,row-1]))
    if col+1 < max_col and row-1 >= 0:
        if array[row-1][col+1] == 1:
            rtn_lst.append(tuple([col+1,row-1]))

    if col-1 >= 0 and row >= 0:
        if array[row][col-1] == 1:
            rtn_lst.append(tuple([col-1,row]))
    if col+1 < max_col and row >= 0:
        if array[row][col+1] == 1:
            rtn_lst.append(tuple([col+1,row]))

    if col-1 >= 0 and row+1 < max_row:
        if array[row+1][col-1] == 1:
            rtn_lst.append(tuple([col-1,row+1]))
    if col >= 0 and row+1 < max_row:
        if array[row+1][col] == 1:
            rtn_lst.append(tuple([col,row+1]))
    if col+1 < max_col and row+1 < max_row:
        if array[row+1][col+1] == 1:
            rtn_lst.append(tuple([col+1,row+1]))

    return rtn_lst

def findPath(src,dest):
    g = Graph()

    filepath = 'New1.txt'

    #src = tuple([0,0])
    #dest = tuple([197,96])

    importGraph(filepath,g,src,dest)
    '''
    print(g.get_vertices)
    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_coor()
            wid = w.get_coor()
            print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    '''

    dijkstra(g, g.get_vertex(*src))

    target = g.get_vertex(*dest)

    path = [target.get_coor()]
    shortest(target, path)
    return path[::-1]
    #print ('The shortest path : %s' %(path[::-1]))

if __name__ == '__main__':
    print(findPath(tuple([140,61]),tuple([140,70])))
    '''imgdic = {    'Electrical Engineering':(140,61),
                        'Mechnical Engineering':(140,70),
                        'Neil Armstrong Hall of Engineering':(24,8),
                        'Physics':(109,36),
			'Materials and Electrical Engineering':(137,47),
			'Engineering Library':(146,86),
			'Polytechnic':(147,91),
			'Civil Engineering':(39,18),
			'Chemical Engineering':(72,40),
			'Office of the Vice President':(72,47),
			'Pharmacy':(21,39),
			'Student Health Center':(30,19),
			'Armory':(2,76),
			'Elliott Hall of Music':(51,66),
			'Hovde Hall of Administration':(71,71),
			'Psychological Sciences':(64,95),
                   }
    filename = 'New1.txt'
    with open(filename, 'r') as fptr:
        array = fptr.readlines()

    for item in imgdic.items():
        if int(array[item[1][1]][item[1][0]]) != 1:
            print(item)
            print(" coordinates is not valid!")'''
    #print(findPath(tuple([170,62]),tuple([140,70])))

