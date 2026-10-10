"""The six example point clouds shared by all three figures.

Each cloud lives in the unit cube [0, 1]^3. A fixed seed makes every run identical.
"""
import numpy as np, math
rng=np.random.default_rng(7)
def ring(n):
    t=rng.uniform(0,2*np.pi,n); r=0.36+rng.normal(0,0.022,n)
    return np.c_[0.5+r*np.cos(t),0.5+r*np.sin(t),0.5+rng.normal(0,0.03,n)]
def torus(n):
    u=rng.uniform(0,2*np.pi,n); v=rng.uniform(0,2*np.pi,n); R,r=0.27,0.11
    return np.c_[0.5+(R+r*np.cos(v))*np.cos(u),0.5+r*np.sin(v),0.5+(R+r*np.cos(v))*np.sin(u)]
def sphere(n):
    p=rng.normal(size=(n,3)); p/=np.linalg.norm(p,axis=1,keepdims=True); return 0.5+0.35*p+rng.normal(0,0.01,(n,3))
def blobs(n):
    c=np.array([[0.28,0.3,0.35],[0.72,0.68,0.6],[0.7,0.28,0.72]]); k=rng.integers(0,3,n)
    return np.clip(c[k]+rng.normal(0,0.065,(n,3)),0.05,0.95)
def helix(n):
    t=rng.uniform(0,1,n); a=t*4*np.pi
    return np.c_[0.5+0.3*np.cos(a),0.08+0.84*t,0.5+0.3*np.sin(a)]+rng.normal(0,0.012,(n,3))
def tilt(p,ax,deg):
    t=np.radians(deg); c,s_=np.cos(t),np.sin(t); q=p-0.5
    if ax=='x': R=np.array([[1,0,0],[0,c,-s_],[0,s_,c]])
    else: R=np.array([[c,0,s_],[0,1,0],[-s_,0,c]])
    return q@R.T+0.5
def uniform(n): return rng.uniform(0.08,0.92,(n,3))
# cells[i][j] = (points, name); the layout is the (3, 2) tensor shape
cells=[[(tilt(ring(140),'y',38),'circle'),(tilt(torus(260),'x',-28),'torus')],
       [(sphere(220),'sphere'),(blobs(150),'three clusters')],
       [(helix(160),'helix'),(uniform(60),'uniform noise')]]

