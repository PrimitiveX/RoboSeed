"""Reproducible vector figures: blue / black / white / gray only."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];F=R/'docs'/'figure'/'results';F.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'axes.titleweight':'bold','axes.labelcolor':'#4b5563','text.color':'#252a31','xtick.color':'#626973','ytick.color':'#626973','axes.edgecolor':'#cbd0d7','axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
BLUE=['#a8c9e6','#679ed0','#1c64a4','#103f71','#526b80','#8c939c'];LIGHT='#edf4fa';GRAY='#6b7280'
def read(n):return list(csv.DictReader((R/'data'/n).open()))
def outside_legend(ax, ncol=1, fontsize=8):
 legend=ax.legend(loc='lower left',bbox_to_anchor=(0,1.015),borderaxespad=0,
                  frameon=False,ncol=ncol,fontsize=fontsize,handlelength=1.8,columnspacing=1.3)
 title=ax.get_title(loc='left');size=ax._left_title.get_fontsize()
 ax.set_title(title,loc='left',fontsize=size,pad=35)
 legend._outside_plot=True
 return legend
def save(fig,n):
 fig.canvas.draw()
 renderer=fig.canvas.get_renderer()
 for ax in fig.axes:
  legend=ax.get_legend()
  if legend is not None and getattr(legend,'_outside_plot',False):
   if legend.get_window_extent(renderer).overlaps(ax.get_window_extent(renderer)):
    raise ValueError(f'{n}: legend intersects plotting area')
 fig.savefig(F/(n+'.pdf'),bbox_inches='tight',pad_inches=.14)
 fig.savefig(F/(n+'.svg'),bbox_inches='tight',pad_inches=.14)
 fig.savefig(F/(n+'.png'),dpi=220,bbox_inches='tight',pad_inches=.14);plt.close(fig)
def grid(ax):ax.set_axisbelow(True);ax.grid(axis='y',color='#e5e7eb',lw=.6)
from diagram_layout import project_diagram, architecture_diagram
save(project_diagram(), '01_project')
save(architecture_diagram(), '02_architecture')
S=read('robotwin_summary.csv');names=[x['backbone'] for x in S];short=[x.replace('Qwen3-VL-','Q3-VL\n').replace('Qwen3.5-','Q3.5\n') for x in names];av=np.array([float(x['avg_pct']) for x in S])
# Capacity and cost side by side; zero-based bars prevent visual exaggeration.
fig,axes=plt.subplots(1,2,figsize=(11.8,3.9),gridspec_kw={'width_ratios':[1.4,1]})
a=axes[0];xx=np.arange(len(S));w=.25
for off,key,label,col in [(-w,'clean_pct','Clean',BLUE[0]),(0,'randomized_pct','Randomized',BLUE[1]),(w,'avg_pct','Average',BLUE[3])]:
 vals=[float(x[key]) for x in S];a.bar(xx+off,vals,w,color=col,label=label)
 for x,y in zip(xx+off,vals):a.text(x,y+1,f'{y:.2f}',ha='center',fontsize=7.5,rotation=90)
a.set_ylim(0,104);a.set_xticks(xx,short);a.set_ylabel('Success rate (%)');a.set_title('(a) RoboTwin: 50 tasks × 100 episodes / scene',loc='left');grid(a);outside_legend(a,ncol=3)
a=axes[1];hours=[float(x['gpu_hours']) for x in S];a.bar(xx,hours,color=BLUE[:len(S)])
for x,y in zip(xx,hours):a.text(x,y+6,f'{y:.1f}',ha='center',fontsize=9)
a.set_ylim(0,max(hours)*1.16);a.set_xticks(xx,short);a.set_ylabel('Training GPU-hours (4 × H200)');a.set_title('(b) Fixed 150k steps; global batch 64',loc='left');grid(a)
axes[1].set_title(axes[1].get_title(loc='left'),loc='left',pad=35)
fig.tight_layout(w_pad=2);save(fig,'03_scale_cost')
# Resources and rollout time show observed implementation conditions.
fig,axes=plt.subplots(1,3,figsize=(12.3,3.25))
for a,key,label,title in zip(axes,['avg_gpu_mem_gib','samples_per_s','clean_eval_hours'],['Recorded mean memory / GPU (GiB)','Training throughput (samples/s)','Rollout wall time (hours)'],['(a) Training memory','(b) End-to-end training throughput','(c) RoboTwin rollout time']):
 if key!='clean_eval_hours':
  vals=[float(x[key]) for x in S];a.bar(xx,vals,color=BLUE[:len(S)])
  for x,y in zip(xx,vals):a.text(x,y+max(vals)*.03,f'{y:.1f}',ha='center',fontsize=9)
  a.set_ylim(0,max(vals)*1.24)
 else:
  for off,k,l,c in [(-.17,'clean_eval_hours','Clean',BLUE[0]),(.17,'randomized_eval_hours','Randomized',BLUE[3])]:a.bar(xx+off,[float(x[k]) for x in S],.34,label=l,color=c)
  a.set_ylim(0,13.5)
 a.set_xticks(xx,short);a.set_ylabel(label,fontsize=9);a.set_title(title,loc='left',fontsize=10);grid(a)
outside_legend(axes[2],ncol=2)
for a in axes[:2]:a.set_title(a.get_title(loc='left'),loc='left',fontsize=10,pad=35)
fig.tight_layout(w_pad=1.7);save(fig,'04_resources_rollout')
# One panel per backbone; matching axes and explicit tail statistics.
from loss_panels import training_loss_panels
save(training_loss_panels(read('robotwin_loss.csv'), S,
                          read('robotwin_training_only.csv')), '05_training_loss')
# Task-level heterogeneity, selected controlled task group; full table in appendix.
T=read('robotwin_tasks.csv');selected=['click_alarmclock','click_bell','hanging_mug','blocks_ranking_size','move_stapler_pad','handover_block','open_microwave','pick_dual_bottles','stack_blocks_three','stack_bowls_three','grab_roller','place_empty_cup']
lookup={(r['backbone'],r['suite'],r['task']):float(r['success_rate_pct']) for r in T}
fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),sharey=True)
for a,suite in zip(axes,['Clean','Randomized']):
 mat=np.array([[lookup[n,suite,t] for n in names] for t in selected]);im=a.imshow(mat,cmap='Blues',vmin=0,vmax=100,aspect='auto')
 for y in range(len(selected)):
  for x in range(len(names)):a.text(x,y,f'{mat[y,x]:.0f}',ha='center',va='center',fontsize=9,color='white' if mat[y,x]>60 else '#252a31')
 a.set_xticks(range(len(names)),short);a.set_yticks(range(len(selected)),selected);a.set_title(suite,loc='left');a.tick_params(length=0);a.spines[['left','bottom']].set_visible(False)
fig.tight_layout(w_pad=2);fig.colorbar(im,ax=axes,shrink=.75,pad=.02,label='Success rate (%)');save(fig,'06_task_profiles')
# LIBERO and LIBERO-plus paired by suite, not pooled due to different denominators.
lib=read('libero_tasks.csv');lp=read('liberoplus_suite.csv');cat=read('liberoplus_category.csv');suites=['libero_spatial','libero_object','libero_goal','libero_10'];xx=np.arange(4)
fig,axes=plt.subplots(1,2,figsize=(12,3.8),gridspec_kw={'width_ratios':[1,1.2]});a=axes[0]
for off,label,vals,col in [(-.18,'LIBERO',[sum(int(x['success']) for x in lib if x['suite']==s)/5 for s in suites],BLUE[0]),(.18,'LIBERO-plus',[float(next(x['success_rate_pct'] for x in lp if x['suite']==s)) for s in suites],BLUE[3])]:
 a.bar(xx+off,vals,.36,label=label,color=col)
 for x,y in zip(xx+off,vals):a.text(x,y+1,f'{y:.1f}',ha='center',fontsize=8)
a.set_xticks(xx,['Spatial','Object','Goal','Long']);a.set_ylabel('Success rate (%)');a.set_ylim(0,108);a.set_title('(a) Qwen3.5-4B: standard and zero-shot tests',loc='left',fontsize=10);grid(a)
outside_legend(a,ncol=2)
a=axes[1];cat.sort(key=lambda x:float(x['success_rate_pct']));ys=np.arange(len(cat));rates=[float(x['success_rate_pct']) for x in cat];a.barh(ys,rates,color=[plt.cm.Blues(.35+.5*i/6) for i in range(7)])
a.set_yticks(ys,[x['category'] for x in cat],fontsize=9);a.set_xlim(0,104);a.set_xlabel('Success rate (%)');a.set_title('(b) LIBERO-plus: seven perturbation dimensions',loc='left',fontsize=10,pad=35)
for y,r in zip(ys,rates):a.text(r+1,y,f'{r:.2f}',va='center',fontsize=9)
a.set_axisbelow(True);a.grid(axis='x',color='#e5e7eb',lw=.6);fig.tight_layout(w_pad=2);save(fig,'07_robustness')
# RoboCasa outcomes; direct task counts, stable readable abbreviations.
RC=read('robocasa_tasks.csv');RC.sort(key=lambda x:int(x['success']))
fig,a=plt.subplots(figsize=(10.8,6.5));ys=np.arange(len(RC));rates=[float(x['success_rate_pct']) for x in RC];rc_mean=100*sum(int(r['success']) for r in RC)/sum(int(r['episodes']) for r in RC)
labels=[x['task'].replace('PosttrainPnPNovelFrom','').replace('SplitA','').replace('To',' → ') for x in RC]
a.barh(ys,rates,color=[plt.cm.Blues(.3+.55*i/(len(RC)-1)) for i in range(len(RC))]);a.set_yticks(ys,labels,fontsize=9);a.set_xlim(0,85);a.set_xlabel('Success rate (%) — 50 episodes per task');a.axvline(rc_mean,ls='--',lw=1.1,color='#4b5563',label=f'Mean: {rc_mean:.2f}%')
for y,r in zip(ys,rates):a.text(r+1,y,f'{r:.0f}',va='center',fontsize=8)
a.set_title('RoboCasa GR1 Tabletop: Qwen3.5-4B / 50k steps',loc='left',fontsize=12);a.grid(axis='x',color='#e5e7eb',lw=.6);a.set_axisbelow(True);outside_legend(a,fontsize=9);fig.tight_layout();save(fig,'08_robocasa')
# CALVIN chain survival and conditional task failures use distinct denominators.
chain=read('calvin_chain.csv');ct=read('calvin_tasks.csv');families=read('calvin_families.csv');summary=read('calvin_summary.csv')[0]
fig,axes=plt.subplots(1,2,figsize=(12,3.8),gridspec_kw={'width_ratios':[1,1.15]});a=axes[0]
xx=np.arange(1,6);rates=[float(r['success_rate_pct']) for r in chain]
a.bar(xx,rates,color=BLUE[:5]);a.set_xticks(xx);a.set_ylim(0,105);a.set_ylabel('Sequences completing prefix (%)');a.set_xlabel('Number of consecutive tasks completed');a.set_title(f"(a) ABCD → D: mean length {summary['avg_seq_len']}",loc='left',fontsize=11);grid(a)
for x,r,c in zip(xx,rates,chain):a.text(x,r+1.8,f"{r:.1f}%\n{c['success']}/1000",ha='center',fontsize=8)
a=axes[1];push=[r for r in ct if r['task'].startswith('push_') and r['task'].endswith(('_left','_right'))];push.sort(key=lambda r:float(r['success_rate_pct']));ys=np.arange(len(push));rates=[float(r['success_rate_pct']) for r in push];reference=float(next(r['success_rate_pct'] for r in families if r['family']=='Other tasks'))
a.barh(ys,rates,color=[BLUE[1] if r['task'].endswith('left') else BLUE[3] for r in push]);a.set_yticks(ys,[r['task'].replace('push_','').replace('_block_',' → ') for r in push],fontsize=9);a.set_xlim(0,105);a.set_xlabel('Success / reached task attempts (%)');a.set_title('(b) Horizontal pushing: direction-dependent failures',loc='left',fontsize=10)
for y,r,t in zip(ys,rates,push):a.text(r+1,y,f"{r:.1f} ({t['success']}/{t['attempts']})",va='center',fontsize=8)
a.axvline(reference,color=GRAY,ls='--',lw=1,label=f'Other tasks: {reference:.2f}%');outside_legend(a);axes[0].set_title(axes[0].get_title(loc='left'),loc='left',pad=35);a.grid(axis='x',color='#e5e7eb',lw=.6);a.set_axisbelow(True);fig.tight_layout(w_pad=2);save(fig,'09_calvin')
# Final CALVIN training run only; preliminary restarts are retained in the audit.
loss=read('calvin_loss.csv');steps=np.array([int(r['step']) for r in loss]);values=np.array([float(r['action_dit_loss']) for r in loss]);smooth=np.convolve(values,np.ones(10)/10,mode='valid')
fig,axes=plt.subplots(1,2,figsize=(11.8,3.4))
for a in axes:a.plot(steps/1000,values,color=BLUE[2],alpha=.22,lw=.7,label='Raw observations');a.plot(steps[9:]/1000,smooth,color=BLUE[3],lw=1.5,label='10-point moving average');a.set_xlabel('Training step (×1000)');a.set_ylabel('Action loss');grid(a)
axes[0].set_title('(a) CALVIN: final 34k-update training run',loc='left');axes[0].set_ylim(0,max(values)*1.08)
axes[1].set_title('(b) Late training — log scale',loc='left');axes[1].set_xlim(5,34);axes[1].set_yscale('log');axes[1].set_ylim(.005,1)
fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,0),frameon=False,fontsize=9,ncol=2)
fig.tight_layout(w_pad=2,rect=(0,.12,1,1));save(fig,'10_calvin_loss')
print('Generated 10 figure sets: PDF + SVG + PNG')
