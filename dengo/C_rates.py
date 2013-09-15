# Gets rates for all C formation reactions in the UMIST database

from reaction_classes import Species, species_registry
from umist_rates import umist_rates

atomicSymbol = 'C'
atomicNumber = -1
atomicWeight = 12
i=-1
# make species s with these params

speciesName = "%s" %(atomicSymbol)
    # Check if the species already exists
    # in the species registry, if it does
    # we don't want to create it again
if (speciesName in species_registry) == False:
    s = Species(speciesName, atomicNumber, atomicWeight, i)
else:
    s = species_registry[speciesName]


umist_rates(s)