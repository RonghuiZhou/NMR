import nmrglue as ng
import matplotlib.pyplot as plt
import numpy as np
import os

def plotNMR(nmr_subfolder, graph = False):
    pfile = os.path.join(nmr_subfolder, "pdata", "1")
    water_peak = ''

    if os.path.exists(pfile):
        p1r = os.path.join(pfile, "1r")
        if os.path.exists(p1r):
            print("This is a 1D NMR spectrum.")

            # read Bruker data
            dic, data = ng.bruker.read_pdata(pfile)

            # convert to pipe format for ppm scaling
            C = ng.convert.converter()
            C.from_bruker(dic, data)
            pdic,pdata = C.to_pipe()

            # make ppm scale
            uc = ng.pipe.make_uc(pdic,pdata)

            # get ppm for the highest peak, water peak in this case
            water_position = np.argmax(pdata)
            water_peak = uc.ppm_scale()[water_position]
            water_peak = round(water_peak, 4)
            print(f"water: {water_peak} ppm")

            # plot the spectrum
            if graph:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.plot(uc.ppm_scale(), data, 'k-')
                # invert chemical shift scale as convention
                ax.invert_xaxis()
                ax.set_xlabel("Chemical shift (ppm)")
                ax.set_ylabel("Signal (A.U.)")

                # make the title as the NMR data file name
                sample_info = nmr_subfolder.rsplit("\\", 2)[1:]
                title = '\\'.join(sample_info)
                ax.set_title(title)

                # label water peak position in the figure
                x_text = uc.ppm_scale().max()
                y_text = int(9 * pdata.real.max()/10)
                txt = "Max Peak Position: \n" + str(water_peak) + " ppm"
                plt.text(x_text, y_text , txt)

                fig_name = '_'.join(sample_info) + ".png"
                # plt.show()

                plt.savefig(fig_name)
                plt.close()
        else:
            print("This is not a 1D NMR spectrum.")
    return water_peak

def main():
    nmr_subfolder = r'.\Ibuprofen\10'
    water_peak = plotNMR(nmr_subfolder, graph = True)

if __name__ == "__main__":
    main()