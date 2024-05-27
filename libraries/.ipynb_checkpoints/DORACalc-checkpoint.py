import numpy as np
from scipy.optimize import curve_fit

class DORA: #the transition state explorer
    def __init__(self, 
                descriptor_data, 
                distance_data, 
                dE_data,
                dE_A, dE_B,
                TdS_AB, TdS_A, TdS_B,
                y_cleave=0.01,
                k_start=10,
                max_iteration=1000,
                k_step=1,
                r_cleave = 0,
                D_name = "Descriptor",
                infinite_distance=10,
                tightness=0.01):
                
        # defining variables
        self.descriptor_data = descriptor_data
        self.distance_data = distance_data
        self.distance_data.append(infinite_distance)
        self.infinite_distance = infinite_distance
        self.dE_data = dE_data
        self.dE_data.append(dE_A + dE_B)

        self.TdS_AB = TdS_AB
        self.TdS_A = TdS_A 
        self.TdS_B = TdS_B 
        self.tightness = tightness
        self.min_descriptor = min(self.descriptor_data)
        self.max_descriptor = max(self.descriptor_data)
        self.gamma_cleave=y_cleave

        self.descriptor_fit=[]
        self.TdS_fit=[]
        self.dE_fit=[]
        self.dG_fit=[]
        self.r_cleave = r_cleave
        self.r_cleave_ext = False

        
        # in case of manual input for r_cleave 
        if self.r_cleave > 0:
            self.r_cleave_ext = True
        

        # variables concerning iterative steepness
        self.k_start=k_start
        self.max_iteration = max_iteration
        self.k_step = k_step
        
        # name of descriptor
        self.D_name = D_name
        
        
        # makes tight r-List for determination of r_cleave
        self.tight_distance=[i for i in np.arange(self.distance_data[0],self.infinite_distance,self.tightness)]
        
    
    # functions for fitting procedure
    def exp_falling(self, x, a,k,d):
        return a*(np.exp(-k*x))+d
    
    def gradient_exp(self, x,a,k):
        return -a*k*(np.exp(-k*x))
    
    def sigmoid(self, x,a,d):
        return a/(1+np.exp(self.k*(x-self.r_cleave)))+d
        
    def morse(self, x, q, m, v):
        return (q * (np.exp(-2*m*(x-self.u))-2*np.exp(-m*(x-self.u))) + v)
        
    
    # function for finding dG_TS
    def descriptor_fitter(self):

        
        # setting max. value of descriptor as 1
        for i in range(len(self.descriptor_data)):
            self.descriptor_data[i] = (self.descriptor_data[i] - self.min_descriptor)/self.max_descriptor
        
        
        # initialize starting value of k
        self.k = self.k_start

        #fitting for descriptor
        popt, pcov = curve_fit(self.exp_falling,self.distance_data[:len(self.descriptor_data)],self.descriptor_data, maxfev=45000)
        
        # make tightly spaced list for descriptor
        for i in range(len(self.tight_distance)):
            self.descriptor_fit.append(self.exp_falling(self.tight_distance[i], *popt))
        
        

        # defining cleaving distance r_cleave
        for i in range(len(self.tight_distance)):
            if self.r_cleave_ext == True:
                break
            elif abs(self.gradient_exp(self.tight_distance[i],popt[0],popt[1]))<=self.gamma_cleave:
                self.r_cleave= self.tight_distance[i]
                break
    
        
        # fitting for electronic energy dE
        tstart = [max(self.dE_data),2,0]


        w = 1000
        self.u = self.distance_data[self.dE_data.index(min(self.dE_data))]
        popt_morse, pcov_morse = curve_fit(self.morse, self.distance_data+[self.distance_data[-1]]*w+[self.distance_data[0]]*w,
                                           self.dE_data+[self.dE_data[-1]]*w+[self.dE_data[0]]*w,
                                           p0=tstart, maxfev=4000000)


        # tight list of dE fit
        for i in range(len(self.tight_distance)):
            self.dE_fit.append(self.morse(self.tight_distance[i],*popt_morse))
        
        # function for iterational procedure for steepness (k-value)
        for j in range(0,self.max_iteration):
            self.dG_fit=[]
            self.TdS_fit=[]

            # 3-point fit for TdS
            popt_sig, pcov_sig = curve_fit(self.sigmoid, [self.distance_data[0],self.infinite_distance],
                                           [self.TdS_AB, self.TdS_A + self.TdS_B],
                                           method="dogbox",maxfev=400000)
            # tight list for TdS
            for i in range(len(self.tight_distance)):
                self.TdS_fit.append(self.sigmoid(self.tight_distance[i],*popt_sig))

            # dG = dH - TdS
            for i in range(len(self.tight_distance)):
                self.dG_fit.append(self.TdS_fit[i] + self.dE_fit[i])

                
            # setting starting structure as dG = 0
            min_dG=self.dG_fit[0]                       
            for i in range(len(self.dG_fit)):
                self.dG_fit[i] = self.dG_fit[i] - min_dG
            

            # adding value to k
            self.k=self.k - self.k_step
            # check, if minimum after TS is still present
            # if no minumum is present, prints parameters
            if min(self.dG_fit[self.dG_fit.index(max(self.dG_fit)):])==self.dG_fit[-1]:
                # defining dG_TS
                self.dG_TS = max(self.dG_fit)
                self.r_TS = self.tight_distance[self.dG_fit.index(max(self.dG_fit))]
                print("k-iterations: {}/{}".format(str(j), str(self.max_iteration)))
                print("Dissociation Barrier Energy dG_TS =     {} kJ/mol".format(str("%.3f" %self.dG_TS)))
                print("Dissociation Barrier Distance r_TS =     {} A".format(str("%.3f" %self.r_TS)))
                break


            elif j==self.max_iteration:
                print("Last iteratation reached! Change parameters k_start and/or k_step!")

                


        self.OutputData = [self.tight_distance, self.dE_fit,self.descriptor_fit, self.TdS_fit, self.dG_fit, self.r_cleave, self.dG_TS,  self.r_TS, self.k]
        self.InputData = [self.descriptor_data, self.distance_data, self.dE_data, [self.TdS_A, self.TdS_B, self.TdS_AB], self.infinite_distance ]

    def run(self):
        self.descriptor_fitter()
        return   self.InputData, self.OutputData
    



