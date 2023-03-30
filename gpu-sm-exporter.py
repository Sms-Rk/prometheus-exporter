from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server, Gauge, Enum
import time
from nvitop import Device, GpuProcess, NA, colored
import os


class GpuSmCollector(object):
    def __init__(self, sm_target_port=9001, polling_interval_seconds=50):
        self.sm_target_port = sm_target_port
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect

#        self.sm = GaugeMetricFamily('gpu_process', 'Help text', labels=['pid'])


    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.collect()
            time.sleep(self.polling_interval_seconds)

    def collect(self):
            sm = GaugeMetricFamily('gpu_process', 'Help text', labels=['process'])
            devices = Device.all()
            for device in devices:
                processes = device.processes()
                if len(processes) > 0:
                    processes = GpuProcess.take_snapshots(processes.values(), failsafe=True)
                    #processes.sort(key=lambda process: (process.username, process.pid))
                    for snapshot in processes:
                        pid = str(snapshot.pid)
                        sm.add_metric("gpu#="+str(device.index)+"pid#="+pid], snapshot.gpu_sm_utilization)
                else:
                    print(colored('  - No Running Processes', attrs=('bold',)))
            return [sm]


def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "50"))
#    app_port = int(os.getenv("APP_PORT", "80"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9001"))

    sm_metrics = GpuSmCollector(
        sm_target_port=exporter_port,
        polling_interval_seconds=polling_interval_seconds
    )
    REGISTRY.register(sm_metrics)
    start_http_server(exporter_port)
    sm_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
