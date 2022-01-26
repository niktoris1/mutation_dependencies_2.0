import VGsim
number_of_sites = 2
populations_number = 1
number_of_susceptible_groups = 2
simulator = VGsim.Simulator(number_of_sites, populations_number, number_of_susceptible_groups, seed=1234)

simulator.set_transmission_rate(0.25)
simulator.set_recovery_rate(0.099)
simulator.set_sampling_rate(0.001)
mutation_rate=0.003
substitution_weights=[1,0,0,1] #ATCG
simulator.set_mutation_rate(mutation_rate, substitution_weights)
simulator.set_susceptibility_type(1)
simulator.set_susceptibility(0.1, susceptibility_type=1)
simulator.set_population_size(10000000, population=0)

simulator.simulate(1000000, time=110)

population = 0
haplotype = 0
simulator.add_plot_infectious(population, haplotype, step_num=100)

susceptibility_type = 0
simulator.add_plot_susceptible(population, susceptibility_type, step_num=100)
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