# WithTimeKeeper
This library provides a convenient way to measure the execution time of code blocks using the with statement.
## Example
```python
import time
from withtimekeeper import WithTimeKeeper
from withtimekeeper import calculate_confidence_interval_time

timer = WithTimeKeeper()
for _ in range(3):
    
    with timer("task1"):
        time.sleep(0.01)
        
    with timer("task2"):
        with timer("task3"):
            time.sleep(0.03)
        with timer("task4"):
            time.sleep(0.04)
        time.sleep(0.02)
        
print(timer.get_dict())
#{'task1': [0.0100784230003228, 0.01007739299984678, 0.010076932999709243], 'task3': [0.03008607999981905, 0.03006290999974226, 0.030076089999965916], 'task4': [0.040077442999972845, 0.040076123000289954, 0.040083872999730374], 'task2': [0.09026030900031401, 0.09022346900019329, 0.09025836899991191]}
print(sum(timer["task1"]))
#0.030232748999878822
print(timer.each_total())
#{'task1': 0.030232748999878822, 'task3': 0.09022507999952722, 'task4': 0.12023743899999317, 'task2': 0.2707421470004192}
print(calculate_confidence_interval_time(timer["task2"]))
#{'lower_bound': 0.09019587639217828, 'upper_bound': 0.09029888827476786, 'mean': 0.09024738233347307, 'margin_of_error': 5.1505941294784504e-05}
```
