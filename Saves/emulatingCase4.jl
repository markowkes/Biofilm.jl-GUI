using Biofilm 
 
 #input parameters 
p = (
            # --------------------- #
            # Simulation Parameters #
            # --------------------- #
		 Title = 	 "simu",
        	 tFinal = 	 100,    #Simulation time [days]
        	 tol = 	 1e-4,   #Tolerance
        	 outPeriod = 	 1.0, # Time between outputs [days]

            # ---------------------- #
            # Particulate Parameters #
            # ---------------------- #

            XNames =["SOB", "SRE"],		# Particulate names
            Xto =   [1.0e-6, 1.0e-6],		# Tank particulate concentration initial condition(s)
            Pbo =   [0.2/2, 0.2/2],		# Biofilm particulates volume fraction initial condition(s) 
            rho =   [2.4e5, 2.5e5],		# Particulate densities
            Kdet =  20000.0,		# Particulates detachment coefficient
            srcX =  [(S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   ],		# Source of particulates
            mu = [
			(S,X,Lf,t,z,p) ->0,  #SOB
			(S,X,Lf,t,z,p) ->0,  #SOB
],

            # ----------------- #
            # Solute Parameters #
            # ----------------- #

            SNames =["Oxygen", "Sulfate", "Hydrogen Sulfide"],		# Solute names
            Sin =   [(t) -> 100
			   (t) -> 100
			   (t) -> 10],		# Solute inflow (can be function of time)
            Sto =   [8.6, 48.0, 0.0],		# Tank solute concentration initial condition(s)
            Sbo =   [8.6, 48.0, 1e-5],		# Biofilm solutes concentration initial condition(s)
            Yxs =   [0.058  0.0  0.058
			   0.0  0.058  -0.05],		# Biomass yield coefficient on solute   #this should come from the reaction menu
            Dt =    [1.51e-4, 8e-5, 1.21e-4],		# Aquious solute diffusion through tank fluid
            Db =    [6.8e-5, 6.8e-5, 6.8e-5],		# Effective solute diffusion through biofilm
            srcS =  [(S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   ],     # Source of solutes

            # --------------- #
            # Tank Parameters #
            # --------------- #
		 V =	0.1,	#Volume of tank[m^3]
        	 A =	1,	#Surface area of biofilm [m^2]
        	 Q =	10,	#Flowrate through tank [m^3/d]
		# ------------------ #
            # Biofilm Parameters #
            # ------------------ #
		Nz = 40,          # Number of grid points in biofilm
            Lfo = 5.0e-6,     # Biofilm initial thickness [m]
            LL = 2.0e-4,      # Boundary layer thickness [m]
)
	t,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
        biofilm_plot(sol,p) # Plot final results