from pyfem2 import *

nodtab = [[1,-4,3], [2,0,0], [3,0,3], [4,nan,nan], [5,4,3]]
eletab = [[1,1,3], [2,3,5], [3,1,2], [4,2,3], [5,2,5]]
V = PlaneBeamColumnTrussModel('PlaneBeamColumn')
V.Mesh(nodtab=nodtab, eletab=eletab)
Ec, Em = 30000, 200000
V.Material('Material-1')
V.materials['Material-1'].Elastic(E=Ec, Nu=.3)
V.Material('Material-2')
V.materials['Material-2'].Elastic(E=Em, Nu=.3)
V.ElementBlock('B1', (1,2))
V.ElementBlock('B2', (3,5))
V.ElementBlock('B3', (4,))
V.AssignProperties('B1', PlaneBeamColumn, 'Material-1', A=.02, Izz=.004)
V.AssignProperties('B2', ElasticLink2D2, 'Material-2', A=.001)
V.AssignProperties('B3', ElasticLink2D2, 'Material-2', A=.003)
V.PrescribedBC(1, (X,Y,TZ))
V.PrescribedBC(5, Y)
V.ConcentratedLoad(2, Y, 100)
V.ConcentratedLoad(5, TZ, 200)
V.ConcentratedLoad(5, X, 300)
V.Solve()
V.WriteResults()
