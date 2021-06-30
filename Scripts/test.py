from multiprocessing import shared_memory

a = shared_memory.ShareableList([1,2,3],name="asaa")
b = shared_memory.ShareableList(name="asaa")
print(b)

a.shm.unlink()
a.shm.close()
b.shm.close()