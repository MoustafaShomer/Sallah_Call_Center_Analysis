# Sallah Call Center Analysis

This project showcases a **complete data analysis workflow in Python**, applied to a real call-center dataset (confidential, not shared).  
The goal is to demonstrate my ability to handle raw data, clean it, detect outliers, explore trends, and answer analytical business questions.

---

## Project Overview

The project includes all stages of a professional data analysis process:

1. **Data Collection & Combination**  
   - Imported monthly CSV files (February, March, April).  
   - Merged them into one consolidated DataFrame using `pd.concat()`.

2. **Data Cleaning**  
   - Standardized column names to lowercase and replaced spaces with underscores.  
   - Checked for missing and duplicated records.  
   - Converted date columns to `datetime` objects.  

3. **Outlier Detection & Treatment**  
   - Built a custom function `detect_outliers()` to loop through numeric columns.  
   - Calculated **IQR (Interquartile Range)** for each variable.  
   - Reported number and percentage of outliers per column.  
   - Created a second function `handle_outlier()` to cap extreme values at upper/lower bounds.

4. **Descriptive Analysis & KPIs**  
   - Calculated total Forecasted Calls, Calls Offered, and Calls Handled across months.  
   - Computed **Call Abandonment Rate per Month** and identified the highest one.  
   - Evaluated **Top 3 Agents by Average Answer Time**.  
   - Measured **ASA (Average Speed of Answer)** trend month by month.  
   - Determined whether the team met demand based on handled/offered call ratio.  

5. **Visualization**  
   - Used `Matplotlib` and `Seaborn` for data exploration.  
   - Generated a **line chart** to show ASA trend by month.  

---

## Key Technical Highlights

- **Functions & Modularity:**  
  Encapsulated repetitive logic (outlier detection, treatment) in reusable functions.

- **Analytical Thinking:**  
  Each code block addresses a specific business question (documented via comments in the script).

- **Visualization:**  
  Used clean, simple charts that communicate insights (e.g., ASA trend, monthly comparison).

- **KPI-Oriented Mindset:**  
  Focused on actionable metrics like call abandonment rate, handled ratio, and agent efficiency.

---
## 🧰 Tools & Environment

- **Programming Language:** Python  
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn  
- **IDE:** Visual Studio Code / Jupyter Notebook  
- **Version Control:** Git & GitHub  

---


##  Example Code Snippet

```python
def detect_outliers(df):
    outlier_summary = {}
    for col in df.select_dtypes(include=['int64','float64']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_summary[col] = len(outliers)
    return outlier_summary
```
---
### Data Confidentiality

The original dataset belongs to a real company and contains sensitive operational data.
For legal and ethical reasons, it cannot be shared or accessed publicly.

>  *This repository is designed for professional assessment only.  
> No raw or proprietary data is shared or accessible.*
