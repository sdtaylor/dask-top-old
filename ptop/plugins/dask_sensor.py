from time import time
from dask.distributed import Client
from distributed.utils import key_split

from ptop.core import Plugin

class DaskSensor(Plugin):
    def __init__(self, dask_address, **kwargs):
        super(DaskSensor, self).__init__(**kwargs)
        self.client = Client(address = dask_address)
        
        self.currentValue = {'Memory' :{'total_memory':0,
                                        'used_memory':0},
                             'CPU'    :{'cpu_usage':0},
                             'Cluster':{'n_workers':0,
                                        'total_threads':0},
                             'Workers':[]}
    
    def close(self):
        self.client.close()
        
    def update(self):
        self.worker_info = self.client.scheduler_info()['workers']
        self.currentValue['Memory']['total_memory'] = round(self.available_memory() / (1024**2),2)
        self.currentValue['Memory']['used_memory']  = round(self.used_memory() / (1024**2),2)
        self.currentValue['Memory']['used_memory_percent']  = self.currentValue['Memory']['used_memory'] / self.currentValue['Memory']['total_memory']
        self.currentValue['CPU']['cpu_usage'] = self.cpu_usage()
        self.currentValue['Cluster']['n_workers'] = self.num_workers()
        self.currentValue['Cluster']['total_threads'] = self.num_workers()
        self.currentValue['Workers'] = self.get_worker_stats()
    
    def num_workers(self):
        return len(self.worker_info)
    
    def num_threads(self):
        threads = [worker['nthreads'] for _, worker in self.worker_info.items()]
        return(sum(threads))
    
    def available_memory(self):
        tots = 0
        for w, info in self.worker_info.items():
            tots += info['memory_limit']
        return tots
    
    def used_memory(self):
        tots = 0
        for w, info in self.worker_info.items():
            tots += info['metrics']['memory']
        return tots
    
    def get_worker_stats(self):
        worker_stats=[]
        for w, info in self.worker_info.items():
            stats = {'user':'filler',
                     'id' : 'filler',
                     'name' : 'filler',
                     'rawtime':1,
                     'time':1,
                     'command':'',
                     'cpu':1,
                     'memory':1,
                     'local_ports':'filler'}
            stats['address'] = w
            stats['nthreads'] = info['nthreads']
            stats['memory']   = round(info['metrics']['memory'] / (1024**2),2)
            stats['memory_limit'] = round(info['memory_limit'] / (1024**2), 2)
            stats['cpu']      = info['metrics']['cpu'] 
            stats['read']     =  round(info['metrics']['read_bytes'] / (1024**2), 2)
            stats['write']     = round(info['metrics']['write_bytes'] / (1024**2), 2)
            
            worker_stats.append(stats)
        return worker_stats
    
    def cpu_usage(self):
        usages = []
        for w, info in self.worker_info.items():
            usages.append(info['metrics']['cpu'])
        if len(usages)>0:
            return sum(usages) / len(usages)
        else:
            return 0

    def task_status(self):
        tasks = self.client.get_task_stream(start = time()-10)
        task_keys = [key_split(t['key']) for t in tasks]
        task_counts = dict()
        for k in task_keys:
            if k not in task_counts:
                task_counts[k]=0
            task_counts[k]+=1
        return task_counts
        