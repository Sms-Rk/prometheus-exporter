from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from nvitop import Device, GpuProcess, NA, colored
import time


class GpuSmCollector(object):
    def __init__(self):
        pass

    def collect(self):
        gauge = GaugeMetricFamily('my_gauge_sm', 'Help text', labels=['pid'])
        devices = Device.all()
        for device in devices:
            processes = device.processes()
            
            if len(processes) > 0:
                processes = GpuProcess.take_snapshots(processes.values(), failsafe=True)
                #processes.sort(key=lambda process: (process.username, process.pid))
                for snapshot in processes:
                    gauge.add_metric([snapshot.command], snapshot.gpu_sm_utilization)
                    yield gauge
            else:
                print(colored('  - No Running Processes', attrs=('bold',)))

if __name__ == "__main__":
    start_http_server(9001)
    REGISTRY.register(GpuSmCollector())
    while True: 
        # period between collection
        time.sleep(1)
