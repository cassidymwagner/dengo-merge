import numpy
import pyximport
pyximport.install(setup_args={"include_dirs":numpy.get_include()},
                  reload_support=True)

import sundials_time_solver_run
sundials_time_solver_run.main_run_sundials_time()