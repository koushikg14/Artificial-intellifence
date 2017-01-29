import sys
import copy
sys.setrecursionlimit(1500)
exhaust_Set = [] # closed set that maintains all the visited configurations...
class Node:
    def __init__(self,config,prev_node = None):
        self.setting = list(config)
        self.pos = -1
        self.prev_node = prev_node	# parent reference node that is used while backtracking...
        for i in range(9):
                if self.setting[i] == 0 :
                    self.pos = i	# get the initial position of the blank space...
                    break
        
    def swap(self,i1,j1):	# swap the space at i1th position with j1th position...
        temp = self.setting[i1]
        self.setting[i1] = self.setting[j1]
        self.setting[j1] = temp

    def up(self):	# swap the blank space with the top tile...
        k = False
        try:
            if (self.pos - 3 >= 0 ):
                self.swap(self.pos,self.pos-3)
                self.pos = self.pos-3
                k = True
        except:
            pass
        return k

    def down(self):	# swap the blank space with the down tile...
        k = False
        try:
            self.swap(self.pos,self.pos+3)
            self.pos = self.pos+3
            k = True
        except:
            pass
        return k

    def left(self):	# swap the blank space with the left tile...
        k = False
        try:
            if (self.pos % 3 != 0):
                self.swap(self.pos,self.pos-1)
                self.pos = self.pos - 1
                k = True
        except:
            pass
        return k

    def right(self):	# swap the blank space with the right tile...
        k = False
        try:
            if (self.pos % 3 != 2) :
                self.swap(self.pos,self.pos+1)
                self.pos = self.pos + 1
                k = True
        except:
            pass
        return k

    def printconfig(self):	# print the ccurrent configuration of the node...
        for i in range(1,10):
            print self.setting[i-1],
            if i%3 == 0 :
                print '\r'
        print '------------------'
        
def dfs(s,start,end):	# implementation of the dfs algorithm...
    s.append(start)	# initial append to the stack...
    notfound = True
    count = 0
    save_start = start
    while(len(s)!=0 and notfound):
        temp = s.pop()	# retrieving the top element from the stack...
        exhaust_Set.append(temp.setting)
        if (temp.setting == end):
            print 'found'
            notfound = False
        #temp.printconfig()
        else:
            temp_l = copy.deepcopy(temp)	# creating a copy of the current node to generate child nodes...
            temp_r = copy.deepcopy(temp)
            temp_u = copy.deepcopy(temp)
            temp_d = copy.deepcopy(temp)
        
            if (temp_u.up()):				# adding to the stack if only it is a valid move...
                if temp_u.setting not in exhaust_Set :
                    temp_u.prev_node = temp
                    s.append(temp_u) 
                    #temp_u.printconfig()
            if (temp_r.right()):
                if temp_r.setting not in exhaust_Set :
                    temp_r.prev_node = temp
                    s.append(temp_r)
                    #temp_r.printconfig()
            if (temp_d.down()):
                if temp_d.setting not in exhaust_Set :
                    temp_d.prev_node = temp
                    s.append(temp_d)
                    #temp_d.printconfig()
            if (temp_l.left()):
                if temp_l.setting not in exhaust_Set :
                    temp_l.prev_node = temp
                    s.append(temp_l)
                    #temp_l.printconfig()
            count += 1
    curr_node = None				# reversing the reference nodes from (parent <- child) to (parent -> child)...
    while (temp.prev_node != None and not notfound):
        #temp.printconfig()
        back_node = temp.prev_node
        temp.prev_node = curr_node
        curr_node = temp
        temp = back_node
    temp.prev_node = curr_node
    print '####################Solution#####################'# printing the sfound solution...
    while (temp.prev_node != None and not notfound):
        temp.printconfig()
        temp = temp.prev_node
    temp.printconfig()
    
end = [1,2,3,
        4,5,6,
        7,8,0]
# the input is the start list...
start = []
#start = [1,2,3,
#        4,0,5,
#        7,8,6]
start = map(int,raw_input().strip().split(' '))
s = []
node1 = Node(start)
#k= copy.deepcopy(node1.setting)
dfs(s,node1,end)
