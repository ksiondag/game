import constants as c

def vp_max( p0, pmax, a ):
    if (pmax > p0 and a < 0) or (p0 > pmax and a > 0):
        return (-2*a*(pmax-p0))**(0.5)
    return 0.

def vp( p0, pt, a, t, max_velocity=c.MAX_VELOCITY ):
    if t == 0:
        if pt - p0 == 0:
            return 0
        elif pt - p0 > 0:
            return max_velocity + 1
        elif pt - p0 < 0:
            return -max_velocity - 1
    return (pt - p0)/t - 0.5*a*t

def tp( p0, pt, v, a ):

    if a == 0:
        if v == 0:
            return 0
        return (pt - p0)/v

    plus_or_minus = (v**2 + 2*a*(pt-p0))
    if plus_or_minus > 0:
        plus_or_minus = plus_or_minus**(0.5)
    else:
        plus_or_minus = 0
    potential_times = [(-v-plus_or_minus)/a,(-v+plus_or_minus)/a]
    potential_times = [ time for time in potential_times if time > 0 ]

    if len( potential_times ) == 0:
        return 0
    return min( potential_times )

def position( p0, v, a, t ):
    return p0 + v*t + 0.5*a*t**2

def velocity( v0, a, t ):
    return v0 + a*t

