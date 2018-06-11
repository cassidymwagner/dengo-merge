/*

The generalized rate data type holders.

*/

#include "omp.h"
/* stdlib, hdf5, local includes */

#include "time.h"
#include "sys/time.h"
#include "stdlib.h"
#include "math.h"
#include "hdf5.h"
#include "hdf5_hl.h"
#include "stdio.h"
#include "string.h"

/* header files for CVODES/SUNDIALS */
#include <cvode/cvode.h>               /* prototypes for CVODE fcts., consts.  */
#include <nvector/nvector_serial.h>    /* access to serial N_Vector            */
#include <sunmatrix/sunmatrix_dense.h> /* access to dense SUNMatrix            */
#include <sunlinsol/sunlinsol_dense.h> /* access to dense SUNLinearSolver      */
#include <cvode/cvode_direct.h>        /* access to CVDls interface            */
#include <sundials/sundials_types.h>   /* defs. of realtype, sunindextype      */
/* User-defined vector and matrix accessor macros: Ith, IJth */

/* These macros are defined in order to write code which exactly matches
   the mathematical problem description given above.

   Ith(v,i) references the ith component of the vector v, where i is in
   the range [1..NEQ] and NEQ is defined below. The Ith macro is defined
   using the N_VIth macro in nvector.h. N_VIth numbers the components of
   a vector starting from 0.

   IJth(A,i,j) references the (i,j)th element of the dense matrix A, where
   i and j are in the range [1..NEQ]. The IJth macro is defined using the
   DENSE_ELEM macro in dense.h. DENSE_ELEM numbers rows and columns of a
   dense matrix starting from 0. */

#define Ith(v,i)    NV_Ith_S(v,i-1)       /* Ith numbers components 1..NEQ */
#define IJth(A,i,j) SM_ELEMENT_D(A,i-1,j-1) /* IJth numbers rows,cols 1..NEQ */



#define MAX_NCELLS 1
#define NSPECIES 10
#define DMAX(A,B) ((A) > (B) ? (A) : (B))
#define DMIN(A,B) ((A) < (B) ? (A) : (B))

 

int cvdls_9species_main(int argc, char **argv);



typedef struct cvdls_9species_data {
    /* All of the network bins will be the same width */
    double dbin;
    double idbin;
    double bounds[2];
    int nbins;

    /* These will be for bins in redshift space */
    double d_zbin;
    double id_zbin;
    double z_bounds[2];
    int n_zbins;

    /* For storing and passing around
       redshift information */
    double current_z;
    double zdef;
    double dz;

    double Ts[MAX_NCELLS];
    double Tdef[MAX_NCELLS]; /* t1, t2, tdef */
    double dT[MAX_NCELLS]; /* t1, t2, tdef */
    double logTs[MAX_NCELLS];
    double invTs[MAX_NCELLS];
    double dTs_ge[MAX_NCELLS];

    /* Now we do all of our cooling and chemical tables */
    double r_k01[1024];
    double rs_k01[MAX_NCELLS];
    double drs_k01[MAX_NCELLS];
    
    double r_k02[1024];
    double rs_k02[MAX_NCELLS];
    double drs_k02[MAX_NCELLS];
    
    double r_k03[1024];
    double rs_k03[MAX_NCELLS];
    double drs_k03[MAX_NCELLS];
    
    double r_k04[1024];
    double rs_k04[MAX_NCELLS];
    double drs_k04[MAX_NCELLS];
    
    double r_k05[1024];
    double rs_k05[MAX_NCELLS];
    double drs_k05[MAX_NCELLS];
    
    double r_k06[1024];
    double rs_k06[MAX_NCELLS];
    double drs_k06[MAX_NCELLS];
    
    double r_k07[1024];
    double rs_k07[MAX_NCELLS];
    double drs_k07[MAX_NCELLS];
    
    double r_k08[1024];
    double rs_k08[MAX_NCELLS];
    double drs_k08[MAX_NCELLS];
    
    double r_k09[1024];
    double rs_k09[MAX_NCELLS];
    double drs_k09[MAX_NCELLS];
    
    double r_k10[1024];
    double rs_k10[MAX_NCELLS];
    double drs_k10[MAX_NCELLS];
    
    double r_k11[1024];
    double rs_k11[MAX_NCELLS];
    double drs_k11[MAX_NCELLS];
    
    double r_k12[1024];
    double rs_k12[MAX_NCELLS];
    double drs_k12[MAX_NCELLS];
    
    double r_k13[1024];
    double rs_k13[MAX_NCELLS];
    double drs_k13[MAX_NCELLS];
    
    double r_k14[1024];
    double rs_k14[MAX_NCELLS];
    double drs_k14[MAX_NCELLS];
    
    double r_k15[1024];
    double rs_k15[MAX_NCELLS];
    double drs_k15[MAX_NCELLS];
    
    double r_k16[1024];
    double rs_k16[MAX_NCELLS];
    double drs_k16[MAX_NCELLS];
    
    double r_k17[1024];
    double rs_k17[MAX_NCELLS];
    double drs_k17[MAX_NCELLS];
    
    double r_k18[1024];
    double rs_k18[MAX_NCELLS];
    double drs_k18[MAX_NCELLS];
    
    double r_k19[1024];
    double rs_k19[MAX_NCELLS];
    double drs_k19[MAX_NCELLS];
    
    double r_k21[1024];
    double rs_k21[MAX_NCELLS];
    double drs_k21[MAX_NCELLS];
    
    double r_k22[1024];
    double rs_k22[MAX_NCELLS];
    double drs_k22[MAX_NCELLS];
    
    int bin_id[MAX_NCELLS];
    int ncells;
    double g_gammaH2_1[1024];
    double g_dgammaH2_1_dT[1024];


    double gammaH2_1[MAX_NCELLS];
    double dgammaH2_1_dT[MAX_NCELLS];
    
    double g_gammaH2_2[1024];
    double g_dgammaH2_2_dT[1024];


    double gammaH2_2[MAX_NCELLS];
    double dgammaH2_2_dT[MAX_NCELLS];
    

    double scale[10];
    double inv_scale[10];
} cvdls_9species_data;

cvdls_9species_data *cvdls_9species_setup_data(int *, char***);
void cvdls_9species_read_rate_tables(cvdls_9species_data*);
void cvdls_9species_read_cooling_tables(cvdls_9species_data*);
void cvdls_9species_read_gamma(cvdls_9species_data*);
void cvdls_9species_interpolate_gamma(cvdls_9species_data*, int );

double dengo_evolve_cvdls_9species (double dtf, double &dt, double z,
                                     double *input, double *rtol,
                                     double *atol, long long dims,
                                     cvdls_9species_data *data);
 


/* Declare ctype RHS and Jacobian */
typedef int(*rhs_f)( realtype, N_Vector , N_Vector , void * );
typedef int(*jac_f)( realtype, N_Vector  , N_Vector , SUNMatrix , void *, N_Vector, N_Vector, N_Vector);




int cvodes_main_solver( rhs_f f, jac_f Jac, 
                 double *input , double *rtol, double *atol, int nchem, cvdls_9species_data *data, double *dt_now);



int calculate_jacobian_cvdls_9species( realtype t,
               N_Vector y, N_Vector fy, SUNMatrix J, void *user_data,
               N_Vector tmp1, N_Vector tmp2, N_Vector tmp3);

int calculate_rhs_cvdls_9species(realtype t, N_Vector y, N_Vector ydot, void *user_data);
void ensure_electron_consistency(double *input, int nstrip, int nchem);
void temperature_from_mass_density(double *input, int nstrip, int nchem, 
                                   double *strip_temperature);



