from model import *
from agent import *
from lattice import Continuum
import functools


kernel = params.r2Dtrans
kernel = functools.partial(kernel, beta = 0.000499, lambda1 = 0.000387, lambda2 = 0.009626, xmin = 13, xmax = 28578)

def quick_run(runs, model_iters = 25, n_agents = 3):
    
    result = []
    r = []
    while len(result) < runs:

        agents = [Parakeet(1) for i in range(n_agents)]
        env = Continuum([(0,0) for i in range(n_agents)])

        m = DeterministModel(agents, env)
        m.run(model_iters)
        
        if 0 in list(m.result['n']):
            continue

        result.append(m.compute_velocity())
        r.append(list(m.result['r'][1:]))
        print('Iteration: %03d' % len(result), end = '\r')
        
    df = pd.DataFrame({'t': list(range(1, model_iters + 1)),
                       'r': np.mean(np.array(r), axis = 0),
                       'sd': np.std(np.array(r), axis = 0)})
        
    return result, df