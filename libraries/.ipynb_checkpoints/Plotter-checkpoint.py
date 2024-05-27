import matplotlib.pyplot as plt
import os

def plotter(CalcData, fontsize=16, D_name = "Descriptor",  savepath=""):

    
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

    
    colorlist = ["firebrick","darkblue","darkgreen","purple"]
    labelist = ["$\Delta E_{fit}$", "$D_{fit}$", "$-T \Delta S_{fit}$",  "$\Delta G_{fit}$"]
    labelist2 = ["$\Delta E_{fit}$", "$D_{fit}$", "$-T \Delta S_{fit}$",  "$\Delta G_{fit}$"]
    
    plt.rcParams["figure.figsize"] = [12, 10]

    fig, axs = plt.subplots(4, 2, sharex=False, gridspec_kw={'width_ratios': [4, 1]})

    plt.subplots_adjust(wspace=0.1, hspace=0.0)

    datalist = [dE_data, descriptor_data]
    fit_list = [dE_fit, descriptor_fit, TdS_fit, dG_fit]

    for ax in axs:
        ax[0].set_xlim(distance_data[0] - 0.25, infinite_distance - 0.5)
        ax[1].set_xlim(infinite_distance - 1, infinite_distance + 1)
        ax[1].spines['left'].set_visible(False)
        ax[0].spines['right'].set_visible(False)
        ax[0].axvline(r_cleave, color="black", linestyle="dashed", alpha=0.5)
        ax[1].set_yticks([])
        ax[0].label_outer()
        ax[1].label_outer()
        ax[0].tick_params(axis="both", which="major", labelsize=fontsize * 3 / 5)
        ax[1].set_xticks([infinite_distance])
        ax[1].set_xticklabels(["$\infty$"], fontsize=fontsize)
        ax[0].set_xlabel("$r_{A \cdot \cdot B}$ / $\AA$", fontsize=fontsize)

    


    a = 1

    for i in range(len(datalist)):
        axs[i][0].scatter(distance_data[:len(datalist[i])], datalist[i], color=colorlist[i], zorder=10, s=25, alpha=a, edgecolor="k")
        axs[i][1].scatter(distance_data[:len(datalist[i])], datalist[i], color=colorlist[i], zorder=10, s=25, alpha=a, edgecolor="k")

    axs[1][1].scatter(distance_data[:len(datalist[1])], datalist[1], color=colorlist[i], edgecolor="k", zorder=10, s=25, label="$D$", alpha=a)

    axs[-2][0].scatter([tight_distance[0], tight_distance[-1]],
                       [TdS_AB, TdS_A + TdS_B],
                       color=colorlist[-2], zorder=10, label="$-T \Delta S$", s=25, alpha=a, edgecolor="k")

    axs[-2][1].scatter([tight_distance[0], tight_distance[-1]],
                       [TdS_AB, TdS_A + TdS_B],
                       color=colorlist[-2], zorder=10, s=25, label="$-T \Delta S$", alpha=a, edgecolor="k")
    axs[0][1].scatter(tight_distance[-1],
                      dE_fit[-1],
                      color=colorlist[0], zorder=10, label="$\Delta E$", alpha=a, edgecolor="k")

    axs[0][0].set_ylabel("$\Delta E$ / $kJ \cdot mol^{-1}$", fontsize=fontsize * 4.5 / 5)
    axs[1][0].set_ylabel(D_name + " / -", fontsize=fontsize * 4 / 5)
    axs[2][0].set_ylabel("$-T \Delta S$ / $kJ \cdot mol^{-1}$", fontsize=fontsize * 4.5 / 5)
    axs[3][0].set_ylabel("$\Delta G$ / $kJ \cdot mol^{-1}$", fontsize=fontsize * 4.5 / 5)



    axs[-1][0].scatter(r_TS, dG_TS, color=colorlist[-1], edgecolor="k", marker="d", zorder=100, s=50)
    axs[-1][1].scatter(r_TS, dG_TS, color=colorlist[-1], edgecolor="k", marker="d", zorder=100, s=50, label="$\Delta G^{\u2021}$")

    for i in range(len(fit_list)):
        axs[i][0].plot(tight_distance[:len(fit_list[i])], fit_list[i],
                       color=colorlist[i], alpha=1, linewidth=2)
        axs[i][1].plot(tight_distance[:len(fit_list[i])], fit_list[i],
                       color=colorlist[i], alpha=1, label=labelist[i], linewidth=2)
        axs[i][1].legend(fontsize=fontsize * 4 / 5, loc="lower right")

    axs[0][0].text(-0.13, 0.92, "a", weight="bold", fontdict=None, fontsize=fontsize, horizontalalignment='left',
                   verticalalignment='top', transform=axs[0][0].transAxes)
    axs[1][0].text(-0.13, 0.92, "b", weight="bold", fontdict=None, fontsize=fontsize, horizontalalignment='left',
                   verticalalignment='top', transform=axs[1][0].transAxes)
    axs[2][0].text(-0.13, 0.92, "c", weight="bold", fontdict=None, fontsize=fontsize, horizontalalignment='left',
                   verticalalignment='top', transform=axs[2][0].transAxes)
    axs[3][0].text(-0.13, 0.92, "d", weight="bold", fontdict=None, fontsize=fontsize, horizontalalignment='left',
                   verticalalignment='top', transform=axs[3][0].transAxes)

    axs[3][1].axvline(r_cleave, color="black", linestyle="dashed", alpha=0.5, label="$r_{cleave}$")
    axs[3][1].legend(fontsize=fontsize * 4 / 5, loc="lower right")

    for i in range(len(axs)):
        axs[i][1].text(-0.01, -0.03, "/", transform=axs[i][1].transAxes, fontsize=15)
        axs[i][0].text(1.0, -0.03, "/", transform=axs[i][0].transAxes, fontsize=15)

    axs[0][1].text(-0.01, 0.97, "/", transform=axs[0][1].transAxes, fontsize=15)
    axs[0][0].text(1.0, 0.97, "/", transform=axs[0][0].transAxes, fontsize=15)

    
    labelx = -0.065
    

    for i in range(len(axs)):
        axs[i, 0].yaxis.set_label_coords(labelx, 0.5)

    if savepath != "":
        try:
            os.mkdir(savepath + "plots")
        except FileExistsError:
            pass

        plt.savefig(savepath + "/plots/" + D_name + ".png", dpi=500, bbox_inches="tight")
        plt.show()
