#%% User-defined parameters

import sys
sys.path.append("/Users/jwellik/PYTHON/")
sys.path.append("/Users/jwellik/PYTHON/vdapseisutils")

from vdapseisutils.maputils.utils.utils import backazimuth_pyproj

import matplotlib.pyplot as plt

from waveform_collection import gather_waveforms
from obspy.core import UTCDateTime
import numpy as np

# from vdapseisutils.maputils.utils.utils import sight_point


def main(markers, verbose=True):

    print(">>> array_processing/<config>.py")

    #%% Array processing and plotting using least squares

    from array_processing.tools.plotting import array_plot
    from lts_array import ltsva
    from array_processing.tools.array_characterization import read_kml

    # latlist = [tr.stats.latitude for tr in st]
    # lonlist = [tr.stats.longitude for tr in st]

    # x = read_kml("./data/tonga_proposed_2023-04-17.kml")

    latlonlist = []
    for mark in markers:
        print(mark)
        latlonlist.append(mark)

    latlist = []
    lonlist = []
    for ll in latlonlist:
        latlist.append(ll[0])
        lonlist.append(ll[1])

    source_latlons = []
    source_latlons.append([-20.536, 175.382])  # Hunga-Tonga
    source_latlons.append([-19.75, 175.07])  # Tofua
    source_latlons.append([-18.992, 174.775])  # Home Reef
    source_lats = []
    sources_lons = []
    # sources.append()
    source_back_az = []
    source_dist = []
    # TODO Determine distance/backazimuth from array-source
    # TODO - Average infrasound location

    #%% Calculate backazimuth from array to source
    from vdapseisutils.maputils.utils.utils import backazimuth_pyproj
    az, dist = backazimuth_pyproj(latlonlist[0], source_latlons[0])
    print("{}km @ {}o".format(dist, az))

    #%% Array uncertainty
    from array_processing.algorithms.helpers import getrij
    from array_processing.tools import arraySig
    from array_processing.tools.plotting import arraySigPlt, arraySigContourPlt

    # SIGLEVEL = 1/st[0].stats.sampling_rate
    SIGLEVEL = 1/100
    KMAX = 400
    TRACE_VELOCITY = 0.33
    rij = getrij(latlist, lonlist)

    if verbose:
        print("Processing array uncertainty")
    sigV, sigTh, impResp, vel, th, kvec = arraySig(rij, kmax=KMAX,
                                                   sigLevel=SIGLEVEL)

    if verbose:
        print("Plotting array maps.")
    fig2 = arraySigPlt(rij, SIGLEVEL, sigV, sigTh, impResp, vel, th, kvec)
    fig2.savefig("./array_map.png")
    # plt.show()

    if verbose:
        print("Plotting array uncertainty.")
    fig3 = arraySigContourPlt(sigV, sigTh, vel, th, trace_v=TRACE_VELOCITY)
    fig3.axes[1].plot(np.deg2rad(0), 4, "*r")  # Tofua
    fig3.axes[1].plot(np.deg2rad(15), 4, "*r")  # Home Reef
    fig3.axes[1].plot(np.deg2rad(325), 4, "*r")  # Hunga-Tonga
    fig3.savefig("./array_uncertainty.jpg")
    # plt.show()

    # TODO Calculate km uncertainty for given distance/back azimuth to possible source
    #

    print("Done.")
    return fig2, fig3


if __name__ == "__main__":
    print(markers)
    main(markers)
