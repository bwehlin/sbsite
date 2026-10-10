"""Figure 2: the (3, 2, 2) BarcodeTensor from persistent homology of the point clouds.

H1 barcodes in the front layer, H0 (16 longest bars) behind.
  python fig_barcodes.py           -> figures/barcode-tensor-3x2x2.svg       (flat bars)
  python fig_barcodes.py --boxes   -> figures/barcode-tensor-3x2x2-boxes.svg (3D boxes)
Needs data/barcodes.json from compute.py.
"""
import json, math, sys, numpy as np
bars=json.load(open('data/barcodes.json'))
BOX='--boxes' in sys.argv   # draw each bar as a 3D box (depth = bar height)
S=150; K=0.62; A=math.radians(35)
NR,NC,ND=3,2,2
def P(x,y,z): return (x*S + z*K*S*math.cos(A), -y*S - z*K*S*math.sin(A))
def pts(ps): return ' '.join('%.1f,%.1f'%P(*p) for p in ps)
def poly(ps,cls): return '<polygon class="%s" points="%s"/>'%(cls,pts(ps))
def line(a,b,cls):
    a=P(*a); b=P(*b); return '<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(cls,*a,*b)
W_,H_,D_=NC,NR,ND
MAX_BARS={0:16,1:6}   # bars shown per cell, by homology degree
def barcode(i,j,k):
    """Barcode of cell (i,j), homology degree k, drawn on its cell's mid-plane (H1 in front, H0 behind)."""
    a=np.array(bars[f'{i}{j}{k}'])                     # rows (birth, death); death may be inf
    inf=~np.isfinite(a[:,1]); L=np.where(inf,np.inf,a[:,1]-a[:,0])
    order=np.argsort(-L)                                # longest (and infinite) bars first
    if k==0:
        keep=list(order)[:MAX_BARS[0]]                  # H0: just the longest bars
    else:
        Lmax=L[np.isfinite(L)].max() if np.isfinite(L).any() else 1
        # H1: drop tiny noise bars (< 10% of the longest), but always keep at least three
        keep=[o for r,o in enumerate(order) if r<3 or L[o]>=0.1*Lmax][:MAX_BARS[1]]
    a=a[keep]
    fin=a[np.isfinite(a[:,1])]
    tm=(fin[:,1].max() if len(fin) else 1.0)*1.12
    a=a[np.lexsort((-(np.where(np.isfinite(a[:,1]),a[:,1],1e9)-a[:,0]),a[:,0]))]   # by birth, then longest first
    x0,y0,z=j, NR-1-i, (1.5 if k==0 else 0.5)
    m=0.2; w=0.48; hgt=0.6;   # left margin, bar-length span, stack height (cell units)
    n=min(MAX_BARS[k],len(a)) if k==0 else MAX_BARS[k]; step=hgt/n; th=step*(0.6 if k==0 else (0.46 if BOX else 0.62))
    out=[]
    rects=[]
    for r,(b,d) in enumerate(a):
        tb=b/tm; td=1.0 if not np.isfinite(d) else min(d/tm,1.0)
        xl=x0+m+w*tb; xr=x0+m+w*td
        if xr-xl<0.012: xr=xl+0.012
        yt=y0+1-m-r*step-(step-th)/2; yb=yt-th
        rects.append((xl,xr,yb,yt,'bar h%d%s'%(k,' inf' if not np.isfinite(d) else '')))
    # centre the drawn barcode in its cell (both directions)
    bx0=min(r[0] for r in rects); bx1=max(r[1] for r in rects)
    by0=min(r[2] for r in rects); by1=max(r[3] for r in rects)
    dx=(x0+0.5)-(bx0+bx1)/2; dy=(y0+0.5)-(by0+by1)/2
    # visual centring: put the barcode on the middle of its cell's front face, as with the point clouds
    dz=z-math.floor(z); dx-=dz*K*math.cos(A); dy-=dz*K*math.sin(A)
    # draw from the top bar down so each box's top face sits in the gap above it
    for xl,xr,yb,yt,cls in rects:
        xl+=dx; xr+=dx; yb+=dy; yt+=dy
        if not BOX:
            out.append(poly([(xl,yb,z),(xr,yb,z),(xr,yt,z),(xl,yt,z)],cls)); continue
        t=yt-yb; zf=z-t/2; zb=z+t/2          # depth equals bar height
        out.append(poly([(xl,yt,zf),(xr,yt,zf),(xr,yt,zb),(xl,yt,zb)],cls+' btop'))
        out.append(poly([(xl,yt,zf),(xr,yt,zf),(xr,yt,zb),(xl,yt,zb)],'hilite'))
        out.append(poly([(xr,yb,zf),(xr,yb,zb),(xr,yt,zb),(xr,yt,zf)],cls+' bside'))
        out.append(poly([(xr,yb,zf),(xr,yb,zb),(xr,yt,zb),(xr,yt,zf)],'shade'))
        out.append(poly([(xl,yb,zf),(xr,yb,zf),(xr,yt,zf),(xl,yt,zf)],cls+' bfront'))
    return out
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
    for j in range(NC): layer_h0+=barcode(i,j,0)
mid=[poly([(0,0,1),(W_,0,1),(W_,H_,1),(0,H_,1)],'midwall')]
for x in range(1,W_):
    for y in range(1,H_): mid.append(line((x,y,0),(x,y,D_),'edge-inner'))
for x in range(1,W_): mid.append(line((x,0,1),(x,H_,1),'edge-inner'))
for y in range(1,H_): mid.append(line((0,y,1),(W_,y,1),'edge-inner'))
layer_h1=[]
for i in range(NR):
    for j in range(NC): layer_h1+=barcode(i,j,1)
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
<title id="t">A StableBear BarcodeTensor of shape (3, 2, 2)</title>
<desc id="d">A block of glass cells, 3 rows by 2 columns by 2 deep. Each cell holds one persistence barcode. The front layer holds the H1 barcodes and the back layer the H0 barcodes of six point clouds: a circle, a torus, a sphere, three clusters, a helix and uniform noise.</desc>
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
  .bar {{ stroke: none; }}
  .h0 {{ fill: var(--sb-h0); }} .layer-h0 {{ opacity: .7; }}
  .h1 {{ fill: var(--sb-h1); }} .layer-h1 {{ opacity: .95; }}
  .hilite {{ fill: #fff; opacity: .35; }}
  .shade {{ fill: #000; opacity: .22; }}
</style>
{chr(10).join(back)}
<g class="layer-h0">{chr(10).join(layer_h0)}</g>
{chr(10).join(mid)}
<g class="layer-h1">{chr(10).join(layer_h1)}</g>
{chr(10).join(front)}
</svg>"""
open('figures/barcode-tensor-3x2x2%s.svg'%('-boxes' if BOX else ''),'w').write(svg)
print(round(x1-x0),round(y1-y0))
