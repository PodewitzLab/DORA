# printing result
# error massage if no transitions state can be found
# def printer(OutputData, OutputFit = False, OutputTS = True):

#     if self.dG_TS == 0:
#             print("Dissociation Barrier = 0, something went wrong!")
#         else:
#             print("dG_AB =     {} kJ/mol".format(str("%.3f" %self.dG_fit[0])))
#             print("dG_A+B =    {} kJ/mol".format(str("%.3f" %self.dG_fit[-1])))
#             print("-------------------------------------------------------------------")
#             print("dG_TS =     {} kJ/mol".format(str("%.3f" %self.dG_TS)))
#             print("r_TS =     {} A".format(str("%.3f" %self.r_TS)))
#             print("===================================================================")
#         return self.dG_TS, self.r_TS, self.dG_fit, self.tight_distance


# def output_printer():

#     with open(self.savepath + self.D_name + "_" + str(self.gamma_cleave) + ".dat","w+") as output_data:
#         print("dG_AB =     {} kJ/mol".format(str("%.3f" %self.dG_fit[0])), file= output_data)
#         print("dG_A+B =    {} kJ/mol".format(str("%.3f" %self.dG_fit[-1])), file= output_data)
#         print("-------------------------------------------------------------------", file= output_data)
#         print("dG_TS =     {} kJ/mol".format(str("%.3f" %self.dG_TS)), file= output_data)
#         print("r_TS =     {} A".format(str("%.3f" %self.r_TS)), file= output_data)
#         print("===================================================================", file= output_data)
        
#     with open(self.savepath + self.D_name + "_" + str(self.gamma_cleave) + "_fit.dat","w+") as output_data_fit:
#         for i in range(len(self.dG_fit)):
#             print(f"{str(round(self.tight_distance[i],5)):<1} {str(round(self.dG_fit[i],5)):<15}", end="\n",file = output_data_fit)
#             # print("\n", file = output_data_fit) 



def PrintFits(CalcData, savepath):
    descriptor_data = CalcData[0][0]
    distance_data = CalcData[0][1]
    dE_data = CalcData[0][2]
    TdS_A = CalcData[0][3][0]
    TdS_B = CalcData[0][3][1]
    TdS_AB = CalcData[0][3][2]
    infinite_distance = CalcData[0][4]

    tight_distance = CalcData[1][0]
    dE_fit = CalcData[1][1]
    descriptor_fit = CalcData[1][2]
    TdS_fit = CalcData[1][3]
    dG_fit = CalcData[1][4]
    r_cleave = CalcData[1][5]
    dG_TS = CalcData[1][6]
    r_TS = CalcData[1][7]
    k =  CalcData[1][8]


    with open(str(savepath) + "DORA_Fit_data.dat", "w+") as OutputFit:
        print("{:<20} {:<20} {:<20} {:<20} {:<20}".format("r", "dE_fit", "D_fit", "TdS_fit", "dG_fit"),file=OutputFit)

        for i in range(len(tight_distance)):
            print("{:<20} {:<20} {:<20} {:<20} {:<20}".format(str("%.5f" %tight_distance[i]), str("%.5f" %dE_fit[i]), str("%.5f" %descriptor_fit[i]), str("%.5f" %TdS_fit[i]), str("%.5f" %dG_fit[i])),file=OutputFit)

    # with open(self.savepath + "test.dat") as OutputFit:
    #     for i in range(len(self.tight_distance)):
    #         print("{} {} {} {} {}".format(tight_distance[i], dE_fit, TdS_fit, dG_fit),file=OutputFit)

    with open(savepath + "DORA_Results.dat", "w+") as OutputResults:
        print("{:<20} {:<20} {:<20} {:<20}".format("dG_TS", "r_TS", "r_cleave", "k"),file=OutputResults)
        print("{:<20} {:<20} {:<20} {:<20}".format(str("%.5f" %dG_TS), str("%.5f" %r_TS),str("%.5f" %r_cleave), str("%.5f" %r_TS)),file=OutputResults)