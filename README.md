This is a simple least recently used cache implementation.

Data Structures used: Double linked list, dictionary

Approach: 
Cache has 4 broad operations:
1. Insertion
2. Deletion
3. Updation
4. Read

I have used a structure to define attributes in student data set. While inserting a new value in cache I check if cache has reached its capacity or not. If cache has empty space for new item, a profer position is found to insert the new item maintaining the sorted order.
If cache reaches its capacity, least recently used item is moved out of the cache and new item is inserted.

In order to record least recently used items, I have taken help of another dictionary(hash_lru)
As an element is inserted into the cache, it is entered in hash_lru with key as student id and value as count.
If cache is full, item with least count is removed as it was the last one to be accessed.

Read operation is performed by searching for key in hash_org. If found, element is also inserted in hash_lru.
If the element was already present in hash_lru, its value is changed to max_count.

Removal is done by check the least used element from cache. Any item in hash_lru whose value is 0 (signifying old retrieval)
is removed.

Updation of an element by removing the previous occurence from cache and inserting a new value again.
