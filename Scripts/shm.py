from multiprocessing import shared_memory

shm_a = shared_memory.SharedMemory(name="aaa",create=True, size=10)
buffer = shm_a.buf
#buffer = "asasdasd"

buffer[:4] = bytearray([22, 33, 44, 55])
buffer[4] = 100

shm_b = shared_memory.SharedMemory("aaa")
#aa = bytes(shm_b.buf)
print(shm_b.buf[1])
shm_a.close()
shm_b.close()
shm_a.unlink()


