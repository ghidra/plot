#https://github.com/caseman/noise/tree/master/examples
import noise #this is a module that needs to be installed. "python -m pip install noise"
import v

#expects a vector2
def snoise2( p ):
	return v.vector2(noise.snoise2(p.x,p.x-1.1), noise.snoise2(p.y - 19.1, p.x + 33.4))

#expects a vector3
def snoise3( p ):
	return v.vector3(noise.snoise3(p.x,p.x-1.1,p.x-2.2), noise.snoise3(p.y - 19.1, p.z + 33.4, p.x + 47.2), noise.snoise3(p.z + 74.2, p.x - 124.5, p.y + 99.4));

def curl2( p ):

	e = .1;
	dx = v.vector(e, 0.0)
	dy = v.vector2(0.0, e)
	p_x0 = snoise2(p - dx)
	p_x1 = snoise2(p + dx)
	p_y0 = snoise2(p - dy)
	p_y1 = snoise2(p + dy)

	x = p_z1.y + p_z0.y
	y = p_z1.x - p_z0.x

	divisor = 1.0 / (2.0 * e)
	return v.vector2.normalized(v.vector2(x, y) * divisor)

def curl3( p ):

	e = .1;
	dx = v.vector3(e, 0.0, 0.0)
	dy = v.vector3(0.0, e, 0.0)
	dz = v.vector3(0.0, 0.0, e)
	p_x0 = snoise3(p - dx)
	p_x1 = snoise3(p + dx)
	p_y0 = snoise3(p - dy)
	p_y1 = snoise3(p + dy)
	p_z0 = snoise3(p - dz)
	p_z1 = snoise3(p + dz)

	x = p_y1.z - p_y0.z - p_z1.y + p_z0.y
	y = p_z1.x - p_z0.x - p_x1.z + p_x0.z
	z = p_x1.y - p_x0.y - p_y1.x + p_y0.x

	divisor = 1.0 / (2.0 * e)
	return v.vector3.normalized(v.vector3(x, y, z) * divisor)


#requires 3d position
def sinusoidal2( pos, time, amp, speed, freq ):

	# Higher frequency wiggle
	displacement = v.vector2( 0, 0 );
	offset = time * speed + ( pos.x * freq + pos.z * freq );
	displacement.x += math.sin( offset ) * ( amp * 0.25 * pos.y );
	displacement.y += math.cos( offset ) * ( amp * 0.25 * pos.y );
	# Lower frequency long wind movement
	offset = time * speed + ( pos.x * freq + pos.z * freq )
	displacement.x += math.sin( offset ) * ( amp * pos.y )
	displacement.y += math.cos( offset ) * ( amp * pos.y ) * 0.5
	return displacement



