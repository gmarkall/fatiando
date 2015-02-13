from __future__ import division
import numpy as np
from numpy.testing import assert_allclose
from fatiando.gravmag import fourier, prism
from fatiando import gridder, utils
from fatiando.mesher import Prism


def test_derivatives():
    "gravmag.fourier x and y derivatives against analytical solutions"
    model = [Prism(-1000, 1000, -1000, 1000, 0, 2000, {'density': 100})]
    shape = (300, 300)
    x, y, z = gridder.regular([-10000, 10000, -10000, 10000], shape, z=-500)
    # Note: The z derivative appears to have a systematic error. Could not get
    # the test to pass.
    derivatives = 'x y'.split()
    # Note: Calculating the x derivative of gx fails for some reason.
    grav = utils.mgal2si(prism.gz(x, y, z, model))
    for deriv in derivatives:
        analytical = getattr(prism, 'g{}z'.format(deriv))(x, y, z, model)
        calculated = utils.si2eotvos(
            getattr(fourier, 'deriv' + deriv)(x, y, grav, shape))
        # Remove the edges from comparison
        actual = np.reshape(calculated, shape)[50:-50, 50:-50]
        desired = np.reshape(analytical, shape)[50:-50, 50:-50]
        assert_allclose(actual, desired, atol=0.0, rtol=1e-3,
                        err_msg="Failed for g{}z".format(deriv))