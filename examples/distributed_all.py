"""
Example how to run evaluation on multiple machines with dask
"""

import pickle as pc

from joblib import parallel_backend
from skopt import gp_minimize, dummy_minimize, forest_minimize

from bbob.evaluation import parallel_evaluate, plot_results, calculate_metrics

run_with_dask = False
dask_scheduler = "54.237.243.247:8786"  # example scheduler address


def run():
    r = parallel_evaluate(
        solvers=[gp_minimize, forest_minimize, dummy_minimize, ],
        task_subset=None,  # automatically selects all tasks
        n_reps=128,
        eval_kwargs={'n_calls': 64},
        joblib_kwargs={'n_jobs': -1, 'verbose': 10})
    # it is a good idea to cache results
    pc.dump(r, open('r.bin', 'wb'))

if run_with_dask:
    with parallel_backend('dask.distributed', scheduler_host=dask_scheduler):
        run()
else:
    run()

# load cached results
r = pc.load(open('r.bin', 'rb'))
p = calculate_metrics(r)  # returns panda's dataframe
p.to_csv('data.csv')
plot_results(r)