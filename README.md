## 📂 Data Access

The dataset used in this project is based on the **Online Retail II** dataset, which contains transactional data from a UK-based online retail company.

Due to GitHub file size limitations and best practices in data science project structuring, the dataset is **not included directly in this repository**.

---

### 🔗 Dataset Source

You can access the dataset from the official source below:

- UCI Machine Learning Repository:  
  https://archive.ics.uci.edu/ml/datasets/online+retail+ii

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

### 🧠 Why the Dataset is Not Included

Including large raw datasets directly in repositories is generally discouraged because:

- It increases repository size unnecessarily  
- It reduces cloning and usability performance  
- It violates common industry practices  

Instead, this project focuses on:
- **reproducibility**
- **clean code structure**
- **clear data access instructions**
