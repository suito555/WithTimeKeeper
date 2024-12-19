from contextlib import contextmanager
from math import sqrt
import statistics
from time import perf_counter

def _get_t_critical(df):
    if df <= 0:
        raise ValueError("Degrees of freedom must be positive.")
    
    T_TABLE = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
        6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
        16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
        21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
        26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042
    }
    if df > 30: #t-distribution approximates normal distribution
        return 1.96  # z-score for 95% confidence
    else:
        return T_TABLE[df]

def calculate_confidence_interval_time(times: list): #only supports 95% confidence level
    data_size = len(times)
    if data_size < 2:
        raise ValueError("At least two data points are required.")
    
    mean = statistics.mean(times)
    sample_std = statistics.stdev(times)
    df = data_size - 1
    
    t_critical = _get_t_critical(df)

    standard_error = sample_std / sqrt(data_size)
    margin_of_error = t_critical * standard_error
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error

    confidence_interval_data = {'lower_bound': lower_bound, 'upper_bound': upper_bound, 'mean': mean, 'margin_of_error':margin_of_error}
    return confidence_interval_data

class WithTimeKeeper:
    def __init__(self):
        self.elapsed_times_dict = {}

    @contextmanager
    def __call__(self, task_name):
        start_time = perf_counter()
        yield
        elapsed_time = perf_counter() - start_time
        self.elapsed_times_dict.setdefault(task_name, []).append(elapsed_time)

    def __str__(self):
        return str(self.elapsed_times_dict)
        
    def __len__(self):
        return len(self.elapsed_times_dict)

    def __getitem__(self, task_name):
        return self.elapsed_times_dict[task_name]

    def get_dict(self):
        return self.elapsed_times_dict

    def each_total(self):
        return {task_name: sum(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_mean(self):
        return {task_name: statistics.mean(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_median(self):
        return {task_name: statistics.median(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_median_low(self):
        return {task_name: statistics.median_low(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_median_high(self):
        return {task_name: statistics.median_high(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_mode(self): #only one mode
        return {task_name: statistics.mode(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_multimode(self): #multi mode
        return {task_name: statistics.multimode(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_pvariance(self):
        return {task_name: statistics.pvariance(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_variance(self):
        return {task_name: statistics.variance(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_pstdev(self):
        return {task_name: statistics.pstdev(times) for task_name, times in self.elapsed_times_dict.items()}

    def each_stdev(self):
        return {task_name: statistics.stdev(times) for task_name, times in self.elapsed_times_dict.items()}
    
    def each_confidence_interval_time(self):
        return {task_name: calculate_confidence_interval_time(times) for task_name, times in self.elapsed_times_dict.items()}