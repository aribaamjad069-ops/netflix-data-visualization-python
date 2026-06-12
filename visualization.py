import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Optional

# ========== CONFIG ==========
CSV_FILE = 'netflix.csv' # Agar file ka naam alag hai to yahan change kar do
OUTPUT_DIR = 'charts'
FIGURE_SIZE = (10, 6)

def setup() -> None:
    """Create charts folder and set plot style"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = FIGURE_SIZE
    plt.rcParams['figure.dpi'] = 150

def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """Load CSV and return dataframe. Error handle karta hai"""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"❌ Error: '{filepath}' file nahi mili. Folder me rakho.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def plot_content_type(df: pd.DataFrame) -> None:
    """Movies vs TV Shows ka bar chart"""
    if 'type' not in df.columns:
        print("⚠️ 'type' column missing, chart skip")
        return

    plt.figure()
    ax = sns.countplot(x='type', data=df, palette=['#E50914', '#221f1f'])
    plt.title('Netflix Content: Movies vs TV Shows', fontsize=14, fontweight='bold')
    plt.xlabel('Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    # Bar ke upar count likh do
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart1_movies_vs_tvshows.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"✅ Chart 1 saved: {path}")

def plot_top_countries(df: pd.DataFrame, top_n: int = 10) -> None:
    """Top N countries ka bar chart"""
    if 'country' not in df.columns:
        print("⚠️ 'country' column missing, chart skip")
        return

    plt.figure()
    top_countries = df['country'].dropna().value_counts().head(top_n)
    ax = top_countries.plot(kind='bar', color='coral', edgecolor='black')

    plt.title(f'Top {top_n} Countries by Content', fontsize=14, fontweight='bold')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Number of Titles', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart2_top_countries.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"✅ Chart 2 saved: {path}")

def plot_release_year(df: pd.DataFrame) -> None:
    """Release year ka histogram"""
    if 'release_year' not in df.columns:
        print("⚠️ 'release_year' column missing, chart skip")
        return

    plt.figure()
    df['release_year'].dropna().hist(bins=30, color='skyblue', edgecolor='black')
    plt.title('Content Distribution by Release Year', fontsize=14, fontweight='bold')
    plt.xlabel('Release Year', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart3_release_year.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"✅ Chart 3 saved: {path}")

def main() -> None:
    """Sab charts banane ka main function"""
    print("="*60)
    print("NETFLIX EDA - CHART GENERATION")
    print("="*60)

    setup()
    df = load_data('netflix_titles.csv')

    if df is None:
        return

    print("\n📊 Generating Charts...")
    plot_content_type(df)
    plot_top_countries(df, top_n=10)
    plot_release_year(df)

    print("\n" + "="*60)
    print(f"✅ DONE! Check '{OUTPUT_DIR}' folder for PNG files")
    print("="*60)

if __name__ == "__main__":
    main()