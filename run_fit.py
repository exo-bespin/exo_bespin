#! /usr/bin/env python

"""Create a lightcurve based on some user-provided parameters.

This code expects three chunks of data read from the `~/params.json`
file:

    1. First, the location of a user-defined (i.e., user-uploaded)
       ascii file, with times in the first column, fluxes in the second
       and errors on the third --- user_params['filename']

    2. Second, a set of definitions on the starting points, prior
       distribution and prior hyperparameters of each of the parameters
       to be fitted. The full list of parameters is defined below on
       the "all_parameters" variable. For each of these, this code
       expects to find:

      a) A definition of the prior distribution of the parameter, e.g.,
         user_params['P_p1_prior'] = 'normal'. Distribution can be
         'fixed' for fixed parameters.

      b) A starting value for the parameter, e.g.,
         user_params['P_p1_starting_value'] = 1.

      c) If the distribution is NOT `fixed`, two hyperparmeters
         defining the prior, e.g.,
         user_params['P_p1_starting_hyperparameter1'] = 1.,
         user_params['P_p1_starting_hyperparameter2'] = 0.01. If the
         distribution is `fixed`, adding those won't matter.

    3. The third are parameters for the sampler, in this case emcee. In
       particular, need to know the number of walkers, steps and burnin
       steps, e.g., user_params['nwalkers'] = 100,
       user_params['nsteps'] = 300, user_params['nburnin'] = 500.
"""

import json
import os
import random

import corner
import juliet
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

random.seed(42)

# Read in user-provided paramater file
with open(os.path.join(os.path.expanduser("~"), 'params.json'), 'r') as f:
    user_params = json.load(f)

# First, read-in lightcuve data into numpy arrays:
t, f, ferr = np.loadtxt(os.path.join(os.path.expanduser("~"), 'lightcurve.dat'), unpack = True, usecols = (0, 1, 2))

# Save those arrays into dictionaries, which is what juliet likes:
times, fluxes, errors = {}, {}, {}

times['inst'], fluxes['inst'], errors['inst'] = t, f, ferr

# All right, now assume the user ingested all the priors. I'm going to assume the web form is able to 
# parse each parameter as follows. First we will have 12 parameters the form needs to let the user decide 
# for: P_p1, t0_p1, p_p1, b_p1, q1_inst, q2_inst, eccentricity_p1, omega_p1, a_p1, mdilution_inst, mflux_inst and sigma_w_inst:

priors = {}
starting_point = {}

# Define all possible parameters:
all_parameters = ['P_p1', 't0_p1', 'p_p1', 'b_p1', 'q1_inst', 'q2_inst', 'ecc_p1', 'omega_p1', 'a_p1', \
                  'mdilution_inst', 'mflux_inst', 'sigma_w_inst']

# Define names for each of them (useful for plots):
parameter_names = ['Period', r'$t_0$', r'$R_p/R_s$', r'$b$', r'$q_1$', r'$q_2$', r'$e$', r'$\omega$', r'$a/R_s$', \
                 'Dilution', 'Mean Flux', r'$\sigma_w$ (ppm)']

for i in range(len(all_parameters)):

    parameter = all_parameters[i]

    # Create key in the priors dictionary:
    priors[parameter] = {}
    # Save distribution read by the form:
    priors[parameter]['distribution'] = user_params[parameter+'_prior']
    # Save strting value of the parameter, also read by the form:
    starting_point[parameter] = user_params[parameter+'_starting_value']

    # Now, for each parameter, the form should tell us if the parameter's prior is 'fixed' or not. If `fixed`, then 
    # set the hyperparameter value to the strting point of the parameter (that the form should also know):
    if user_params[parameter+'_prior'] == 'fixed':

        priors[parameter]['hyperparameters'] = user_params[parameter+'_starting_value']

    else:

        priors[parameter]['hyperparameters'] = [user_params[parameter+'_hyperparameter1'], user_params[parameter+'_hyperparameter2']] 

        # This key doesn't tell anything to juliet, but we use it below for plotting purposes:
        priors[parameter]['name'] = parameter_names[i]

# Load and fit dataset with juliet. Note the form also needs to retrieve the nwalkers, nsteps and nburnin parameters:
dataset = juliet.load(priors=priors, t_lc=times, y_lc=fluxes, yerr_lc=errors, out_folder='results', starting_point=starting_point)

results = dataset.fit(sampler='emcee', progress=True, nwalkers = user_params['nwalkers'], nsteps = user_params['nsteps'], nburnin = user_params['nburnin'])

# Extract posterior model predictions:
model, errup68, errdown68 = results.lc.evaluate('inst', return_err=True)
model, errup95, errdown95 = results.lc.evaluate('inst', return_err=True, alpha = 0.95)

# Extract extra jitter on lightcurve:
if 'sigma_w_inst' in results.posteriors['posterior_samples'].keys():

    sigma_w = np.median(results.posteriors['posterior_samples']['sigma_w_inst']) * 1e-6
    
    ferr = np.sqrt(ferr**2 + sigma_w**2)


# First, plot lightcurve best-fit and residuals. To this, do a 
#two-grid plot to plot data and residuals, respectively:
grid = GridSpec(10, 1)

# If TESS-like lightcurve, plot long plot:
if (np.max(t) - np.min(t)) > 1.:

    fig = plt.figure(figsize=(5,10)) 

else:

    fig = plt.figure(figsize=(8,5))

ax1 = fig.add_subplot(grid[0:7, :])
ax2 = fig.add_subplot(grid[7:, :])

# Plot data:
ax1.errorbar(t, f, ferr, fmt = '.', color = 'black', zorder = 5)

# Plot best-fit model with errors:
ax1.plot(t, model, color = 'orangered', zorder = 4)
ax1.fill_between(t, errdown95, errup95, color='cornflowerblue', alpha = 0.5, zorder = 3)
ax1.fill_between(t, errdown95, errup95, color='cornflowerblue', alpha = 0.5, zorder = 3)
ax1.set_xlim(np.min(t), np.max(t))

# Plot residuals:
ax2.errorbar(t, (f - model)*1e6, ferr*1e6, fmt = '.', color = 'black', zorder = 5)
ax2.plot([np.min(t), np.max(t)], [0, 0] , '--', color = 'orangered', zorder = 3)
ax2.set_xlim(np.min(t), np.max(t))

# Labels:
ax1.set_ylabel('Relative flux')
ax2.set_ylabel('Residuals (ppm)')
ax2.set_xlabel('Time (days)')

plt.tight_layout()
plt.savefig('transit_fit.png')

# Now plot posterior distributions. First, grab all posteriors in a matrix:
first_time = True
names = []

for parameter in list(results.posteriors['posterior_samples'].keys()):

    if parameter not in ['unnamed', 'loglike']:

        if first_time:

            X = results.posteriors['posterior_samples'][parameter]
            first_time = False

        else:

            X = np.vstack(( X, results.posteriors['posterior_samples'][parameter]))

        names.append(priors[parameter]['name'])

# Plot:
figure = corner.corner(X.transpose(), labels = names, \
                       quantiles=[0.16, 0.5, 0.84],\
                       show_titles = True, title_kwargs={"fontsize": 12})

plt.tight_layout()
plt.savefig('corner_plot.png')
