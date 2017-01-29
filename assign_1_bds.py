import time
start_time = time.time()


import resource
import sys
import copy

exhaust_Set_fwd = []	# closed list that has the visited nodes in the forward search...
exhaust_Set_bwd = []	# closed list that has the visited nodes in the backward search...
exhaust_nodes_bwd = []	# closed list that has the visited nodes in the fwd_search to retracce the path...
exhaust_nodes_fwd = []	# closed list that has the visited nodes in the bwd_search to retrace the path...
nodesprinted=0;
class Node:
    def __init__(self,config,prev_node = None):
        self.setting = list(config)
        self.pos = -1
        self.prev_node = prev_node	# parent reference node that is used while backtracking...
        for i in range(9):
            if self.setting[i] == 0 :
                self.pos = i		# get the initial position of the blank space...
                break
        
    def swap(self,i1,j1):			# swap the space at i1th position with j1th position...
        temp = self.setting[i1]
        self.setting[i1] = self.setting[j1]
        self.setting[j1] = temp

    def up(self):				# swap the blank space with the top tile...
        k = False
        try:
            if (self.pos - 3 >= 0):
                self.swap(self.pos,self.pos-3)
                self.pos = self.pos - 3
                k = True
        except:
            pass
        return k

    def down(self):			# swap the blank space with the down tile...
        k = False
        try:
            self.swap(self.pos,self.pos+3)
            self.pos = self.pos+3
            k = True
        except:
            pass
        return k

    def left(self):			# swap the blank space with the left tile...
        k = False
        try:
            if (self.pos % 3 != 0):
                self.swap(self.pos,self.pos-1)
                self.pos = self.pos - 1
                k = True
        except:
            pass
        return k

    def right(self):		# swap the blank space with the right tile...
        k = False
        try:
            if (self.pos % 3 != 2):
                self.swap(self.pos,self.pos+1)
                self.pos = self.pos + 1
                k = True
        except:
            pass
        return k

    def printconfig(self):
	global nodesprinted;
	nodesprinted+=1;	# print the configuration of the current node...
        for i in range(1,10):
            print self.setting[i-1],
            if i%3 == 0:
                print '\r'
        print '-------------------'

def listrev(nod):		# reversing the reference nodes from (parent <- child) to (parent -> child) and print the path...
    curr_node = None
    while(nod.prev_node != None):
        back_node = nod.prev_node
        nod.prev_node = curr_node
        curr_node = nod
        nod = back_node
    nod.prev_node = curr_node
    while (nod.prev_node != None):
        nod.printconfig()
        nod = nod.prev_node
    #nod.printconfig()

def bds(q1,q2,start,end):
    q1.append(start)	# queue 1 for the fwd_search...	
    q2.append(end)		# queue 2 for the bwd_search...
    notfound = True
    count = 0
    while((len(q1)!=0 and len(q2)!=0)and notfound):
        temp1 = q1.pop(0)
        temp2 = q2.pop(0)
        exhaust_Set_fwd.append(temp1.setting)
        exhaust_Set_bwd.append(temp2.setting)
        exhaust_nodes_fwd.append(temp1)
        exhaust_nodes_bwd.append(temp2)

        #if (temp1.setting == end.setting or temp2.setting == start.setting or temp1.setting in exhaust_Set_bwd or temp2.setting in exhaust_Set_fwd):
         #   print 'found'

        if (temp1.setting == end.setting):	# case where the fwd_search finds the end or goal state...
            print 'found1'
            notfound = False
	    listrev(temp1)
            #while(temp1.prev_node != None):
            #    temp1.printconfig()
            #    temp1 = temp1.prev_node
            temp1.printconfig()

        elif (temp2.setting == start.setting):	# case where the bwd_Search finds the end or goal state...
            print 'found2'
            notfound = False
            while(temp2.prev_node != None):
                temp2.printconfig()
                temp2 = temp2.prev_node
            temp2.printconfig()

        elif (temp1.setting in exhaust_Set_bwd):	# case where the fwd_search encounters a state that has already been reached by the bwd_search...
            print 'found3'
            notfound = False
            listrev(temp1)
            print '-------------End of First Search-------------'
            for noddy in exhaust_nodes_bwd :
                if (noddy.setting == temp1.setting):
                    while(noddy.prev_node != None):
                        noddy.printconfig()
                        noddy = noddy.prev_node
                    noddy.printconfig()
                    break

        elif (temp2.setting in exhaust_Set_fwd):	# case where the bwd_search encounters a state that has already been reached by the fwd_search...
            print 'found4'
            notfound = False
            for noddy in exhaust_nodes_fwd :
                if (noddy.setting == temp2.setting):
                    listrev(noddy)
                    break
            print '--------------End of First Search------------'
            while(temp2.prev_node != None):
                temp2.printconfig()
                temp2 = temp2.prev_node
            temp2.printconfig()

        else :								# else perform the bfs search...
											# creating a copy of the current node to generate child nodes in both fwd and bwd_searches...
            temp1_l = copy.deepcopy(temp1)
            temp1_r = copy.deepcopy(temp1)
            temp1_u = copy.deepcopy(temp1)
            temp1_d = copy.deepcopy(temp1)

            temp2_d = copy.deepcopy(temp2)
            temp2_u = copy.deepcopy(temp2)
            temp2_r = copy.deepcopy(temp2)
            temp2_l = copy.deepcopy(temp2)

            if (temp1_u.up()):
                if temp1_u.setting not in exhaust_Set_fwd :
                    temp1_u.prev_node = temp1
                    q1.append(temp1_u)

            if (temp1_d.down()):
                if temp1_d.setting not in exhaust_Set_fwd :
                    temp1_d.prev_node = temp1
                    q1.append(temp1_d)

            if (temp1_r.right()):
                if temp1_r.setting not in exhaust_Set_fwd :
                    temp1_r.prev_node = temp1
                    q1.append(temp1_r)
                
            if (temp1_l.left()):
                if temp1_l.setting not in exhaust_Set_fwd :
                    temp1_l.prev_node = temp1
                    q1.append(temp1_l)

            if (temp2_u.up()):
                if temp2_u.setting not in exhaust_Set_bwd :
                    temp2_u.prev_node = temp2
                    q2.append(temp2_u)

            if (temp2_d.down()):
                if temp2_d.setting not in exhaust_Set_bwd :
                    temp2_d.prev_node = temp2
                    q2.append(temp2_d)
            
            if (temp2_r.right()):
                if temp2_r.setting not in exhaust_Set_bwd :
                    temp2_r.prev_node = temp2
                    q2.append(temp2_r)

            if (temp2_l.left()):
                if temp2_l.setting not in exhaust_Set_bwd :
                    temp2_l.prev_node = temp2
                    q2.append(temp2_l)

            count += 1
    #print count ," this is path cost";

    
end = [1,2,3,
        4,5,6,
        7,8,0]
# the input is given in the start list... it should space separated in a single line please give accordingly.
print "\nNote the time taken and other computational resources  over 20 different experiments has been recorded in assgn report\n"
print "The input shpould be space separated in a single line please give accordingly"
start = []
#start = [1,2,3,
#        4,0,5,
#        6,7,8]
start = map(int,raw_input().strip().split(' '))
q1 = []
q2 = []
node1 = Node(start)
node2 = Node(end)
#k= copy.deepcopy(node1.setting)


bds(q1,q2,node1,node2)
print("--- %s seconds ---" % (time.time() - start_time))
print "bytes used",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print "The path length",nodesprinted

