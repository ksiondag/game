
def vy( y0, ymax, a ):
    if (ymax > y0 and a < 0) or (y0 > ymax and a > 0):
        return (-2*a*(ymax-y0))**(0.5)
    return 0.

def vy2( y0, yt, a, t ):
    return (yt - y0)/t - 0.5*a*t

def vx( x0, xt, t, max_velocity=0 ):
    if t != 0:
        velocity = (xt - x0)/t
    else:
        velocity = max_velocity if xt >= x0 else -max_velocity

    if max_velocity and abs(velocity) > max_velocity:
        if velocity > 0:
            velocity = max_velocity
        else:
            velocity = -max_velocity

    return velocity

def ty( y0, yt, v, a ):
    plus_or_minus = (v**2 + 2*a*(yt-y0))
    if plus_or_minus > 0:
        plus_or_minus = plus_or_minus**(0.5)
    else:
        plus_or_minus = 0
    potential_times = [(-v-plus_or_minus)/a,(-v+plus_or_minus)/a]
    potential_times = [ time for time in potential_times if time > 0 ]

    if len( potential_times ) == 0:
        return 0
    return min( potential_times )

def tx( x0, xt, v, time_y=0 ):
    if v == 0:
        return time_y

    t = (xt - x0)/v

    assert t >= 0, 'Time expectancy for travelling is less than zero.'

    return t

def position( p0, v, a, t ):
    return p0 + v*t + 0.5*a*t**2

def velocity( v0, a, t ):
    return v0 + a*t

