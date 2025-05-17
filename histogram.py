import bibtexparser
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path

# ---------- load BibTeX ----------------------------------------------------
with open('bib/references.bib', encoding='utf-8') as f:
    bib = bibtexparser.load(f)
entries = bib.entries

# ---------- collect counts  (year, catogory) -----------------------------------
catogorys = set()
matrix = defaultdict(lambda: defaultdict(int))   # year → catogory → count

for e in entries:
    # parse year
    try:
        year = int(e.get('year', 0))
    except ValueError:
        continue
    
    # use the 'catogory' field directly
    catogory_tag = e.get('catogory', 'unknown')
    catogorys.add(catogory_tag)
    matrix[year][catogory_tag] += 1

year_list = sorted(matrix.keys())
catogory_list = sorted(catogorys)  # fixed order in legend

# ---------- colour palette per catogory ----------------------------------------
catogory_colour = {
    'missing-modality'        : '#4e79a7',  # blue
    'transformer-segmentation': '#ff9da7',  # pink
    'frequency-segmentation'  : '#59a14f',  # green
    'image-super-resolution'  : '#b07aa1',  # purple
}

# ---------- start new, wider figure ----------------------------------------
plt.figure(figsize=(12, 6))
bottom = [0] * len(year_list)

# ---------- build stacked bars ---------------------------------------------
for t in catogory_list:
    heights = [matrix[y].get(t, 0) for y in year_list]
    plt.bar(year_list, heights, bottom=bottom,
            label=t.replace('-', ' ').title(),
            color=catogory_colour.get(t, '#bbbbbb'))
    bottom = [b + h for b, h in zip(bottom, heights)]

plt.xlabel('Publication Year')
plt.ylabel('Number of Papers')
plt.xticks(year_list, rotation=45)
plt.subplots_adjust(right=0.8)
plt.legend(frameon=False,
           loc='center left',
           bbox_to_anchor=(1.0, 0.5))
plt.tight_layout()

# ---------- ensure output directory exists and save ------------------------
Path('figs').mkdir(parents=True, exist_ok=True)
plt.savefig('figs/hist_years.png', dpi=300, bbox_inches='tight')
print('hist_years.png saved')