import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_axisbelow(True)
    ax.xaxis.set_tick_params(rotation=45)
    ax.yaxis.set_major_formatter(lambda x, _: '{:,.0f}'.format(x))
    ax.set_ylim(20000, 180000)
    plt.tight_layout()
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    
    df_bar = df.groupby(['year', 'month'], observed = False)['value'].mean().unstack()

    # Draw bar plot

    fig, ax = plt.subplots(figsize=(10, 7))
    df_bar.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_ylim([0,140000])
    ax.legend(title='Months', loc='upper left')
    ax.set_xticklabels(df_bar.index, rotation=90)
    plt.tight_layout()
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_year = df_box.copy()
    df_month = df_box.copy()

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(18, 10))
    sns.boxplot(y='value', x='year',  data=df_year, ax=axes [0], saturation=2)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_ylim(0, 200000)
    axes[0].set_yticks(range(0, 200001, 20000))
    axes[0].set_yticklabels([f'{i:,}'.replace(',', '') for i in range(0, 200001, 20000)])

    sns.boxplot(y='value', x='month',  data=df_month, ax=axes[1],
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], saturation= 2)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_ylim(0, 200000)
    axes[1].set_yticks(range(0, 200001, 20000))
    axes[1].set_yticklabels([f'{i:,}'.replace(',', '') for i in range(0, 200001, 20000)])

    plt.tight_layout()
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
