## 📂 Data Access

The dataset used in this project is based on the **Online Retail II** dataset, which contains transactional data from a UK-based online retail company.

Due to GitHub file size limitations and best practices in data science project structuring, the dataset is **not included directly in this repository**.

---

### 🔗 Dataset Source

You can access the dataset from the official source below:

- https://archive.ics.uci.edu/ml/datasets/online+retail+ii
  
---

### 📊 Dataset Description

The dataset includes real-world transactional data with the following key attributes:

- **Invoice**: Unique transaction identifier  
- **StockCode**: Product/item code  
- **Description**: Product name  
- **Quantity**: Number of items purchased  
- **InvoiceDate**: Transaction timestamp  
- **Price**: Unit price  
- **CustomerID**: Unique customer identifier  
- **Country**: Customer location  

---

### ⚙️ Data Preprocessing

Before modeling, the dataset undergoes several preprocessing steps to ensure analytical quality:

- Removal of canceled transactions (Invoices containing "C")  
- Exclusion of non-product entries (e.g., shipping codes such as "POST")  
- Filtering out invalid values (e.g., non-positive prices)  
- Handling missing values  
- Outlier capping using IQR-based thresholds  

---

### 🤖 Recommendation System (Association Rule Learning)

After preprocessing, an **Association Rule Learning (ARL)**–based recommendation system is developed using the **Apriori Algorithm**.

The goal is to identify products that are frequently purchased together and generate **data-driven product recommendations**.

---

#### 🧠 Approach

The recommendation system follows these steps:

- Transform transactional data into a **basket (invoice-product) matrix**  
- Convert quantities into a **binary format** (1 if purchased, 0 otherwise)  
- Apply the **Apriori algorithm** to extract frequent itemsets  
- Generate **association rules** using support, confidence, and lift metrics  
- Rank rules based on **lift** to identify strong product relationships  

---

#### 📊 Key Concepts

- **Support** → Frequency of itemset occurrence  
- **Confidence** → Probability of purchasing item B given item A  
- **Lift** → Strength of association between products (higher = stronger relationship)  

---

#### ⚙️ Recommendation Logic

- For a given product:
  - Find rules where the product appears in the **antecedent (left-hand side)**  
  - Retrieve the corresponding **consequents (right-hand side)**  
  - Sort by **lift** to prioritize stronger associations  
  - Return top-N recommended products  

---

#### 🎯 Business Value

This system enables:

- Cross-selling opportunities (e.g., “Customers who bought this also bought…”)  
- Improved product bundling strategies  
- Increased average order value (AOV)  
- More personalized shopping experiences  

---

#### 💡 Example Use Case

If a customer purchases a specific product, the system can recommend complementary products based on historical co-purchase patterns.

This makes the solution directly applicable to:
- E-commerce recommendation engines  
- Campaign targeting  
- Product placement strategies  
