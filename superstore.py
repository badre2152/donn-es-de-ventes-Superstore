# %% [markdown]
# IMPORTATION ET EXPLORATION

# %%
import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\user\Desktop\superstore\store.csv')


# %% [markdown]
# filling the missing postal code using mapping method

# %%
mapping = df.dropna(subset=['Postal Code']).set_index('City')['Postal Code'].to_dict()

df['Postal Code'] = df['Postal Code'].fillna(df['City'].map(mapping))

# %% [markdown]
# changing the date format

# %%
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

# %% [markdown]
# converting ("Postal Code") type into string

# %%
df['Postal Code'] = df['Postal Code'].astype(int).astype(str)

# %% [markdown]
# Nettoyage

# %%
print(df.columns)

# %%
df.sample(10,random_state=42)

# %%
text_columns = ['Customer Name', 'City', 'State', 'Product Name', 'Category', 'Sub-Category']

for col in text_columns:
    df[col] = df[col].str.strip().str.title()

df['Order ID'] = df['Order ID'].str.strip().str.upper()
df['Product ID'] = df['Product ID'].str.strip().str.upper()

# %%
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# %%
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month_name()
df['Order Day'] = df['Order Date'].dt.day

# %%
df['Segment'] = df['Segment'].str.strip().str.title()
df['Ship Mode'] = df['Ship Mode'].str.strip().str.title()
df['Region'] = df['Region'].str.strip().str.title()

# %%
df_alt = df.copy()

# %%
df_alt.info()

# %%
df_alt.sample(10,random_state=42)

# %%
df_alt['Order Quarter'] = df_alt['Order Date'].dt.to_period('Q').astype(str)

print(df_alt['Order Quarter'].head())


# %%
print(df.columns.tolist())

# %%
df.sample(5,random_state=42)

# %%
df['Profit'] = df['Sales'] * 0.30

df['Profit Margin %'] = (df['Profit'] / df['Sales']) * 100

df['Profit Margin %'] = df['Profit Margin %'].round(2)

print(df[['Sales', 'Profit', 'Profit Margin %']].head())


# %%
cat_columns = ['Segment', 'Category', 'Sub-Category', 'Region', 'Ship Mode', 'State']

for col in cat_columns:
    df[col] = df[col].astype('category')

print(df[cat_columns].dtypes)


# %%
bins = [0, 100, 1000, df['Sales'].max()]
labels = ['Low Sales', 'Medium Sales', 'High Sales']

df['Sales_Performance'] = pd.cut(df['Sales'], bins=bins, labels=labels)


# %%
def categorize_profit(margin):
    if margin > 20: return 'Highly Profitable'
    elif margin > 0: return 'Profitable'
    else: return 'Loss'

df['Profitability_Status'] = df['Profit Margin %'].apply(categorize_profit)


# %%
df.info()

# %%
df.describe()

# %%
df['Ship Delay'] = (df['Ship Date'] - df['Order Date']).dt.days

def ship_speed(days):
    if days <= 2: return 'Express'
    elif days <= 5: return 'Standard'
    else: return 'Late'

df['Shipping Class'] = df['Ship Delay'].apply(ship_speed)


# %%
df['Estimated Cost'] = df['Sales'] - df['Profit']

df['ROI_Factor'] = df['Profit'] / df['Estimated Cost']

df['Is_Profitable'] = df['Profit'] > 0

import numpy as np
df['ROI_Factor'] = df['ROI_Factor'].replace([np.inf, -np.inf], 0).fillna(0)

print(df[['Sales', 'Profit', 'Estimated Cost', 'ROI_Factor']].head())



# %%
total_sales = df['Sales'].sum()
df['Sales_Weight_%'] = (df['Sales'] / total_sales) * 100

# %%
region_analysis = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Profit Margin %': 'mean',
    'Order ID': 'count'
}).rename(columns={'Order ID': 'Total Orders'}).sort_values(by='Profit', ascending=False)

print(region_analysis)

# %%
product_performance = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'ROI_Factor': 'mean'
}).sort_values(by='Sales', ascending=False).head(10)

print(product_performance)

# %%
shipping_efficiency = df.groupby('Ship Mode').agg({
    'Ship Delay': 'mean',      
    'Sales': 'sum',            
    'Is_Profitable': 'mean'    
}).sort_values(by='Ship Delay')

print(shipping_efficiency)

# %%
monthly_trend = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().unstack()

# %%
invalid_dates = df[df['Ship Date'] < df['Order Date']]
print(f" Nombre d'erreurs temporelles : {len(invalid_dates)}")


# %%
invalid_profits = df[df['Profit'] > df['Sales']]
print(f" Nombre d'erreurs dans le calcul du profit : {len(invalid_profits)}")


# %%
zero_cost = df[(df['Sales'] > 0) & (df['Estimated Cost'] <= 0)]
print(f" Nombre de commandes à un coût déraisonnable (0 ou moins) : {len(zero_cost)}")

# %%
zip_check = df.groupby('Postal Code')['City'].nunique()
invalid_zips = zip_check[zip_check > 1]
print(f" Nombre de codes postaux associés à plus d'une ville : {len(invalid_zips)}")

# %%
zip_check = df.groupby('Postal Code')['City'].nunique()
invalid_zip_list = zip_check[zip_check > 1].index.tolist()

duplicate_cities = df[df['Postal Code'].isin(invalid_zip_list)][['Postal Code', 'City']].drop_duplicates()
print(duplicate_cities)


# %%
df.loc[df['Postal Code'] == '92024', 'City'] = 'Encinitas'

check_again = df.groupby('Postal Code')['City'].nunique()
print(f" Le nombre de symboles associés à plus d'une ville à présent : {check_again[check_again > 1].count()}")

# %%
cols_order = [
    'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 
    'Customer ID', 'Customer Name', 'Segment', 'Country', 'City', 
    'State', 'Postal Code', 'Region', 'Product ID', 'Category', 
    'Sub-Category', 'Product Name', 'Sales', 'Profit', 'Estimated Cost',
    'Profit Margin %', 'ROI_Factor', 'Quantity', 'Ship Delay', 'Shipping Class',
    'Order Year', 'Order Month', 'Order Day', 'Sales_Performance', 'Is_Profitable'
]
df = df[ [c for c in cols_order if c in df.columns] ]


# %%
df_for_sql = df.copy()
for col in df_for_sql.select_dtypes('category').columns:
    df_for_sql[col] = df_for_sql[col].astype(str)

# %%
df.to_csv('superstore_clean.csv', index=False, encoding='utf-8-sig')

print("✅ The file was successfully exported with the name: superstore_clean.csv")
print(f"📊 Exported data size: {df.shape[0]} ligne {df.shape[1]} colonne.")


