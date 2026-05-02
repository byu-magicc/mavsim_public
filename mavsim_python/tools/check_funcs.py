"""
mavsimPy
    Check code output against (known good--hopefully) sim values
        2025-02-12 - engband
"""
import numpy as np

import tools.color
# ======================================
# ======================================

# left pad size
lpad = 17

def err_msg_scalar(soln, check):
    str_fail    = f"{tools.color.red('FAIL'):<28}"
    str_ck      = f"yours = {tools.color.red(check):<37}"
    str_soln    = f"expected = {tools.color.violet(soln)}"
    return ''.join([str_fail, str_ck, str_soln])
#
# check error
def ck_err(soln, check):

    tol_zero = 1e-14
    tol_perc = 1e-4

    if np.isscalar(soln):
        pass_zero = False
        # if soln < tol_zero:
        if soln == 0.:
            pass_zero = check < tol_zero
            if pass_zero:
                return f"{tools.color.green('PASS')}"
            else:
                return err_msg_scalar(soln, check)
            #
        #
        err = check - soln
        err_abs = np.abs(err)
        err_perc = err_abs / np.abs(soln)
        pass_perc = err_perc < tol_perc
        if pass_perc:
            return f"{tools.color.green('PASS')}"
        else:
            return err_msg_scalar(soln, check)
        #
    #

    corr_idxs = np.zeros_like(soln, dtype=bool)

    mask0 = soln == 0.
    mask1 = np.logical_not(mask0)

    # handle zero entries
    corr_idxs[mask0] = np.abs(check[mask0]) < tol_zero

    # handle non-zero entries
    soln_test = soln.copy()
    # avoid divide by zero
    soln_test[mask0] = 1.

    err = check - soln
    err_abs = np.abs(err)
    err_percent = err_abs / np.abs(soln_test)
    corr_idxs[mask1] = err_percent[mask1] < tol_perc

    if corr_idxs.all():
        return f"{tools.color.green('PASS')}"
    else:
        wrong_val_mask = np.logical_not(corr_idxs)
        wrong_val_idxs = np.argwhere(wrong_val_mask)
        msg = [f"{tools.color.red('FAIL')}"]
        for idx in wrong_val_idxs:
            idx_str = f"idx {tools.color.blue(idx)}"
            chk_str = f"yours = {tools.color.red(check[idx])}"
            sln_str = f"expected = {tools.color.violet(soln[idx])}"
            msg.append(f'{idx_str:>{45}}: {chk_str:<{45}}{sln_str}')
        return '\n'.join(msg)
    #
#
