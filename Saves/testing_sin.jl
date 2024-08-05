using Biofilm 
 
 #input parameters 
p = (
            # --------------------- #
            # Simulation Parameters #
            # --------------------- #
		 Title = 	 "",
        	 tFinal = 	 1,    #Simulation time [days]
        	 tol = 	 1e-4,   #Tolerance
        	 outPeriod = 	 0.1, # Time between outputs [days]

            # ---------------------- #
            # Particulate Parameters #
            # ---------------------- #

            XNames = [""],		# Particulate names
            Xto =   [0.0],		# Tank particulate concentration initial condition(s)
            Pbo =   [0.0],		# Biofilm particulates volume fraction initial condition(s) 
            rho =   [0.0],		# Particulate densities
            Kdet =  20000.0,		# Particulates detachment coefficient
            srcX =  [(S,X,Lf,t,z,p) -> 0.0],		# Source of particulates
            mu = [(S,X,Lf,t,z,p) ->0.0,  #
		],

       	#===Kinetics===#
       	#, 0.0
		#, none, 0, 0
		#, none, 0, 1
		#, none, 0, 2
       	#===End_Kinetics===#

            # ----------------- #
            # Solute Parameters #
            # ----------------- #

            SNames =["", "", ""],	# Solute names
            Sin =   [(t) -> 0.0 + (2.0 * sin(t/1.0)),
			   (t) -> 0,
			   (t) -> 1.0 * (1 - heaviside( mod((t - 1.0), 1.0) - 0.5))],		# Solute inflow (can be function of time)
            Sto =   [0.0, 0.0, 0.0],		# Tank solute concentration initial condition(s)
            Sbo =   [0.0, 0.0, 0.0],		# Biofilm solutes concentration initial condition(s)
            Yxs =   [0.0  0.0  0.0],		# Biomass yield coefficient on solute   #this should come from the reaction menu
            Dt =    [0.0, 0.0, 0.0],		# Aquious solute diffusion through tank fluid
            Db =    [0.0, 0.0, 0.0],		# Effective solute diffusion through biofilm
            srcS =  [(S,X,Lf,t,z,p) -> 0.0,
			   (S,X,Lf,t,z,p) -> 0.0,
			   (S,X,Lf,t,z,p) -> 0.0],     # Source of solutes

		#===Sin===#
		#, sin, 2.0, 1.0, 0.0
		#, none
		#, periodic, 1.0, 1.0, 0.5, 1.0
		#===End_Sin===#

            # --------------- #
            # Tank Parameters #
            # --------------- #
		 V =	1,	#Volume of tank[m^3]
        	 A =	1,	#Surface area of biofilm [m^2]
        	 Q =	1,	#Flowrate through tank [m^3/d]

		# ------------------ #
            # Biofilm Parameters #
            # ------------------ #
		Nz = 40,          # Number of grid points in biofilm
            Lfo = 0.1,     # Biofilm initial thickness [m]
            LL = 10e-4,      # Boundary layer thickness [m]
		savePlots = true,
        	makePlots = true,)

		t,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
            biofilm_plot(sol,p) # Plot final results
            #biofilm_sol2csv(sol,p,filname)