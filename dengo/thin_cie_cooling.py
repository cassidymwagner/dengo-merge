import numpy as np

#     Taken from grackle/clib/cie_thin_cooling_rate_g routine
#
#     written by Tom Abel    8/2003
#     compute optically thin cooling rate due to CIE cooling
#     as discussed in Ripamonti and Abel 2003.
#     input: temp is temperature in Kelvin
#     output total CIE cooling rate (including H2-H2 and He-H2)
#     in erg per second times cm^3 per gram per (gram in H2 molecules).
#     Hence to get cooling rate in erg/s cm^-3 one has to multiply by
#     the total mass density and the mass density in H2 molecules
#     (*rho*rho_H2).
#     This again is an approximation in that it assumes large H2 fractions
#     (greater than 0.5).
#     Currently it is not clear what happens in the regime where H2
#     becomes mostly dissociated.


def cie_cooling_rate(state):

    temp_cie = np.array([400.0, 404.0, 408.0, 412.1, 416.2, 420.4,
        424.6, 428.9, 433.1, 437.5, 441.8, 446.3, 450.7, 455.2,
        459.8, 464.4, 469.0, 473.7, 478.5, 483.2, 488.1, 493.0,
        497.9, 502.9, 507.9, 513.0, 518.1, 523.3, 528.5, 533.8,
        539.1, 544.5, 550.0, 555.5, 561.0, 566.6, 572.3, 578.0,
        583.8, 589.6, 595.5, 601.5, 607.5, 613.6, 619.7, 625.9,
        632.2, 638.5, 644.9, 651.3, 657.9, 664.4, 671.1, 677.8,
        684.6, 691.4, 698.3, 705.3, 712.4, 719.5, 726.7, 733.9,
        741.3, 748.7, 756.2, 763.7, 771.4, 779.1, 786.9, 794.8,
        802.7, 810.7, 818.8, 827.0, 835.3, 843.7, 852.1, 860.6,
        869.2, 877.9, 886.7, 895.6, 904.5, 913.6, 922.7, 931.9,
        941.2, 950.6, 960.2, 969.8, 979.5, 989.2, 999.1, 1009.0,
        1019.0, 1029.0, 1040.0, 1050.0, 1061.0, 1071.0, 1082.0,
        1093.0, 1104.0, 1115.0, 1126.0, 1137.0, 1148.0, 1160.0,
        1172.0, 1183.0, 1195.0, 1207.0, 1219.0, 1231.0, 1244.0,
        1256.0, 1269.0, 1281.0, 1294.0, 1307.0, 1320.0, 1333.0,
        1347.0, 1360.0, 1374.0, 1387.0, 1401.0, 1415.0, 1430.0,
        1444.0, 1458.0, 1473.0, 1488.0, 1502.0, 1517.0, 1533.0,
        1548.0, 1563.0, 1579.0, 1595.0, 1611.0, 1627.0, 1643.0,
        1660.0, 1676.0, 1693.0, 1710.0, 1727.0, 1744.0, 1762.0,
        1779.0, 1797.0, 1815.0, 1833.0, 1852.0, 1870.0, 1889.0,
        1908.0, 1927.0, 1946.0, 1966.0, 1985.0, 2005.0, 2025.0,
        2045.0, 2066.0, 2086.0, 2107.0, 2128.0, 2150.0, 2171.0,
        2193.0, 2215.0, 2237.0, 2259.0, 2282.0, 2305.0, 2328.0,
        2351.0, 2375.0, 2398.0, 2422.0, 2447.0, 2471.0, 2496.0,
        2521.0, 2546.0, 2571.0, 2597.0, 2623.0, 2649.0, 2676.0,
        2702.0, 2730.0, 2757.0, 2784.0, 2812.0, 2840.0, 2869.0,
        2897.0, 2926.0, 2956.0, 2985.0, 3015.0, 3045.0, 3076.0,
        3106.0, 3138.0, 3169.0, 3201.0, 3233.0, 3265.0, 3298.0,
        3331.0, 3364.0, 3397.0, 3431.0, 3466.0, 3500.0, 3535.0,
        3571.0, 3606.0, 3643.0, 3679.0, 3716.0, 3753.0, 3790.0,
        3828.0, 3867.0, 3905.0, 3944.0, 3984.0, 4024.0, 4064.0,
        4105.0, 4146.0, 4187.0, 4229.0, 4271.0, 4314.0, 4357.0,
        4401.0, 4445.0, 4489.0, 4534.0, 4579.0, 4625.0, 4671.0,
        4718.0, 4765.0, 4813.0, 4861.0, 4910.0, 4959.0, 5008.0,
        5058.0, 5109.0, 5160.0, 5212.0, 5264.0, 5316.0, 5370.0,
        5423.0, 5477.0, 5532.0, 5588.0, 5643.0, 5700.0, 5757.0,
        5814.0, 5873.0, 5931.0, 5991.0, 6051.0, 6111.0, 6172.0,
        6234.0, 6296.0, 6359.0, 6423.0, 6487.0, 6552.0, 6617.0,
        6684.0, 6750.0, 6818.0, 6886.0, 6955.0])

    rate_cie = np.array([1.435e-15, 1.488e-15, 1.544e-15, 1.601e-15,
        1.661e-15, 1.722e-15, 1.786e-15, 1.853e-15, 1.922e-15, 1.993e-15,
        2.067e-15, 2.143e-15, 2.223e-15, 2.305e-15, 2.39e-15, 2.479e-15,
        2.57e-15, 2.665e-15, 2.763e-15, 2.865e-15, 2.971e-15, 3.08e-15,
        3.194e-15, 3.314e-15, 3.44e-15, 3.571e-15, 3.707e-15, 3.848e-15,
        3.995e-15, 4.148e-15, 4.307e-15, 4.472e-15, 4.643e-15, 4.822e-15,
        5.008e-15, 5.201e-15, 5.402e-15, 5.611e-15, 5.829e-15, 6.056e-15,
        6.292e-15, 6.539e-15, 6.8e-15, 7.071e-15,  7.354e-15, 7.648e-15,
        7.955e-15, 8.274e-15, 8.607e-15, 8.954e-15, 9.316e-15, 9.692e-15,
        1.008e-14, 1.049e-14, 1.092e-14, 1.136e-14, 1.183e-14, 1.235e-14,
        1.291e-14, 1.35e-14, 1.412e-14, 1.477e-14, 1.545e-14, 1.617e-14,
        1.693e-14, 1.773e-14, 1.857e-14, 1.946e-14, 2.039e-14, 2.137e-14,
        2.242e-14, 2.352e-14, 2.469e-14, 2.592e-14, 2.721e-14, 2.857e-14,
        3e-14, 3.151e-14, 3.31e-14, 3.477e-14, 3.653e-14, 3.838e-14,
        4.053e-14, 4.3e-14, 4.561e-14, 4.837e-14, 5.127e-14, 5.434e-14,
        5.758e-14, 6.099e-14, 6.458e-14, 6.837e-14, 7.236e-14, 7.687e-14,
        8.167e-14, 8.675e-14, 9.21e-14, 9.776e-14, 1.037e-13, 1.1e-13,
        1.167e-13, 1.237e-13, 1.31e-13, 1.388e-13, 1.47e-13, 1.556e-13,
        1.646e-13, 1.741e-13, 1.841e-13, 1.946e-13, 2.057e-13, 2.172e-13,
        2.294e-13, 2.421e-13, 2.554e-13, 2.694e-13, 2.841e-13, 2.994e-13,
        3.155e-13, 3.323e-13, 3.498e-13, 3.682e-13, 3.874e-13, 4.074e-13,
        4.284e-13, 4.502e-13, 4.73e-13, 4.968e-13, 5.216e-13, 5.475e-13,
        5.744e-13, 6.025e-13, 6.318e-13, 6.622e-13, 6.939e-13, 7.268e-13,
        7.611e-13, 7.967e-13, 8.337e-13, 8.721e-13, 9.121e-13, 9.535e-13,
        9.966e-13, 1.041e-12, 1.088e-12, 1.136e-12, 1.185e-12, 1.237e-12,
        1.29e-12, 1.346e-12, 1.403e-12, 1.462e-12, 1.524e-12, 1.587e-12,
        1.653e-12, 1.721e-12, 1.791e-12, 1.864e-12, 1.939e-12, 2.016e-12,
        2.096e-12, 2.179e-12, 2.268e-12, 2.374e-12, 2.483e-12, 2.597e-12,
        2.714e-12, 2.836e-12, 2.961e-12, 3.091e-12, 3.226e-12, 3.365e-12,
        3.508e-12, 3.657e-12, 3.81e-12, 3.968e-12,  4.132e-12, 4.3e-12,
        4.474e-12, 4.654e-12, 4.839e-12, 5.029e-12, 5.226e-12, 5.428e-12,
        5.637e-12, 5.852e-12, 6.073e-12, 6.301e-12, 6.535e-12, 6.776e-12,
        7.024e-12, 7.28e-12, 7.542e-12, 7.812e-12, 8.089e-12, 8.374e-12,
        8.666e-12, 8.967e-12, 9.276e-12, 9.593e-12, 9.919e-12, 1.025e-11,
        1.06e-11, 1.099e-11, 1.145e-11, 1.193e-11, 1.241e-11, 1.292e-11,
        1.343e-11, 1.396e-11, 1.451e-11, 1.507e-11, 1.565e-11, 1.624e-11,
        1.685e-11, 1.748e-11, 1.813e-11, 1.879e-11, 1.947e-11, 2.017e-11,
        2.089e-11, 2.162e-11, 2.238e-11, 2.316e-11, 2.395e-11, 2.477e-11,
        2.561e-11, 2.646e-11, 2.734e-11, 2.824e-11, 2.917e-11, 3.011e-11,
        3.118e-11, 3.234e-11, 3.353e-11, 3.475e-11, 3.601e-11, 3.729e-11,
        3.861e-11, 3.996e-11, 4.135e-11, 4.277e-11, 4.422e-11, 4.571e-11,
        4.724e-11, 4.881e-11, 5.041e-11, 5.205e-11, 5.373e-11, 5.545e-11,
        5.721e-11, 5.901e-11, 6.085e-11, 6.273e-11, 6.47e-11, 6.692e-11,
        6.92e-11, 7.152e-11, 7.391e-11, 7.635e-11, 7.885e-11, 8.141e-11,
        8.402e-11, 8.67e-11, 8.944e-11, 9.224e-11, 9.51e-11, 9.803e-11,
        1.01e-10, 1.041e-10, 1.072e-10, 1.104e-10, 1.137e-10, 1.17e-10,
        1.204e-10, 1.239e-10, 1.275e-10, 1.311e-10, 1.348e-10, 1.386e-10,
        1.425e-10, 1.464e-10, 1.505e-10, 1.546e-10, 1.588e-10, 1.631e-10,
        1.674e-10, 1.719e-10])

    min_cie_temp = temp_cie[0]
    max_cie_temp = temp_cie[-1]

    min_cie_rate = rate_cie[0]
    max_cie_rate = rate_cie[-1]

    _i1 = (state.T <= min_cie_temp)
    _i2 = (state.T <= max_cie_temp)

    # extrapolate high temperature with **3. Not discussed in Ripamonti &Abel...
    vals = max_cie_rate * (state.T / max_cie_temp)**(3)

    # interpolation with the given rates
    vals[_i2] = np.interp( state.T[_i2] , temp_cie, rate_cie)

    # rough low temperature extrapolation
    vals[_i1] = min_cie_rate* (state.T[_i1] / min_cie_temp)**(4)

    return vals
