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

            XNames =["", ""],		# Particulate names
            Xto =   [0.0, 0.0],		# Tank particulate concentration initial condition(s)
            Pbo =   [0.0, 0.0],		# Biofilm particulates volume fraction initial condition(s) 
            rho =   [0.0, 0.0],		# Particulate densities
            Kdet =  20000.0,		# Particulates detachment coefficient
            srcX =  [(S,X,Lf,t,z,p) -> 0.0
			(S,X,Lf,t,z,p) -> 0.0
			],		# Source of particulates
            mu = [
			(S,X,Lf,t,z,p) ->0,  #
			(S,X,Lf,t,z,p) ->0,  #
],

            # ----------------- #
            # Solute Parameters #
            # ----------------- #

            SNames =["", ""],		# Solute names
            Sin =   [(t) -> 100
			   (t) -> 100
			],		# Solute inflow (can be function of time)
            Sto =   [0.0, 0.0],		# Tank solute concentration initial condition(s)
            Sbo =   [0.0, 0.0],		# Biofilm solutes concentration initial condition(s)
            Yxs =   [0.0  0.0
			   0.0  0.0
				],		# Biomass yield coefficient on solute   #this should come from the reaction menu
            Dt =    [0.0, 0.0],		# Aquious solute diffusion through tank fluid
            Db =    [0.0, 0.0],		# Effective solute diffusion through biofilm
            srcS =  [(S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			],     # Source of solutes

            # --------------- #
            # Tank Parameters #
            # --------------- #
		 V =	0,	#Volume of tank[m^3]
        	 A =	0,	#Surface area of biofilm [m^2]
        	 Q =	0,	#Flowrate through tank [m^3/d]
		# ------------------ #
            # Biofilm Parameters #
            # ------------------ #
		Nz = 0,          # Number of grid points in biofilm
            Lfo = 0,     # Biofilm initial thickness [m]
            LL = 0,      # Boundary layer thickness [m]
)
		 t,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
        biofilm_plot(sol,p) # Plot final results