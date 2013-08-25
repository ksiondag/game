from sys import maxsize

import constants as c

def vp_max( p0, pmax, a ):
    if (pmax > p0 and a < 0) or (p0 > pmax and a > 0):
        return (-2*a*(pmax-p0))**(0.5)
    return 0.

def vp( p0, pt, a, t ):
    if t == 0:
        if pt - p0 == 0:
            return 0
        elif pt - p0 > 0:
            return maxsize
        elif pt - p0 < 0:
            return -maxsize
    return (pt - p0)/t - 0.5*a*t

def tp( p0, pt, v, a ):

    if a == 0:
        if v == 0:
            if pt == p0:
                return 0
            else:
                return sys.maxsize
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

def vxy( x0, xt, ax, y0, yt, ay, max_vx=c.MAX_VELOCITY ):
    # Find y velocity, time
    vy = vp_max( y0, yt, ay )
    ty = tp( y0, yt, vy, ay )

    # Find x velocity, time
    vx = vp( x0, xt, ax, ty )

    # Correct y velocity to land on target y at time x
    if abs(vx) > max_vx:
        if vx > 0:
            vx = max_vx
        else:
            vx = -max_vx
        tx = tp( x0, xt, vx, ax )
        vy = vp( y0, yt, ay, tx )

    return vx, vy

