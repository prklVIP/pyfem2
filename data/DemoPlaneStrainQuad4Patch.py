import logging
from pyfem2 import *
V = FiniteElementModel(jobid='PlaneStrainQuad4Patch')
V.AbaqusMesh(filename='EC4SFP1.inp')
mat = V.Material('Material-1')
mat.Elastic(E=1e6, Nu=.25)
V.AssignProperties('EALL', PlaneStrainQuad4, mat, t=.001)

step = V.StaticStep()
step.PrescribedBC(10, (X,Y), 0.)
step.PrescribedBC(20, X, .24e-3)
step.PrescribedBC(20, Y, .12e-3)
step.PrescribedBC(30, X,  .3e-3)
step.PrescribedBC(30, Y, .24e-3)
step.PrescribedBC(40, X, .06e-3)
step.PrescribedBC(40, Y, .12e-3)
step.run()
#V.Plot2D(show=1)
V.WriteResults()

# Average stress must be 1600 in x and y
step = V.steps.last
field = step.frames[-1].field_outputs['S']
for value in field.values:
    data = value.data
    assert allclose(data[:,0], 1600.), 'Wrong Sxx'
    assert allclose(data[:,1], 1600.), 'Wrong Syy'
    assert allclose(data[:,2],  800.), 'Wrong Szz'
    assert allclose(data[:,3],  400.), 'Wrong Sxy'
logging.info('PATCH TEST PASSED')
