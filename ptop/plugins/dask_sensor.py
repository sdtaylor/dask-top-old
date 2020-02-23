from dask.distributed import Client
from ptop.core import Plugin

class DaskSensor(Plugin):
    def __init__(self, dask_address, **kwargs):
        super(DaskSensor, self).__init__(**kwargs)
        self.client = Client(address = dask_address)
        
        self.currentValue = {'Memory' :{'total_memory':0,
                                        'used_memory':0},
                             'CPU'    :{'cpu_usage':0},
                             'Cluster':{'n_workers':0,
                                        'total_threads':0}}
    
    def update(self):
        self.worker_info = self.client.scheduler_info()['workers']
        self.currentValue['Memory']['total_memory'] = round(self.available_memory() / (1024**2),2)
        self.currentValue['Memory']['used_memory']  = round(self.used_memory() / (1024**2),2)
        self.currentValue['CPU']['cpu_usage'] = self.cpu_usage()
        self.currentValue['Cluster']['n_workers'] = self.num_workers()
        self.currentValue['Cluster']['total_threads'] = self.num_workers()
    
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
    
    def cpu_usage(self):
        usages = []
        for w, info in self.worker_info.items():
            usages.append(info['metrics']['cpu'])
        if len(usages)>0:
            return sum(usages) / len(usages)
        else:
            return 0