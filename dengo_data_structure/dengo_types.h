/***********************************************************************
/
/ Grackle variable types
/
/
/ Copyright (c) 2013, Enzo/Grackle Development Team.
/
/ Distributed under the terms of the Enzo Public Licence.
/
/ The full license is in the file LICENSE, distributed with this 
/ software.
************************************************************************/

/***********************************************************************
/  
/ VARIABLE TYPES
/
************************************************************************/

typedef struct
{

  long int ncells;
    
  // This should be updated dynamically 
  // with dengo
  double *density;
  double *H2_1_density;
  
  double *H2_2_density;
  
  double *H_1_density;
  
  double *H_2_density;
  
  double *H_m0_density;
  
  double *He_1_density;
  
  double *He_2_density;
  
  double *He_3_density;
  
  double *de_density;
  
  double *ge_density;
  

} dengo_field_data;

typedef struct
{

  int comoving_coordinates;
  double density_units;
  double length_units;
  double time_units;
  double velocity_units;
  double a_units;
  double a_value;

} code_units;