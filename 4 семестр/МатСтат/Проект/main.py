import pandas as pd
import statsmodels.api as sm
import scipy.stats as stats
import matplotlib.pyplot as plt

def load_data():
    path = 'dunnhumby_The-Complete-Journey/'
    tx = pd.read_csv(path + 'transaction_data.csv').rename(columns={
        'HOUSEHOLD_KEY': 'household_key',
        'BASKET_ID': 'basket_id',
        'DAY': 'day',
        'QUANTITY':'quantity',
        'SALES_VALUE': 'sales',
        'RETAIL_DISC': 'retail_disc',
        'COUPON_DISC': 'coupon_disc',
        'COUPON_MATCH_DISC': 'coupon_match_disc',
        'STORE_ID': 'store_id'
    })
    return tx

def build_rfm(tx):
    agg = tx.groupby('household_key').agg(
        freq=('basket_id','nunique'),
        mon =('sales','sum'),
        tot_qty=('quantity','sum'),
        first_day=('day','min'),
        last_day =('day','max')
    ).reset_index()
    agg['AOV']    = agg['mon']/agg['freq']
    agg['repeat'] = ((agg['last_day']-agg['first_day'])<=30).astype(int)
    agg['AvgQty'] = agg['tot_qty']/agg['freq']
    return agg

def add_region(rfm, tx):
    region = (tx.groupby('household_key')['store_id']
                .agg(lambda x: x.mode().iat[0])
                .reset_index())
    region.columns = ['household_key','region']
    return rfm.merge(region, on='household_key', how='left')


def plot_results(rfm):
    plt.figure(figsize=(6,4))
    plt.scatter(rfm['freq'], rfm['AOV'], alpha=0.5)
    plt.xlabel('Частота покупок')
    plt.ylabel('Средний чек')
    plt.tight_layout()
    plt.savefig('img/freq_vs_aov.png')
    plt.close()

    plt.figure(figsize=(6,4))
    plt.scatter(rfm['mon'], rfm['AOV'], alpha=0.5)
    plt.xlabel('Прибыльность')
    plt.ylabel('Средний чек')
    plt.tight_layout()
    plt.savefig('img/mon_vs_aov.png'); plt.close()

def plot_top_stores(rfm, top_n=10):
    stats_store = (rfm.groupby('region')
                    .agg(mean_AOV=('AOV','mean'))
                    .sort_values('mean_AOV', ascending=False)
                  )
    top = stats_store.head(top_n)
    plt.figure(figsize=(8,4))
    top['mean_AOV'].plot(kind='bar')
    plt.xlabel('ID магазина')
    plt.ylabel('Средний чек')
    plt.tight_layout()
    plt.savefig('img/top_stores_mean_aov.png')
    plt.close()

def plot_h3(rfm):
    plt.figure(figsize=(6,4))
    rfm.boxplot(column='AvgQty', by='repeat')
    plt.xlabel('Повторная покупка (0/1)')
    plt.title('')
    plt.suptitle('')
    plt.ylabel('AvgQty')
    plt.tight_layout()
    plt.savefig('img/boxplot_avgqty_repeat.png')
    plt.close()


def test_h1(rfm):
    r1,p1 = stats.pearsonr(rfm['freq'], rfm['AOV'])
    r2,p2 = stats.pearsonr(rfm['mon'], rfm['AOV'])
    print(f"H1 freq->AOV: r={r1:.3f}, p={p1:.3e}")
    print(f"H1 mon->AOV: r={r2:.3f}, p={p2:.3e}")
    X = sm.add_constant(rfm[['freq','mon']])
    print(sm.OLS(rfm['AOV'], X).fit().summary())

def test_h2(rfm):
    groups = [g['AOV'].values for _,g in rfm.groupby('region')]
    f,p = stats.f_oneway(*groups)
    print(f"\nH2 ANOVA AOV~region: F={f:.2f}, p={p:.3e}")
    print(rfm.groupby('region')['AOV'].mean().sort_values())

def test_h3_alt(rfm):
    grp1 = rfm.loc[rfm['repeat']==1,'AvgQty']
    grp0 = rfm.loc[rfm['repeat']==0,'AvgQty']
    t,p = stats.ttest_ind(grp1, grp0, equal_var=False)
    print(f"\nH3 AvgQty (repeat vs no): t={t:.2f}, p={p:.3e}")
    print(f"mean AvgQty repeat=1: {grp1.mean():.2f}")
    print(f"mean AvgQty repeat=0: {grp0.mean():.2f}")

def main():
    tx = load_data()
    rfm = build_rfm(tx)
    rfm = add_region(rfm, tx)
    plot_results(rfm)
    plot_top_stores(rfm, top_n=10)
    plot_h3(rfm)
    test_h1(rfm)
    test_h2(rfm)
    test_h3_alt(rfm)

if __name__=='__main__':
    main()
