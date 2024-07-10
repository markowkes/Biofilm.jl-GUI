using Biofilm 
 
 #input parameters 
p = (
            # --------------------- #
            # Simulation Parameters #
            # --------------------- #
		 Title = 	 "emulate case 4",
        	 tFinal = 	 100,    #Simulation time [days]
        	 tol = 	 1e-4,   #Tolerance
        	 outPeriod = 	 1.0, # Time between outputs [days]

            # ---------------------- #
            # Particulate Parameters #
            # ---------------------- #

            XNames =["SOB", "SRB", "Dead Bacteria"],		# Particulate names
            Xto =   [1.0e-6, 1.0e-6, 0.0],		# Tank particulate concentration initial condition(s)
            Pbo =   [0.2/2, 0.2/2, 0.0],		# Biofilm particulates volume fraction initial condition(s) 
            rho =   [2.5e5, 2.5e5, 2.5e5],		# Particulate densities
            Kdet =  20000.0,		# Particulates detachment coefficient
            srcX =  [(S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   ],		# Source of particulates
            mu = [
			(S,X,Lf,t,z,p) ->0,  #SOB
			(S,X,Lf,t,z,p) ->0,  #SRB
			(S,X,Lf,t,z,p) ->0,  #Dead Bacteria
],

            # ----------------- #
            # Solute Parameters #
            # ----------------- #

            SNames =["Oxygen", "Sulfate", "Hydrogen Sulfide"],		# Solute names
            Sin =   [(t) -> 100
			   (t) -> 100
			   (t) -> 100],		# Solute inflow (can be function of time)
            Sto =   [8.6, 48.0, 0.0],		# Tank solute concentration initial condition(s)
            Sbo =   [8.6, 48.0, 1e-5],		# Biofilm solutes concentration initial condition(s)
            Yxs =   [0.058  0.0  0.09
			   0.0  0.058  -1.645
			   0.0  0.0  0.0],		# Biomass yield coefficient on solute   #this should come from the reaction menu
            Dt =    [1.51e-4, 8e-5, 1.21e-4],		# Aquious solute diffusion through tank fluid
            Db =    [6.8e-5, 4e-5, 6.04e-5],		# Effective solute diffusion through biofilm
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

            makePlots =false,
            savePlots=true,
)
	t,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
        biofilm_plot(sol,p) # Plot final results