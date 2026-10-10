"""Figure 1: a (3, 2) PointCloudTensor drawn as a 3 x 2 block of glass cells.

Writes figures/pointcloud-tensor-3x2.svg
"""
import numpy as np, math
from clouds import cells
# Same projection as the barcode and Betti figures, so the three line up and the next
# tensor reads as this block grown one cell deeper.
S=150; K=0.62; A=math.radians(35)
NR,NC=3,2
ND_NEXT=2   # depth of the (3, 2, 2) tensors that follow; the viewBox leaves room for it
Z0=ND_NEXT-1   # sit in their back layer, so the next tensors grow a layer in front
ZC=0.0   # centre each cloud on its cell's front face (z=0), which reads as centred
def P0(x,y,z): return (x*S + z*K*S*math.cos(A), -y*S - z*K*S*math.sin(A))
def P(x,y,z): return P0(x,y,z+Z0)
def pts_str(ps): return ' '.join('%.1f,%.1f'%P(*p) for p in ps)
def poly(ps,cls): return '<polygon class="%s" points="%s"/>'%(cls,pts_str(ps))
def line(a,b,cls):
    a=P(*a); b=P(*b); return '<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(cls,*a,*b)
W_,H_=NC,NR   # block size in cube units: x in [0,2], y in [0,3], z in [0,1]
back=[]
back.append(poly([(0,0,1),(W_,0,1),(W_,H_,1),(0,H_,1)],'backwall'))
back.append(poly([(0,0,0),(W_,0,0),(W_,0,1),(0,0,1)],'floor'))
back.append(poly([(0,0,0),(0,0,1),(0,H_,1),(0,H_,0)],'leftwall'))
# hidden back edges (dashed): back-wall grid, left-back and floor-back edges
for x in range(0,W_+1): back.append(line((x,0,1),(x,H_,1),'edge-back'))
for y in range(0,H_+1): back.append(line((0,y,1),(W_,y,1),'edge-back'))
back.append(line((0,0,0),(0,0,1),'edge-back'))
for y in range(1,H_): back.append(line((0,y,0),(0,y,1),'edge-back'))
for x in range(1,W_): back.append(line((x,0,0),(x,0,1),'edge-back'))
# interior shared walls: depth lines from interior front grid points
for x in range(1,W_):
    for y in range(1,H_): back.append(line((x,y,0),(x,y,1),'edge-inner'))
# points of all cells, sorted far to near
allp=[]
for i in range(NR):
    for j in range(NC):
        cl,_=cells[i][j]
        cl=0.5+(cl-0.5)*np.array([0.74,0.74,0.62])
        # centre by projected 2D bounding box, so the cloud *looks* centred in its cell
        pr=np.array([P(*p) for p in cl]); bc=(pr.min(0)+pr.max(0))/2
        tgt=np.array(P(0.5,0.5,ZC))
        d=tgt-bc
        cl=cl+np.array([d[0]/S, -d[1]/S, 0.0])
        off=np.array([j, NR-1-i, 0.0])
        allp.append(cl+off)
allp=np.vstack(allp); order=np.argsort(-allp[:,2])
pts=[]
for k in order:
    x,y,z=allp[k]; px,py=P(x,y,z); t=1-z
    pts.append('<circle class="pt%s" cx="%.1f" cy="%.1f" r="%.2f"/>'%(' far' if t<0.45 else '',px,py,(2.0+2.0*t)*S/200))
front=[]
front.append(poly([(W_,0,0),(W_,0,1),(W_,H_,1),(W_,H_,0)],'face side'))
front.append(poly([(0,H_,0),(W_,H_,0),(W_,H_,1),(0,H_,1)],'face top'))
front.append(poly([(0,0,0),(W_,0,0),(W_,H_,0),(0,H_,0)],'face front'))
for x in range(0,W_+1): front.append(line((x,0,0),(x,H_,0),'edge'))
for y in range(0,H_+1): front.append(line((0,y,0),(W_,y,0),'edge'))
for x in range(0,W_+1): front.append(line((x,H_,0),(x,H_,1),'edge'))   # top face depth lines
front.append(line((0,H_,1),(W_,H_,1),'edge'))
for y in range(0,H_): front.append(line((W_,y,0),(W_,y,1),'edge'))     # right face depth lines
front.append(line((W_,0,1),(W_,H_,1),'edge'))
xs=[P0(x,y,z)[0] for x in (0,W_) for y in (0,H_) for z in (0,ND_NEXT)]
ys=[P0(x,y,z)[1] for x in (0,W_) for y in (0,H_) for z in (0,ND_NEXT)]
pad=12; x0,x1,y0,y1=min(xs)-pad,max(xs)+pad,min(ys)-pad,max(ys)+pad
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1-x0:.0f} {y1-y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" role="img" aria-labelledby="t d">
<title id="t">A StableBear PointCloudTensor of shape (3, 2)</title>
<desc id="d">A block of six glass cells in 3 rows and 2 columns. Each cell is one tensor element holding its own point cloud: a circle, a torus, a sphere, three clusters, a helix and uniform noise.</desc>
<style>
  svg {{ --sb-ink: var(--ink, #16110d); --sb-pt: var(--espresso, #3b2a20); --sb-glass: var(--fur, #d9c6b0); }}
  @media (prefers-color-scheme: dark) {{ svg {{ --sb-ink: var(--ink, #f0e9e0); --sb-pt: var(--espresso, #e8d5bf); --sb-glass: #8a7a68; }} }}
  .backwall {{ fill: var(--sb-glass); opacity: .16; }}
  .floor {{ fill: var(--sb-glass); opacity: .45; }}
  .leftwall {{ fill: var(--sb-glass); opacity: .10; }}
  .face {{ fill: var(--sb-glass); }} .front {{ opacity: .10; }} .side {{ opacity: .28; }} .top {{ opacity: .22; }}
  .edge {{ stroke: var(--sb-ink); stroke-width: 1.5; stroke-linejoin: round; stroke-linecap: round; opacity: .8; }}
  .edge-inner {{ stroke: var(--sb-ink); stroke-width: 1; opacity: .3; }}
  .edge-back {{ stroke: var(--sb-ink); stroke-width: 1; stroke-dasharray: 3 4; opacity: .3; }}
  .pt {{ fill: var(--sb-pt); opacity: .92; }} .pt.far {{ opacity: .42; }}
</style>
{chr(10).join(back)}
{chr(10).join(pts)}
{chr(10).join(front)}
</svg>"""
open('figures/pointcloud-tensor-3x2.svg','w').write(svg)
print(round(x1-x0),round(y1-y0))
