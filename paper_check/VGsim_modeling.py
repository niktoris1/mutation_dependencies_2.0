import VGsim

number_of_sites = 1
populations_number = 2
number_of_susceptible_groups = 1
simulator = VGsim.Simulator(number_of_sites, populations_number, number_of_susceptible_groups, seed=1234)

simulator.set_transmission_rate(0.25)
simulator.set_recovery_rate(0.099)
simulator.set_sampling_rate(0.001)
mutation_rate=0.005
substitution_weights=[1,1,1,1] #ATCG
simulator.set_mutation_rate(mutation_rate, substitution_weights)
#simulator.set_susceptibility_type(0)
#simulator.set_susceptibility(1, susceptibility_type=0) # no resist
simulator.set_susceptibility(1)
simulator.set_population_size(100000, population=0)
simulator.set_population_size(100000, population=1)
simulator.set_migration_probability(0.1)

simulator.simulate(1000000, time=200)


simulator.add_plot_infectious(population=0, haplotype=0, step_num=100)
simulator.add_plot_infectious(population=1, haplotype=0, step_num=100)

simulator.add_plot_susceptible(population=0, susceptibility_type=0, step_num=100)
simulator.add_plot_susceptible(population=1, susceptibility_type=0, step_num=100)
simulator.add_title(name="Plot")
simulator.add_legend()
simulator.plot()

simulator.genealogy()

#file_name = "/Users/LAB-SCG-125/Documents/data_from_simulation/example"
file_name = "example"

simulator.output_newick(file_name)
simulator.output_mutations(file_name)
simulator.output_migrations(file_name)

simulator.print_basic_parameters()
simulator.print_immunity_model()
simulator.print_populations()