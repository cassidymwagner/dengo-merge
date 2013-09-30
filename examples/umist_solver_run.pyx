cimport numpy as np
import numpy as np

cdef extern from "alloca.h":
    void *alloca(int)

DEF NSPECIES = 1
DEF MAX_NCELLS = 1024

cdef extern from "umist_solver.h":
    ctypedef struct umist_data:
        double dbin
        double idbin
        double bounds[2]
        int nbins

        double Ts[MAX_NCELLS]
        double Tdef[MAX_NCELLS]
        double dT[MAX_NCELLS]
        double logTs[MAX_NCELLS]
        double dTs_ge[MAX_NCELLS]
        int bin_id[MAX_NCELLS]
        int ncells

    ctypedef int(*rhs_f)(double *, double *, int, int, void *)
    ctypedef int(*jac_f)(double *, double *, int, int, void *)

    int umist_main(int argc, char **argv)
    umist_data *umist_setup_data()
    void umist_read_rate_tables(umist_data*)
    void umist_read_cooling_tables(umist_data*)
    double dengo_evolve_umist (double dtf, double &dt, double *input,
                double *rtol, double *atol, int dims,
                umist_data *data)
    int BE_chem_solve(rhs_f f, jac_f J,
		    double *u, double dt, double *rtol, 
                    double *atol, int nstrip, int nchem, 
		    double *scaling, void *sdata)
    int calculate_jacobian_umist(double *input, double *Joutput,
            int nstrip, int nchem, void *sdata)
    int calculate_rhs_umist(double *input, double *rhs, int nstrip,
                      int nchem, void *sdata)

def main_run_umist():
    umist_main(0, NULL)

def run_umist(ics, double tf, int niter = 10000, int intermediate = 1):
    cdef np.ndarray[np.float64_t, ndim=1] ge_arr = ics["ge"]
    # All of the intermediate variables get declared, but not necessarily assigned
    cdef np.ndarray[np.float64_t, ndim=2] ge_int
    cdef np.ndarray[np.uint8_t, ndim=1] result_int
    cdef np.ndarray[np.float64_t, ndim=2] temp_int
    cdef np.ndarray[np.float64_t, ndim=1] t_int
    cdef np.ndarray[np.float64_t, ndim=1] dt_int

    cdef int i, j, k, iter
    cdef int N = ge_arr.shape[0]
    cdef int NTOT = NSPECIES * N
    cdef double *input = <double *> alloca(NTOT * sizeof(double))
    cdef double *prev = <double *> alloca(NTOT * sizeof(double))
    cdef double *atol = <double *> alloca(NTOT * sizeof(double))
    cdef double *rtol = <double *> alloca(NTOT * sizeof(double))
    cdef double *scale = <double *> alloca(NTOT * sizeof(double))
    cdef double v

    if intermediate == 1:
        ge_int = np.zeros((N, niter), "float64")
        temp_int = np.zeros((N, niter), "float64")
        result_int = np.zeros(niter, "uint8")
        t_int = np.zeros(niter, "float64")
        dt_int = np.zeros(niter, "float64")

    j = 0
    for i in range(N):
        input[j] = prev[j] = ge_arr[i] / 1.0
        atol[j] = input[j] * 1e-11
        rtol[j] = 1e-11
        scale[j] = 1.0
        j += 1

    cdef umist_data *data = umist_setup_data()
    cdef rhs_f f = calculate_rhs_umist
    cdef jac_f jf = calculate_jacobian_umist

    cdef double dt = tf / 1e5
    cdef double ttot = 0.0
    cdef int status
    # Now we manually evolve
    #ttot = dengo_evolve_umist(tf, dt, input, rtol, atol, N, data)
    for iter in range(niter):
        status = BE_chem_solve(f, jf, input, dt, rtol, atol, N, NSPECIES, scale,
                               <void *> data)
        if intermediate == 1:
            j = 0
            for i in range(N):
                ge_int[i, iter] = input[j]
                j += 1
                temp_int[i, iter] = data.Ts[i]
            if status == 0:
                result_int[iter] = 1
            elif status == 1:
                result_int[iter] = 0
            t_int[iter] = ttot
            dt_int[iter] = dt
        if status == 0:
            if iter % 1000 == 0:
                print "Successful iteration[% 5i]: (%0.3e) %0.3e / %0.3e" % (
                    iter, dt, ttot, tf)
            copy_array(input, prev, NTOT)
            ttot += dt
            dt *= 1.1
            if tf - ttot < dt:
                dt = tf- ttot
        elif status == 1:
            dt /= 2.0
            copy_array(prev, input, NTOT)
            if dt < 1e-30 * tf:
                print "dt too small (%0.3e / %0.3e) so breaking" % (dt, tf)
                break
            continue
        if ttot >= tf: break

    print "End in %s iterations: %0.5e / %0.5e (%0.5e)" % (iter + 1, ttot, tf, tf - ttot)

    rv, rv_t = {}, {}
    ge_arr = rv["ge"] = np.zeros(N, "float64")
    if intermediate:
        rv_t["ge"] = ge_int[:niter]
        rv_t["successful"] = result_int.astype("bool")
        rv_t['T'] = temp_int
        rv_t['t'] = t_int
        rv_t['dt'] = dt_int

    j = 0
    for i in range(N):
        ge_arr[i] = input[j] * 1.0
        j += 1
    return rv, rv_t

cdef copy_array(double *input, double *output, int N):
    cdef int i
    for i in range(N):
        output[i] = input[i]