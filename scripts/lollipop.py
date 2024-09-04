import os
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_font
from highlight_text import fig_text, ax_text
from drawarrow import fig_arrow, ax_arrow
import numpy as np

EXPORT_PATH = './img/'

def create_lollipop_plot(csv_file_path: str, export_path: Optional[str] = EXPORT_PATH) -> None:
    """
    Create an enhanced lollipop plot showing global maximum temperature per year based on ERA5 Copernicus C3S data.

    Args:
        csv_file_path (str): The file path to the CSV file containing preprocessed data with 'Year' as the index.
        export_path (str, optional): The directory path to export the generated plot. Defaults to './img/'.

    Raises:
        FileNotFoundError: If the specified CSV file is not found.
        ValueError: If the CSV file does not contain the expected data format.
    """
    try:
        df = pd.read_csv(csv_file_path, index_col='Year')
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {csv_file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file {csv_file_path} is empty.")

    if 'Max Temperature' not in df.columns:
        raise ValueError("The CSV file does not contain a 'Max Temperature' column.")

    cmap = load_cmap('Bodianus_rufus', cmap_type='continuous', reverse=True, type_warning = False)
    font = load_font('https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Light.ttf?raw=true')
    bold_font = load_font('https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Medium.ttf?raw=true')
    arrow_props = dict(color='black', tail_width=0.05, linewidth=0.5, head_width=3, head_length=5)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_axis_off()

    vmin, vmax = df['Max Temperature'].min(), df['Max Temperature'].max()

    for year, row in df.iterrows():
        temp = row['Max Temperature']
        color = cmap((temp - vmin) / (vmax - vmin))
        ax.scatter(x=year, y=temp, color=color)
        ax.plot([year, year], [vmin, temp], color=color, alpha=0.8)

    for year in range(df.index.min(), df.index.max() + 1, 20):
        ax.text(x=year, y=vmin-0.2, s=f'{year:.0f}', font=font, size=15, ha='center')

    h_lines =  np.linspace(vmin, vmax, 5)
    ax.hlines(y=h_lines, xmin=df.index.min(), xmax=df.index.max(),
              colors=[cmap((val - vmin) / (vmax - vmin)) for val in h_lines],
              linewidth=1.2, zorder=-1, alpha=0.5)
    for value in h_lines:
        ax.text(x=df.index.min()-2, y=value, s=f'{value:.2f}', font=font,
                color=cmap((value - vmin) / (vmax - vmin)), size=9, va='center', ha='right')

    fig_text(x=0.1, y=0.95, s='Global Daily Surface Air Temperature', font=font, size=32, ha='left')

    fig_text(x=0.1, y=0.85,
              s='Maximum daily mean temperature from 1940 to present (World)',
              font=font, size=14, ha='left', color='grey', alpha=0.7)

    fig_text(x=0.1, y=0.05,
              s='<Graph>: Gaël PENESSOT\n<Data Source>: ERA5 Copernicus C3S',
              font=font, size=8, ha='left',
              highlight_textprops=[{'font': bold_font}]*2)

    ax_text(x=1963, y=vmax-0.13, s='Significant temperature\nincrease since 1980s', font=font, size=8, ha='left')
    ax_arrow(
         tail_position=(1972, vmax-0.3), head_position=(1980, vmax-0.9), **arrow_props
    )

    ax_text(x=2000, y=vmax-0.1, s='Recent years show\nhighest temperatures', font=font, size=8, ha='left')
    ax_arrow(
         tail_position=(2011, vmax-0.2), head_position=(2015, vmax-0.37), **arrow_props
    )

    ax.set_xlim(df.index.min() - 5, df.index.max() + 5)
    ax.set_ylim(vmin - 0.5, vmax + 0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(export_path, 'temperature_lollipop_plot.png'), dpi=300, bbox_inches='tight')
    plt.show()

def main() -> None:
    """
    Main function to create the enhanced lollipop plot from the processed CSV file.
    """
    csv_path = './data/processed/processed_data.csv'
    create_lollipop_plot(csv_path)

if __name__ == "__main__":
    main()