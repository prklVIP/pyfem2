#!/usr/bin/env python
import sys
sys.path.insert(0, '../')
from pyfem2 import *
import matplotlib.pyplot as plt

mu = 1.
Nu = .499
E = 2. * mu * (1. + Nu)

def LinearSolution(ax=None):
    V = FiniteElementModel(jobid='VolumeLocking.Linear')
    V.AbaqusMesh('ThickCylinder_Linear.inp')
    mat = V.Material('Material-1')
    mat.Elastic(E=E, Nu=Nu)
    V.AssignProperties('ALL', PlaneStrainQuad4Reduced, mat, t=1)
    V.PrescribedBC('SymYZ', X)
    V.PrescribedBC('SymXZ', Y)
    step = V.StaticStep()
    # Pressure on inside face
    step.Pressure('SurfID', 1.)
    step.run()
    V.WriteResults()
    ax = V.Plot2D(deformed=1, color='b', linestyle='-.', ax=ax, label='Linear',
                  xlim=(-.2,5), ylim=(-.2, 5))
    return ax

def QuadraticSolution(ax=None):
    V = FiniteElementModel(jobid='VolumeLocking.Quadratic')
    V.AbaqusMesh('ThickCylinder_Quadratic.inp')
    mat = V.Material('Material-1')
    mat.Elastic(E=E, Nu=Nu)
    V.AssignProperties('ALL', PlaneStrainQuad8BBar, mat, t=1)
    V.PrescribedBC('SymYZ', X)
    V.PrescribedBC('SymXZ', Y)
    # Pressure on inside face
    step = V.StaticStep()
    step.Pressure('SurfID', 1.)
    step.run()
    V.WriteResults()
    return ax

def WriteAnalyticSolution(ax=None):
    mesh = Mesh(filename='ThickCylinder_Linear.inp')
    ix = where(mesh.coord[:,1]<=1e-12)
    a = mesh.coord[ix][:,0].min()
    b = mesh.coord[ix][:,0].max()
    p = 1.
    u = zeros_like(mesh.coord)
    for (i, x) in enumerate(mesh.coord):
        r = sqrt(x[0] ** 2 + x[1] ** 2)
        term1 = (1. + Nu) * a ** 2 * b ** 2 * p / (E * (b ** 2 - a ** 2))
        term2 = 1. / r + (1. - 2. * Nu) * r / b ** 2
        ur = term1 * term2
        u[i, :] = ur * x[:] / r
    mesh.PutNodalSolution('VolumeLocking.Analytic', u)
    ax = mesh.Plot2D(xy=u+mesh.coord, ax=ax, color='orange', weight=6,
                     label='Analytic')
    return ax

ax = None
ax = WriteAnalyticSolution(ax)
ax = LinearSolution(ax)
QuadraticSolution()

if not os.environ.get('NOGRAPHICS'):
    plt.legend()
    plt.show()
