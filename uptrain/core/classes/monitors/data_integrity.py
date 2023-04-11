import numpy as np

from uptrain.core.classes.monitors import AbstractMonitor
from uptrain.core.classes.measurables import MeasurableResolver
from uptrain.constants import Monitor

from scipy.stats import zscore

class DataIntegrity(AbstractMonitor):
    dashboard_name = "data_integrity"
    monitor_type = Monitor.DATA_INTEGRITY

    def base_init(self, fw, check):
        self.integrity_type = check["integrity_type"]
        self.threshold = check.get("threshold", None)
        self.count = 0
        self.num_issues = 0
            
    def base_check(self, inputs, outputs, gts=None, extra_args={}):
        signal_value = self.measurable.compute_and_log(
            inputs, outputs, gts=gts, extra=extra_args
        )
        outliers = None
        if self.integrity_type == "non_null":
            has_issue = signal_value == None
        elif self.integrity_type == "less_than":
            has_issue = signal_value > self.threshold
        elif self.integrity_type == "greater_than":
            has_issue = signal_value < self.threshold
        elif self.integrity_type == "z_score":
            has_issue = abs(zscore(signal_value)) > self.threshold
        else:
            raise NotImplementedError(
                "Data integrity check {} not implemented".format(self.integrity_type)
            )            
        self.count += len(signal_value)
        self.num_issues += np.sum(np.array(has_issue))
        plot_name = (
            self.measurable.col_name()
            + " "
            + self.integrity_type
            + " "
            + str(self.threshold)
        )

        self.log_handler.add_scalars(
            self.dashboard_name + "_" + plot_name,
            {"y_" + plot_name: 1 - self.num_issues / self.count},
            self.count,
            self.dashboard_name,
        )

        if outliers is not None:
            self.log_handler.add_scalars(
            self.dashboard_name + "_" + plot_name,
            {"y_" + plot_name+"_outliers": 1 - len(outliers) / len(signal_value)},
            self.count,
            self.dashboard_name,
            )
        
    def need_ground_truth(self):
        return False
