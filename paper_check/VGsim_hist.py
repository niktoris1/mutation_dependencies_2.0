import random
import sys
import VGsim

number_of_sites = 1
populations_number = 2
number_of_susceptible_groups = 3
simulator = VGsim.Simulator(number_of_sites, populations_number, number_of_susceptible_groups,
                                seed=random.randint(0, sys.maxsize))

simulator.set_transmission_rate(0.25)
simulator.set_transmission_rate(0.4, haplotype="G")

mutation_rate = 0.003
substitution_weights = [1, 1, 1, 1]  # ATCG
simulator.set_mutation_rate(mutation_rate, substitution_weights)

simulator.set_recovery_rate(0.0)
simulator.set_sampling_rate(0.1)

simulator.set_susceptibility_type(0)  # default
simulator.set_susceptibility_type(1, haplotype="A")
simulator.set_susceptibility_type(1, haplotype="C")
simulator.set_susceptibility_type(1, haplotype="T")
simulator.set_susceptibility_type(2, haplotype="G")

simulator.set_susceptibility(1.0, susceptibility_type=0)  # no resist
simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype=0)  # resist
simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype=1)  # resist
simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype=2)  # resist
simulator.set_susceptibility(0.2, susceptibility_type=1, haplotype=3)  # partial resist
simulator.set_susceptibility(0.0, susceptibility_type=2)  # resist


simulator.set_immunity_transition(0.01, source=1, target=0)
simulator.set_immunity_transition(0.01, source=2, target=0)

simulator.set_population_size(100000, population=0)
simulator.set_population_size(100000, population=1)
simulator.set_migration_probability(0.01)

simulator.simulate(iterations=1000000)
simulator.genealogy()

tree, times = simulator.get_tree()

counter = 0
for el in times:
    if el < 1e-6:
        counter += 1

print("counter", counter)
