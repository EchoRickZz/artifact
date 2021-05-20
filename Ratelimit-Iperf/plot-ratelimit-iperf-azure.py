#!/usr/bin/python3
from os import path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.utils import *
import context

# Start of Config
EXPR_NAME = 'Ratelimit-Iperf'
SHOW_PLOT_FLAG = False  # True will show in GUI, False will save plot as file
MARKERS = ['*', 'd', '>', '<', '^', 'v']

OP_COLOR = {
    'Verizon': '*',
    'single': 'P'
}
CONN_LINE_STYLE = {
    'multi': '-',
    'single': '--'
}

# End of Config

# filter data using config

df = pd.read_csv(path.join(context.data_processed_dir, f"{EXPR_NAME}_combined.csv"))

# country-level
grp = df.groupby(['server location', 'type', 'distance']).agg(
    download_max=('throughput_rolled3', np.max),
    download_mean=('throughput_rolled3', np.mean),
    download_median=('throughput_rolled3', np.median),
    latency_min=('latency_min', np.min),
)

grp.reset_index(level=0, inplace=True)
grp.reset_index(level=0, inplace=True)
grp.reset_index(level=0, inplace=True)

grp.sort_values(by=['distance', 'type'], ascending=True, inplace=True)

####################################################################
# Azure Servers
####################################################################
plot_id = '24a'
plot_name = 'rate-limiting-iperf-azure'

color_list = ['tab:green', 'tab:orange', 'tab:blue', 'tab:red']

plt.close('all')
plt.figure(figsize=(6, 1.8))
print('plotting {} - {} plot...'.format(plot_id, plot_name))

x = np.arange(grp['server location'].unique().shape[0])  # the label locations
width = 0.2  # the width of the bars

df_udp = grp[(grp['type'] == 'udp')].copy(deep=True)
df_tcp8 = grp[(grp['type'] == 'tcp8')].copy(deep=True)
df_tcp1c = grp[(grp['type'] == 'tcp1c')].copy(deep=True)
df_tcp1d = grp[(grp['type'] == 'tcp1d')].copy(deep=True)

plt.bar(x, df_udp['download_max'].tolist(), width, label='UDP', hatch='/////',
        ec=colorlist20[4], color=colorlist20[5], alpha=1, zorder=2)
plt.bar(x + width, df_tcp8['download_max'].tolist(), width, label='TCP-8', hatch='xxxxx',
        ec=colorlist20[2], color=colorlist20[3], alpha=1, zorder=2)
plt.bar(x + width * 2, df_tcp1c['download_max'].tolist(), width, label='TCP-1 Tuned', hatch='\\\\\\\\\\',
        ec=colorlist20[0], color=colorlist20[1], alpha=1, zorder=2)
plt.bar(x + width * 3, df_tcp1d['download_max'].tolist(), width, label='TCP-1 Default', hatch='.....',
        ec=colorlist20[6], color=colorlist20[7], alpha=1, zorder=2)


plt.ylabel('Throughput\n(in Mbps)', fontsize=14)
plt.xlabel('Microsoft Azure Server Location ID', fontsize=14)
server_list = [f'AZ{i}' for i in range(1, grp['server location'].unique().shape[0] + 1)]
ax = plt.gca()
ax.set_xticks(x + (width * 1.5))
ax.set_xticklabels(server_list)
ax.tick_params(axis='x')
ax.set_yticks(np.arange(0, 2100, 500))
legend1 = ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.4, 1.28), facecolor='#dddddd',
                    handlelength=2, framealpha=.7, fontsize=12, borderpad=0.3, labelspacing=.21, handletextpad=.3)

ax.grid(axis='y', linestyle='--', zorder=-1)
ax.set_axisbelow(True)
ax.yaxis.grid(color='gainsboro', linestyle='dashed')
if not os.path.exists(context.plot_dir):
    os.makedirs('{}/png/'.format(context.plot_dir))

plotme(plt, plot_id, plot_name, context.plot_dir, show_flag=SHOW_PLOT_FLAG, png_only=False, pad_inches=0.07)

####################################################################


print('Complete./')
