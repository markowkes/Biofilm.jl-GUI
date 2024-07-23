using Biofilm 
 
 #input parameters 
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

            XNames = ["p1", "p2", "p3"],		# Particulate names
            Xto =   [0.0, 0.0, 0.0],		# Tank particulate concentration initial condition(s)
            Pbo =   [0.0, 0.0, 0.0],		# Biofilm particulates volume fraction initial condition(s) 
            rho =   [0.0, 0.0, 0.0],		# Particulate densities
            Kdet =  20000.0,		# Particulates detachment coefficient
            srcX =  [(S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   ],		# Source of particulates
            mu = [
			(S,X,Lf,t,z,p) ->1 * ( S[0] / (1.1 + S[0]) ) * ( 1 / (1 + (S[1] / 1.2)) ),  #p1
			(S,X,Lf,t,z,p) ->2 * ( S[1] / (2.1 + S[1]) ) * ( 1 / (1 + (S[2] / 2.2)) ),  #p2
			(S,X,Lf,t,z,p) ->3 * ( 1 / (1 + (S[0] / 3.1)) ) * ( S[2] / (3.2 + S[2]) ),  #p3
     #===Kinetics===#
       #, 1, 2, 3
       #, monod, 0, 0, 1.1
       #, inhibition, 0, 1, 1.2
       #, none, 0, 2
       #, none, 1, 0
       #, monod, 1, 1, 2.1
       #, inhibition, 1, 2, 2.2
       #, inhibition, 2, 0, 3.1
       #, none, 2, 1
       #, monod, 2, 2, 3.2
        #===End_Kinetics===#

],

            # ----------------- #
            # Solute Parameters #
            # ----------------- #

            SNames =["s1", "s2", "s3"],		# Solute names
            Sin =   [(t) -> 100
			   (t) -> 100
			   (t) -> 100],		# Solute inflow (can be function of time)
            Sto =   [0.0, 0.0, 0.0],		# Tank solute concentration initial condition(s)
            Sbo =   [0.0, 0.0, 0.0],		# Biofilm solutes concentration initial condition(s)
            Yxs =   [1.1  1.2  1.3
			   2.1  2.2  2.3
			   3.1  3.2  3.3],		# Biomass yield coefficient on solute   #this should come from the reaction menu
            Dt =    [0.0, 0.0, 0.0],		# Aquious solute diffusion through tank fluid
            Db =    [0.0, 0.0, 0.0],		# Effective solute diffusion through biofilm
            srcS =  [(S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   (S,X,Lf,t,z,p) -> 0.0
			   ],     # Source of solutes

            # --------------- #
            # Tank Parameters #
            # --------------- #
		 V =	10,	#Volume of tank[m^3]
        	 A =	10,	#Surface area of biofilm [m^2]
        	 Q =	10,	#Flowrate through tank [m^3/d]
		# ------------------ #
            # Biofilm Parameters #
            # ------------------ #
		Nz = 10,          # Number of grid points in biofilm
            Lfo = 0.1,     # Biofilm initial thickness [m]
            LL = 0.1,      # Boundary layer thickness [m]
savePlots = true,
                               makePlots = true,)
	t,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
        biofilm_plot(sol,p) # Plot final results
        #biofilm_sol2csv(sol,p,filname)