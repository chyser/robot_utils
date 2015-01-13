#!/usr/bin/env python
"""
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import pylib.osscripts as oss
import math

#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ usage: 
    """
    args, opts = oss.gopt(argv[1:], [], [('c', 'chassis_len'), ('h', 'chassis_ht'), 
        ('s', 'step_ht'), ('a', 'ramp_angle'), ('S', 'step')], main.__doc__ + __doc__)
    
    cc = ChassisClearance(opts.chassis_len, opts.chassis_ht, opts.step_ht, opts.ramp_angle)
    
    print("ramp base: %5.2f\n" % cc.ramp_base_len)
    for fh, rh, tl, cl, ag in cc.get_clearance_profile():
        print("%5.2f: %5.2f" % (tl, cl))
    
    oss.exit(0)
        

#-------------------------------------------------------------------------------
class ChassisClearance(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, chass_len, chass_ht, step_ht, ramp_angle):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        
        self.chass_len = float(chass_len)
        self.chass_ht = float(chass_ht)
        self.step_ht = float(step_ht)
        self.ramp_angle = math.radians(float(ramp_angle))

        self.ramp_base_len = self.step_ht / math.tan(self.ramp_angle)
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get_traversal_angle(self, front_ht, rear_ht):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return traversal angle in rads 
        """
        return math.asin((front_ht - rear_ht) / self.chass_len)
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get_traversal_len(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.step_ht / math.tan(self.get_traversal_angle(self.chass_ht + self.step_ht, self.chass_ht))
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get_clearance(self, trav_len, front_ht, rear_ht):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return (math.tan(self.get_traversal_angle(front_ht, rear_ht)) * trav_len) - (self.step_ht - rear_ht)
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get_ht_off(self, ramp_base_off):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if ramp_base_off < 0:
            ramp_base_off = 0
        return math.tan(self.ramp_angle) * ramp_base_off

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get_clearance_profile(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        tl = self.get_traversal_len()
        a = []
        step = 1.0
        
        while tl > -step:
            if tl < 0:
                tl = 0
            fh = rh = self.chass_ht
            fh += self.step_ht
            
            if tl < self.ramp_base_len:
                rh += self.get_ht_off(self.ramp_base_len - tl)
                
            ag = self.get_traversal_angle(fh, rh)
            cl = self.get_clearance(tl, fh, rh)
                
            a.append((fh, rh, tl, cl, math.degrees(ag)))
            tl -= step
            
        return a

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __str__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return str(self.__dict__)
        

#-------------------------------------------------------------------------------
def sqr(a):
#-------------------------------------------------------------------------------
    return a * a
    
    
if __name__ == "__main__":
    main(oss.argv)
