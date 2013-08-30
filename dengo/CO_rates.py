# Gets rates for all CO formation reactions in the UMIST database

from reaction_class import Species, species_registry
import umist_rates

atomicSymbol = 'CO'
atomicNumber = -1
atomicWeight = 28

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