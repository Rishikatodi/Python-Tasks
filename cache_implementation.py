import fileinput
class CacheItem(object):
    """Data structure of items stored in cache. Using doubly linked list for storing data."""
    def __init__(self, id, enroll_class, marks):
        self.key = id
        self.enroll_class = enroll_class
        self.marks = marks
        self.next = None
        self.prev = None


class CreateCacheList(object):

    def __init__(self):
        self.head = None
        self.tail = None
        self.hash_org = {}
        self.hash_lru = {}
        self.cnt = 0

    def removeFromCache(self, id):
        node = self.hash_org[id];
        print ("node to be removed: ",node)

        if (node == self.head):
            self.head = self.head.next
            if(self.head is not None):
                self.head.prev = None
	
        elif (node == self.tail):
            self.tail = self.tail.prev
            if (self.tail is not None):
                self.tail.next = None

        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        self.hash_org.pop(id, None)
        self.hash_lru.pop(id, None)


    def remove_lru(self):
        temp = self.head
        rem = 0
        remove_pos = {}
        while(temp!=self.tail):
            if(temp.key not in self.hash_lru):
                rem = 1
                self.removeFromCache(temp.key)
            temp = temp.next
        if(rem==0):
            """All keys are in self.hash_lru, so remove the one with lowest count"""
            remove_pos = {k:v for k,v in self.hash_lru.iteritems() if v==0}
            self.removeFromCache(remove_pos.keys()[0])
        return self.head


    def find_pos(self, marks):
        temp = self.head
        previous = None

        while(temp is not None):
            if(temp.marks<=marks):
                previous = temp
                temp = temp.next
            else:
                break
        return previous


    def insertInCache(self, id, enroll_class, marks):

        if(len(self.hash_org) == 20):
            """Cache full; replacement required"""
            self.head = self.remove_lru()

        data = CacheItem(id, enroll_class, marks)
	print ("CacheItem: ",data)
        if (self.head is None):
            self.head = data
            self.tail = data
        else:
            """find correct position to insert to maintain sorting"""
            node = self.find_pos(marks)
            print node
            adjust_tail = 0
            if(node is None):
                data.next = self.head
                self.head.prev = data
                data.prev = None
                self.head = data
            elif(node.next is None):
                adjust_tail = 1
                data.next = node.next
                data.prev = node
                node.next = data
            else:
                node.next.prev = data
                data.next = node.next
                node.next = data
                data.prev = node

            if(adjust_tail is 1):
		      self.tail = data

        self.hash_org[id] = data
        self.hash_lru[id] = self.cnt
        self.cnt+=1


    def read(self, id):
        """If requested id is in the cache, print the relevant data"""

        if(id in self.hash_org):
            print(self.hash_org[id].enroll_class, self.hash_org[id].marks)
            if(id not in self.hash_lru):
                self.hash_lru[id] = self.cnt
                self.cnt+=1
            else:
                """make this id's count as current count and adjust rest of the entries"""
                self.hash_lru[id] = self.cnt
                for entry in self.hash_lru:
                    if(self.hash_lru[entry]>0):
                        self.hash_lru[entry]-=1


    def update(self, id, new_class, new_marks):
        if id in self.hash_org:
            self.removeFromCache(id)
            self.insertInCache(id, new_class, new_marks)
        else:
            print("Requested student id not found in the cache")
            return


    def printReverse(self):
        temp = self.tail
        while (temp):
            print(temp.key + " ")
            temp = temp.prev
		
        print("\n")


class testCache(object):
    "Test cache functions using Student dataset"
    f = open("students_data.txt","r") 

    count = 0
    cache = CreateCacheList()
    lines = f.read().strip().split("\n")
    for line in lines:
        data = line.split(',')
        print data[0]
        cache.insertInCache(data[0],data[1],data[2])
        count+=1
        if (count == 20):
            break

    cache.read('16')
    line_new = lines[35]
    data = line_new.split(',')
    cache.insertInCache(data[0],data[1],data[2])
    
    cache.printReverse()
    
    cache.update ('10', 'V', 58)
    cache.printReverse()
