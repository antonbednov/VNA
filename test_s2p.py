import sys
import unittest
sys.path.append('modules')

import s2p

class s2pTestClass (unittest.TestCase):
    
    def test_getparams(self):
        params = {'freq-unit':'GHZ', 'param-type':'S', 'data-format':'RI', 'keyword':'R', 'impedance-ohms':50}
        self.assertEqual(params, s2p.getparams())
        
    def test_readFile(self):
        s = '.\s2p_files\Calibrovka 1.s2p'
        [freq, arrS, params] = s2p.readFile(s)
#print(params)
#print(freq)
#print(s)
        self.assertEqual(len(freq), 9001)
    
    def test_writeFile(self):
        s = '.\s2p_files\Calibrovka 1.s2p'
        [freq, arrS, params] = s2p.readFile(s)
        s2p.writeFile(s+'.test', freq, arrS, params)
        