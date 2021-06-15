from multiprocessing import shared_memory

a = shared_memory.ShareableList(["sdsdfas","asdasd","aa23"],name="aaa")
print(a[1])

b = shared_memory.ShareableList(name="aaa")
print(b)

a.shm.close()
b.shm.close()
a.shm.unlink()


