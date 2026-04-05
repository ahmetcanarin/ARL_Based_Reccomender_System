import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Display settings for better readability during analysis
pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 10)

# Load dataset (transaction-level retail data)
df_ = pd.read_excel("online_retail_II.xlsx", sheet_name=2010-2011)
df_.to_pickle("Online_Retail_II_2010-11.pickle")
df = pd.read_pickle("Online_Retail_II_2010-11.pickle")

# Initial data inspection
df.describe().T
df.info()
df.isnull().sum()

# ---------------------------
# DATA CLEANING & PREPROCESSING
# ---------------------------

# Remove non-product entries such as shipping costs (POST)
df = df[~df["StockCode"].str.contains("POST", na=False)]

# Drop missing values to ensure clean transactional structure
df.dropna(inplace=True)

# Remove canceled transactions (invoices containing "C")
df = df[~df["Invoice"].str.contains("C", na=False)]

# Remove invalid transactions with non-positive prices
df = df[df["Price"] > 0]


# ---------------------------
# OUTLIER HANDLING
# ---------------------------

def outlier_thresholds(dataframe, variable):
    """
    Calculates lower and upper bounds for outliers using IQR method
    based on 1% and 99% quantiles.
    """
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    """
    Caps extreme values instead of removing them,
    preserving dataset size while reducing noise.
    """
    low_limit, up_limit = outlier_thresholds(dataframe, variable)

    dataframe.loc[(dataframe[variable] < low_limit), variable] = \
        int(low_limit) if df[variable].dtype == int else low_limit

    dataframe.loc[(dataframe[variable] > up_limit), variable] = \
        int(up_limit) if df[variable].dtype == int else up_limit


# Apply outlier capping on critical numerical features
replace_with_thresholds(df, "Price")
replace_with_thresholds(df, "Quantity")


# ---------------------------
# FILTERING (COUNTRY-LEVEL ANALYSIS)
# ---------------------------

# Focus analysis on Germany to build country-specific recommendations
df_ger = df[df['Country'] == "Germany"]


# ---------------------------
# BASKET STRUCTURE CREATION
# ---------------------------

# Create invoice-product matrix:
# Rows → invoices
# Columns → products
# Values → binary (1 if purchased, 0 otherwise)

def create_invoice_product_df(dataframe, id=False):
    """
    Converts transactional data into a basket (invoice-product) matrix.

    If id=True → uses StockCode
    If id=False → uses product Description
    """
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0).\
                map(lambda x: True if x > 0 else False)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0).\
            map(lambda x: True if x > 0 else False)


ger_inv_pro_df = create_invoice_product_df(df_ger, id=True)


# ---------------------------
# ASSOCIATION RULE LEARNING
# ---------------------------

def create_rules(dataframe, id=True, country="Germany"):
    """
    Generates association rules using Apriori algorithm.

    Steps:
    1. Filter dataset by country
    2. Create basket matrix
    3. Generate frequent itemsets
    4. Derive association rules
    """
    dataframe = dataframe[dataframe["Country"] == country]

    dataframe = create_invoice_product_df(dataframe, id)

    # Extract frequent itemsets (minimum support threshold)
    frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True)

    # Generate rules using support as evaluation metric
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)

    return rules


rules = create_rules(df_ger)


# ---------------------------
# PRODUCT IDENTIFICATION HELPER
# ---------------------------

def check_id(dataframe, stock_code):
    """
    Retrieves product name from StockCode for interpretability.
    """
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)


# Example: check product name
check_id(df_ger, 11001)


# Select a random antecedent to test recommendation system
orn = list(rules['antecedents'].sample(1).values[0])[0]
check_id(df_ger, orn)


# ---------------------------
# RECOMMENDATION SYSTEM
# ---------------------------

def arl_recommender(rules_df, product_id, rec_count=1):
    """
    Recommends products based on Association Rule Learning (ARL).

    Logic:
    - Sort rules by lift (strength of association)
    - Find rules where given product is in antecedents
    - Return corresponding consequents as recommendations
    """
    sorted_rules = rules_df.sort_values("lift", ascending=False)

    recommendation_list = []

    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]


# Example recommendation
check_id(df_ger, arl_recommender(rules, orn, 1)[0])
