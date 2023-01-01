import planesections as ps
import numpy as np

import matplotlib.pyplot as plt

# Define node locations, and support conditions
L = 4
beam = ps.newEulerBeam2D(L)


# Define beam and fixities-
pinned = [1,1,0]
beam.setFixity(L*0.1, pinned, label = 'A')
beam.setFixity(L*0.9, pinned, label = 'B')

# Define loads
Pz = -1
beam.addVerticalLoad(L*0.5, 5*Pz)
# beam.addDistLoadVertical(0, L, Pz)
# beam.addDistLoadVertical(1, L*0.3, 5*Pz)

# Plot the beam diagram
ps.plotBeamDiagram(beam)

# Run the analysis
analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

# Plot the SFD and BMD

ps.plotMoment2D(beam)
var = ps.plotShear2D(beam)

plt.show()
