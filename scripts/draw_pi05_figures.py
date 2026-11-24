"""Regenerate pi05 figures from packaged evidence without models, simulators or GPUs."""
from pathlib import Path
import csv, json, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/figure/results'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.titleweight':'bold',
 'axes.labelcolor':'#4b5563','text.color':'#252a31','xtick.color':'#626973','ytick.color':'#626973',
 'axes.edgecolor':'#cbd0d7','axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,
 'svg.fonttype':'none','savefig.facecolor':'white'})
# Match the released RoboSeed method figures (e.g. 13_openwam_experiments.png).
BLUE='#0066cc'; DARK=BLUE; LIGHT='#79a9cf'; GRAY='#6b7280'; GRID='#e5e7eb'

def save(fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for ax in fig.axes:
        legend = ax.get_legend()
        if legend is not None:
            bounds = legend.get_window_extent(renderer)
            if any(bounds.overlaps(other.get_window_extent(renderer)) for other in fig.axes):
                raise ValueError(f'{name}: legend overlaps a plotting area')
            if bounds.overlaps(ax.xaxis.label.get_window_extent(renderer)):
                raise ValueError(f'{name}: legend overlaps the x-axis label')
    for ext in ('pdf','svg','png'):
        fig.savefig(OUT/f'{name}.{ext}',dpi=220,bbox_inches='tight',pad_inches=.14)
    svg=OUT/f'{name}.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)

def box(ax, xy, wh, title, detail, color='#edf4fa'):
    x,y=xy; w,h=wh
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.018,rounding_size=.025',
                 linewidth=.8,edgecolor='#96b4cf',facecolor=color))
    ax.text(x+w/2,y+h*.70,title,ha='center',va='center',weight='bold',fontsize=10)
    ax.text(x+w/2,y+h*.32,detail,ha='center',va='center',fontsize=8,color='#52606e',linespacing=1.4)

def arrow(ax,a,b):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,lw=1.4,color=DARK))

fig,ax=plt.subplots(figsize=(12.2,3.5)); ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
box(ax,(.02,.60),(.17,.26),'Three camera views','Head + left / right wrist\nRoboTwin RGB observations')
box(ax,(.02,.15),(.17,.26),'Robot state + language','14-D state; task instruction')
box(ax,(.26,.60),(.19,.26),'SigLIP','Shared image encoder')
box(ax,(.51,.60),(.19,.26),'PaliGemma','Gemma 2B context backbone')
box(ax,(.51,.15),(.19,.26),'Action expert','Gemma 300M + flow matching\nconditioned on action noise')
box(ax,(.77,.15),(.20,.26),'Action chunk','50 × 32 internal action\n50 × 14 physical action')
arrow(ax,(.19,.73),(.26,.73)); arrow(ax,(.45,.73),(.51,.73)); arrow(ax,(.19,.28),(.51,.60)); arrow(ax,(.605,.60),(.605,.41)); arrow(ax,(.70,.28),(.77,.28))
ax.text(.02,.02,'Local RoboTwin adaptation: full π0.5-base initialization; one 50-task policy.',fontsize=8,color=GRAY)
save(fig,'18_pi05_architecture')

jobs=json.loads((ROOT/'data/pi05/robotwin_retry_audit.json').read_text())['jobs']
with (ROOT/'data/pi05/robotwin_loss.csv').open() as f:
    loss=[(int(r['step']),float(r['loss'])) for r in csv.DictReader(f)]
with (ROOT/'data/pi05/libero_suite_results.csv').open() as f:
    lib={r['suite']:{'success_rate':float(r['local_success_rate_pct'])/100} for r in csv.DictReader(f)}
assert len(loss)==29548 and loss[-1][0]==295470

