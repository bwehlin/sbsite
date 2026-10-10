"""Figure 3: the (3, 2, 2) PcfTensor of Betti curves computed from the barcodes.

H1 Betti curves in front, H0 behind, each drawn as a step line.
Writes figures/betti-tensor-3x2x2.svg. Needs data/betti_curves.json from compute.py.
"""
import json, math, numpy as np
S=150; K=0.62; A=math.radians(35)
NR,NC,ND=3,2,2
def P(x,y,z): return (x*S + z*K*S*math.cos(A), -y*S - z*K*S*math.sin(A))
def pts(ps): return ' '.join('%.1f,%.1f'%P(*p) for p in ps)
def poly(ps,cls): return '<polygon class="%s" points="%s"/>'%(cls,pts(ps))
def line(a,b,cls):
    a=P(*a); b=P(*b); return '<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(cls,*a,*b)
W_,H_,D_=NC,NR,ND
betti=json.load(open('data/betti_curves.json'))
def betti_curve(i,j,k):
    """Betti curve of cell (i,j), homology degree k, drawn as a step line on its cell's mid-plane."""
    pc=np.array(betti[f'{i}{j}{k}'])   # rows (t, value): value holds from t to the next t
    t=pc[:,0]; v=pc[:,1]
    tend = t[-1]*1.15 if k==0 else t[-1]*1.04
    vmax=v.max()
    x0,y0,z=j, NR-1-i, (1.5 if k==0 else 0.5)
    w=0.56; hgt=0.5
    xs=np.append(t,tend)/tend*w; ys=v/vmax*hgt
    # centring (same rule as the barcodes): centre of the visible curve -> centre of the cell's front face
    nz=np.nonzero(v>0)[0]; cx0=xs[nz[0]]; cx1=xs[nz[-1]+1]
    dx=(x0+0.5)-(x0+(cx0+cx1)/2); dy=(y0+0.5)-(y0+hgt/2)
    dz=z-math.floor(z); dx-=dz*K*math.cos(A); dy-=dz*K*math.sin(A)
    ox,oy=x0+dx, y0+dy
    lw=0.018 if k==1 else 0.013          # line width, in cell units
    n=len(v)
    steps=[]
    for r in range(n):
        steps+=[(ox+xs[r],oy+ys[r]),(ox+xs[r+1],oy+ys[r])]
    def path(zz):
        q=[P(px,py,zz) for px,py in steps]
        return 'M'+' L'.join('%.1f %.1f'%c for c in q)
    return ['<path class="curve h%d" stroke-width="%.2f" d="%s"/>'%(k,lw*S,path(z))]
back=[]
back.append(poly([(0,0,D_),(W_,0,D_),(W_,H_,D_),(0,H_,D_)],'backwall'))
back.append(poly([(0,0,0),(W_,0,0),(W_,0,D_),(0,0,D_)],'floor'))
back.append(poly([(0,0,0),(0,0,D_),(0,H_,D_),(0,H_,0)],'leftwall'))
for x in range(W_+1): back.append(line((x,0,D_),(x,H_,D_),'edge-back'))
for y in range(H_+1): back.append(line((0,y,D_),(W_,y,D_),'edge-back'))
for z in range(D_): back.append(line((0,0,z),(0,0,z+1),'edge-back'))
for y in range(1,H_):
    back.append(line((0,y,0),(0,y,D_),'edge-back'))
for x in range(1,W_): back.append(line((x,0,0),(x,0,D_),'edge-back'))
for z in range(1,D_):
    back.append(line((0,0,z),(W_,0,z),'edge-back')); back.append(line((0,0,z),(0,H_,z),'edge-back'))
# back layer (H0), then the shared middle wall, then the front layer (H1)
layer_h0=[]
for i in range(NR):
    for j in range(NC): layer_h0+=betti_curve(i,j,0)
mid=[poly([(0,0,1),(W_,0,1),(W_,H_,1),(0,H_,1)],'midwall')]
for x in range(1,W_):
    for y in range(1,H_): mid.append(line((x,y,0),(x,y,D_),'edge-inner'))
