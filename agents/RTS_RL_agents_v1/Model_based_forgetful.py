"""Model based model. The MB model with forgetful decay as in Collins & Frank 2012. """
import numpy as np
from numba import jit
from random import random, randint
from .core import TwoStepModelCoreCSO, _compute_loglik, _step_other_variables

INIT_Q = 0.5
@jit(nopython=True)
def _MB_step_core_variables(alpha, beta, p_transit, c, s, o, Q_s, Q_mb):
    nc = 1 - c  # Not chosen first step action.
    ns = 1 - s  # Not reached second step state.

    Q_s_new = Q_s.copy()
    # update action values.
    Q_s_new[s] = (1. - alpha) * Q_s[s] + alpha * o
    Q_s_new = (1. - beta) * Q_s_new + beta * INIT_Q

    Q_mb_new = p_transit * Q_s_new + (1-p_transit) * Q_s_new[::-1]

    return Q_s_new, Q_mb_new


@jit(nopython=True)
def _MB_session_likelihood_core(alpha, beta, iTemp, p_transit, choices, second_steps, outcomes, Q_s, Q_mb, scores, choice_probs, n_trials):
    trial_log_likelihood = np.zeros(n_trials)
    for trial in range(n_trials):
        c, s, o = choices[trial], second_steps[trial], outcomes[trial]
        trial_log_likelihood[trial] = _compute_loglik(choice_probs[trial], c)
        Q_s[trial + 1], Q_mb[trial + 1] = _MB_step_core_variables(alpha, beta, p_transit, c, s, o, Q_s[trial], Q_mb[trial])
        scores[trial + 1], choice_probs[trial + 1] = _step_other_variables(iTemp, Q_mb[trial + 1])
    return trial_log_likelihood, Q_s, Q_mb, scores, choice_probs

class Model_based_forgetful(TwoStepModelCoreCSO):
    def __init__(self, p_transit=0.8):
        super().__init__()
        self.name = 'Model based forgetful'
        self.param_names = ['alpha', 'beta', 'iTemp']
        self.params = [ 0.5   , 0.5   , 5.    ]
        self.param_ranges = ['unit' , 'unit' ,'pos'  ]
        self.n_params = 3
        self.p_transit = p_transit
        self.state_vars = ['Q_s']

    def _init_core_variables(self, wm, params):
        if wm is None:
            self.wm = {
                'Q_s': np.ones(2) * INIT_Q,
                'Q_mb': np.ones(2) * INIT_Q,
            }
        else:
            if 'h0' in wm:
                self.wm = {
                    'Q_s': wm['h0'],
                    'Q_mb': self.p_transit * wm['h0'] + (1-self.p_transit) * wm['h0'][::-1]
                }
            else:
                self.wm = wm

    def _step_core_variables(self, trial_event, params):
        (c, s, o) = trial_event
        alpha, beta, iTemp = params
        self.wm['Q_s'], self.wm['Q_mb'] = _MB_step_core_variables(alpha, beta, self.p_transit, c, s, o, self.wm['Q_s'], self.wm['Q_mb'])

    def _step_other_variables(self, params):
        alpha, beta, iTemp = params
        self.wm['scores'], self.wm['choice_probs'] = _step_other_variables(iTemp, self.wm['Q_mb'])

    def _session_likelihood_core(self, session, params, DVs):
        alpha, beta, iTemp = params
        DVs['trial_log_likelihood'], DVs['Q_s'], DVs['Q_mb'], DVs['scores'], DVs['choice_probs'] = _MB_session_likelihood_core(
            alpha, beta, iTemp, self.p_transit, session['choices'], session['second_steps'], session['outcomes'],
            DVs['Q_s'], DVs['Q_mb'], DVs['scores'], DVs['choice_probs'], session['n_trials'])
        return DVs