fig,axes=plt.subplots(2,2,figsize=(12,7.8)); ax=axes[0,0]
xs=np.arange(2); vals=[73.04,71.88]; bars=ax.bar(xs,vals,color=[LIGHT,BLUE],width=.55)
for x,y in zip(xs,vals): ax.text(x,y+2,f'{y:.2f}%\n{int(y*50):,}/5,000',ha='center',fontsize=8)
ax.set_xticks(xs,['Clean','Randomized']);ax.set_ylim(0,110);ax.set_ylabel('Success rate (%)');ax.set_title('(a) RoboTwin: local 50-task checkpoint',loc='left');ax.grid(axis='y',color=GRID,lw=.6);ax.set_axisbelow(True)
ax=axes[0,1]; x=np.array([v[0] for v in loss]); y=np.array([v[1] for v in loss]); window=200
sm=np.convolve(y,np.ones(window)/window,mode='valid');ax.plot(x[::40]/1000,y[::40],color=LIGHT,alpha=.55,lw=.6,label='Raw, every 40th record'); ax.plot(x[window-1:]/1000,sm,color=DARK,lw=1.3,label='200-observation mean')
ax.set_yscale('log');ax.set_ylim(1e-4,.2);ax.set_xlabel('Recorded updates (thousands)');ax.set_ylabel('Native flow-matching loss');ax.set_title('(b) Local RoboTwin training',loc='left');ax.grid(axis='y',color=GRID,lw=.6);ax.legend(frameon=False,fontsize=7)
ax=axes[1,0]; weak=sorted((v['successes'],k.split('/')[1]) for k,v in jobs.items() if k.startswith('demo_clean/'))[:6]; yloc=np.arange(6); labels=[t.replace('_',' ') for _,t in weak]; c=[v for v,t in weak]; r=[jobs['demo_randomized/'+t]['successes'] for _,t in weak]
ax.barh(yloc-.18,c,.36,color=LIGHT,label='Clean');ax.barh(yloc+.18,r,.36,color=BLUE,label='Randomized');ax.set_yticks(yloc,labels);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Successes / 100 per scene');ax.set_title('(c) Six weakest local Clean tasks',loc='left');ax.grid(axis='x',color=GRID,lw=.6);ax.set_axisbelow(True);ax.legend(frameon=False,fontsize=7,loc='lower right')
for i,(a,b) in enumerate(zip(c,r)): ax.text(a+1,i-.18,str(a),va='center',fontsize=7);ax.text(b+1,i+.18,str(b),va='center',fontsize=7)
ax=axes[1,1]; s=['libero_spatial','libero_object','libero_goal','libero_10']; ref=[98.8,98.2,98,92.4]; local=[100*lib[k]['success_rate'] for k in s];xx=np.arange(4)
ax.bar(xx-.17,ref,.34,color=LIGHT,label='Official reported');ax.bar(xx+.17,local,.34,color=BLUE,label='Our official-weight evaluation')
for x0,y0 in zip(xx-.17,ref):ax.text(x0,y0+1,f'{y0:.1f}',ha='center',fontsize=7)
for x0,y0 in zip(xx+.17,local):ax.text(x0,y0+1,f'{y0:.1f}',ha='center',fontsize=7)
ax.set_xticks(xx,['Spatial','Object','Goal','Long']);ax.set_ylim(0,112);ax.set_ylabel('Success rate (%)');ax.set_title('(d) LIBERO: released checkpoint only',loc='left');ax.grid(axis='y',color=GRID,lw=.6);ax.set_axisbelow(True);ax.legend(frameon=False,fontsize=7,loc='lower left')
for ax in (axes[0,1], axes[1,0], axes[1,1]):
    ax.get_legend().remove()
    ax.legend(loc='upper center', bbox_to_anchor=(.5,-.22), ncol=1 if ax is axes[1,1] else 2,
              frameon=False, fontsize=8, handlelength=1.8, columnspacing=1.4,
              borderaxespad=0)
fig.tight_layout(h_pad=4.0,w_pad=2.5);save(fig,'19_pi05_experiments')
print('Generated pi05 Git figure companions from packaged evidence; the authoritative article figures are maintained separately.')