for x in range(1,W_): mid.append(line((x,0,1),(x,H_,1),'edge-inner'))
for y in range(1,H_): mid.append(line((0,y,1),(W_,y,1),'edge-inner'))
layer_h1=[]
for i in range(NR):
    for j in range(NC): layer_h1+=betti_curve(i,j,1)
front=[]
front.append(poly([(W_,0,0),(W_,0,D_),(W_,H_,D_),(W_,H_,0)],'face side'))
front.append(poly([(0,H_,0),(W_,H_,0),(W_,H_,D_),(0,H_,D_)],'face top'))
front.append(poly([(0,0,0),(W_,0,0),(W_,H_,0),(0,H_,0)],'face front'))
for x in range(W_+1): front.append(line((x,0,0),(x,H_,0),'edge'))
for y in range(H_+1): front.append(line((0,y,0),(W_,y,0),'edge'))
for x in range(W_+1): front.append(line((x,H_,0),(x,H_,D_),'edge'))
for z in range(1,D_+1): front.append(line((0,H_,z),(W_,H_,z),'edge'))
for y in range(H_): front.append(line((W_,y,0),(W_,y,D_),'edge'))
for z in range(1,D_+1): front.append(line((W_,0,z),(W_,H_,z),'edge'))
xs=[P(x,y,z)[0] for x in (0,W_) for y in (0,H_) for z in (0,D_)]
ys=[P(x,y,z)[1] for x in (0,W_) for y in (0,H_) for z in (0,D_)]
pad=12; x0,x1,y0,y1=min(xs)-pad,max(xs)+pad,min(ys)-pad,max(ys)+pad
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1-x0:.0f} {y1-y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" role="img" aria-labelledby="t d">
<title id="t">A StableBear PcfTensor of Betti curves, shape (3, 2, 2)</title>
<desc id="d">A block of glass cells, 3 rows by 2 columns by 2 deep. Each cell holds one Betti curve, a step function drawn as a line. The front layer holds the H1 Betti curves and the back layer the H0 Betti curves of six point clouds: a circle, a torus, a sphere, three clusters, a helix and uniform noise.</desc>
<style>
  svg {{ --sb-ink: var(--ink, #16110d); --sb-h1: var(--espresso, #3b2a20); --sb-h0: var(--honey, #d9a441); --sb-glass: var(--fur, #d9c6b0); }}
  @media (prefers-color-scheme: dark) {{ svg {{ --sb-ink: var(--ink, #f0e9e0); --sb-h1: var(--espresso, #e8d5bf); --sb-h0: var(--honey, #e5b45a); --sb-glass: #8a7a68; }} }}
  .backwall {{ fill: var(--sb-glass); opacity: .16; }}
  .floor {{ fill: var(--sb-glass); opacity: .42; }}
  .leftwall {{ fill: var(--sb-glass); opacity: .10; }}
  .midwall {{ fill: var(--sb-glass); opacity: .10; }}
  .face {{ fill: var(--sb-glass); }} .front {{ opacity: .10; }} .side {{ opacity: .28; }} .top {{ opacity: .22; }}
  .edge {{ stroke: var(--sb-ink); stroke-width: 1.5; stroke-linejoin: round; stroke-linecap: round; opacity: .8; }}
  .edge-inner {{ stroke: var(--sb-ink); stroke-width: 1; opacity: .28; }}
  .edge-back {{ stroke: var(--sb-ink); stroke-width: 1; stroke-dasharray: 3 4; opacity: .28; }}
  .curve {{ fill: none; stroke-linejoin: miter; stroke-miterlimit: 4; stroke-linecap: square; }}
  .curve.h0 {{ stroke: var(--sb-h0); }} .layer-h0 {{ opacity: .7; }}
  .curve.h1 {{ stroke: var(--sb-h1); }} .layer-h1 {{ opacity: .95; }}
</style>
{chr(10).join(back)}
<g class="layer-h0">{chr(10).join(layer_h0)}</g>
{chr(10).join(mid)}
<g class="layer-h1">{chr(10).join(layer_h1)}</g>
{chr(10).join(front)}
</svg>"""
open('figures/betti-tensor-3x2x2.svg','w').write(svg)
print(round(x1-x0),round(y1-y0))
