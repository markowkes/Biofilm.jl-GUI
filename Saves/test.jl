using Biofilm 
 
 #input parameters 
 mumax = 20; KM = 3; 
p = (
        # --------------------- #
        # Simulation Parameters #
        # --------------------- #
		 Title = 	 "tit",
    	 tFinal = 	 1,    #Simulation time [days]
    	 tol = 	 1e-4,   #Tolerance
    	 outPeriod = 	 0.1, # Time between outputs [days]

        # ---------------------- #
        # Particulate Parameters #
        # ---------------------- #

        XNames =["par"],		# Particulate names
        Xto =   [1],		# Tank particulate concentration initial condition(s)
        Pbo =   [1],		# Biofilm particulates volume fraction initial condition(s) 
        rho =   [1],		# Particulate densities
        Kdet =  20000.0,		# Particulates detachment coefficient
        srcX =  [(S,X,Lf,t,z,p) -> 0.0],		# Source of particulates
        mu = [(S,X,Lf,t,z,p) -> (mumax * S[1]) ./ (KM .+ S[1])],

        # ----------------- #
        # Solute Parameters #
        # ----------------- #

        SNames =["sol"],		# Solute names
        Sin =   [(t) -> 100],		# Solute inflow (can be function of time)
        Sto =   [1],		# Tank solute concentration initial condition(s)
        Sbo =   [1],		# Biofilm solutes concentration initial condition(s)
        Yxs =   [.2],		# Biomass yield coefficient on solute   #this should come from the reaction menu
        Dt =    [1],		# Aquious solute diffusion through tank fluid
        Db =    [1],		# Effective solute diffusion through biofilm
        srcS =  [(S,X,Lf,t,z,p) -> 0.0],     # Source of solutes

        # --------------- #
        # Tank Parameters #
        # --------------- #
		 V =	1,	#Volume of tank[m^3]
    	 A =	10,	#Surface area of biofilm [m^2]
    	 Q =	10,	#Flowrate through tank [m^3/d]
		# ------------------ #
        # Biofilm Parameters #
        # ------------------ #
		Nz = 10,          # Number of grid points in biofilm
        Lfo = .1,     # Biofilm initial thickness [m]
        LL = .01,      # Boundary layer thickness [m]
	)

    

    t,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
    biofilm_plot(sol,p) # Plot final results