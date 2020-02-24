from dask.distributed import Client
import dask.array as da
from time import sleep

def sqrt(x):
    return x**0.5

if __name__ == '__main__':
    client = Client(n_workers=2, nthreads=1, memory_limit='512mb', dashboard_address=8787) 
    print(client.scheduler_info())
    sleep(3)
    while True:
        x = client.scatter(da.random.random((1000,1000), chunks=(50,50)))
        _ =client.submit(sqrt, x).result().compute() 
        sleep(3)
