from model import *
from agent import *
from lattice import Continuum

def quick_run(runs = 1):
    
    result = []
    for r in range(runs):
        agents = [Parakeet(1) for i in range(3)]
        env = Continuum([(0,0) for i in range(3)])

        m = DeterministModel(agents, env)
        m.run(25)

        # print(m.result)
        # print(m.compute_velocity())
        result.append(m.compute_velocity())
        
    print(np.mean(np.array(result)))
    return result