import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

top_dir = r"C:\Users\Laura\OneDrive - Northwestern University\SoundBrain Lab - EAM2\beh_raw"

df_motor = pd.DataFrame()
df_active = pd.DataFrame()
df_passive = pd.DataFrame()
for file in os.listdir(top_dir):
    if 'pilot' not in file:
        continue
    df = pd.read_csv(os.path.join(top_dir, file), 
                     sep='\t',
                     skiprows=2,
                     usecols=['Trial', 'Event Type', 'Code', 'Time'])
    
    df = df[pd.to_numeric(df["Time"], errors='coerce').notna()].copy()
    df["Time"] = df["Time"].astype(float)

    # get condition and run information from file name
    fname_no_ext = file.split('.')[0]
    fname_split = fname_no_ext.split('-')
    sub = fname_split[0]
    cond = fname_split[1].split('_')[0]
    sch = fname_split[2]

    if "passive" not in sch:
        df = df[df["Event Type"] == 'Response'].copy()

    df["ISI"] = df["Time"].diff()
    isi = df.dropna(subset=["ISI"]).copy()
    isi['ISI_ms'] = isi['ISI'] / 10


    if cond == "motor":
        df_motor = pd.concat((df_motor, isi))
        print(f"length of motor dataframe: {len(df_motor)}")
    elif "active" in sch:
        df_active = pd.concat((df_active, isi))
        print(f"length of active dataframe: {len(df_active)}")
    elif "passive" in sch:
        df_passive = pd.concat((df_passive, isi))
        print(f"length of passive dataframe: {len(df_passive)}")

df_active = df_active[df_active['ISI_ms']< 6000]

print("Stats for motor only:")
print(f"Mean Response ISI: {df_motor['ISI_ms'].mean():.2f} ms")
print(f"Std Response ISI: {df_motor['ISI_ms'].std():.2f} ms")
print(f"Max Response ISI {df_motor['ISI_ms'].max():.2f} ms")
print(f"Min Response ISI {df_motor['ISI_ms'].min():.2f} ms")

print("\nStats for active task:")
print(f"Mean Response ISI: {df_active['ISI_ms'].mean():.2f} ms")
print(f"Std Response ISI: {df_active['ISI_ms'].std():.2f} ms")
print(f"Max Response ISI {df_active['ISI_ms'].max():.2f} ms")
print(f"Min Response ISI {df_active['ISI_ms'].min():.2f} ms")

# histograms
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 6))
h1 = sns.histplot(df_motor['ISI_ms'], ax=ax[0], bins=100)
ax[0].set_xlabel('ISI (ms)')
ax[0].set_ylabel('Count')
ax[0].axvline(df_motor['ISI_ms'].mean(), color='red', linestyle='--')
ax[0].annotate(f"Mean= {df_motor['ISI_ms'].mean():.2f}", xy=(df_motor['ISI_ms'].mean(), ax[0].get_ylim()[1]),
               xytext=(df_motor['ISI_ms'].mean() + 5, ax[0].get_ylim()[1] * .95), annotation_clip=False)
ax[0].set_xlim(df_motor['ISI_ms'].min() - 1, df_motor['ISI_ms'].max() + 1)
ax[0].set_title(f'ISI distribution for response in motor only')

h2 = sns.histplot(df_active['ISI_ms'], ax=ax[1], bins=100)
ax[1].set_xlabel('ISI (ms)')
ax[1].axvline(df_active['ISI_ms'].mean(), color='red', linestyle='--')
ax[1].annotate(f"Mean= {df_active['ISI_ms'].mean():.2f}", xy=(df_active['ISI_ms'].mean(), ax[1].get_ylim()[1]),
               xytext=(df_active['ISI_ms'].mean() + 10, ax[1].get_ylim()[1] * .95), annotation_clip=False)
ax[1].set_xlim(df_active['ISI_ms'].min() - 1, df_active['ISI_ms'].max() + 1)
ax[1].set_title(f'ISI distribution for response in active task')

h3 = sns.histplot(df_passive['ISI_ms'], ax=ax[2], bins=100)
ax[2].set_xlabel('ISI (ms)')
ax[2].set_title(f'ISI distribution for sound stimuli in passive task')
plt.tight_layout()

# violin plots of response ISI (motor and active)
df_motor['Condition'] = 'motor'
df_active['Condition'] = 'active'
response_df = pd.concat((df_motor, df_active))
fig2, ax2 = plt.subplots()
sns.violinplot(x='Condition', y='ISI_ms', data=response_df, ax=ax2, palette='pastel', hue='Condition', legend=False, linewidth=1)
ax2.set_title('Response ISI distribution')
plt.show()
