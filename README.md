
# 📄 CPWD eTender Scraper

This project is a Python script that scrapes **public tender data** from the [CPWD eTender website](https://etender.cpwd.gov.in/), specifically from the **"New Tenders → All"** section.

It uses **Selenium WebDriver** to extract the latest tender listings (first N tenders, default: 20) and saves the relevant details into a **CSV file**.

---

## 🚀 Features

- Automatically launches a headless browser.
- Handles JavaScript-rendered content and popup alerts.
- Selects the number of records per page (10, 20, 40, 50, 100).
- Extracts:
  - NIT/RFP NO
  - Name of Work / Subwork / Packages
  - Estimated Cost
  - Bid Submission Closing Date & Time
  - EMD Amount
  - Bid Opening Date & Time
- Saves data as `new_tenders_data.csv`.

---

## 📦 Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Script Overview

##### Configurable Parameters

| Variable           | Description                                      | Default      |
|--------------------|--------------------------------------------------|--------------|
| `WEBPATH`          | URL of the CPWD eTender site                     | `"https://etender.cpwd.gov.in"` |
| `no_of_Records`   | Number of tender records to extract              | `10/20/40/50/100`  |
| `csv_columns`      | Mapping of raw column headers to clean headers   | (dict shown below) |

```python
csv_columns = {
    "NIT/RFP NO": "ref_no",
    "Name of Work / Subwork / Packages": "title",
    "Estimated Cost": "tender_value",
    "Bid Submission Closing Date & Time": "bid_submission_end_date",
    "EMD Amount": "emd",
    "Bid Opening Date & Time": "bid_open_date"
}
```

---

## 📂 Output

The final data will be saved in the file:

```
new_tenders_data.csv
```

with cleaned and renamed column headers as per the `csv_columns` mapping.

---

## 🧪 How It Works

1. Opens the CPWD eTender portal.
2. Clicks the "All" tab under **New Tenders**.
3. Selects 20 tenders per page via dropdown.
4. Waits for the table to reload.
5. Extracts data for the first 10/20/40/50/100 tenders.
6. Saves the output into a CSV file.

---

## ⚠️ Known Limitations

- This script assumes the site structure remains unchanged.
- Requires a stable internet connection.
- Sleep Required Due to government website can block access (if many requests at the same time). 
- Default Sleep time 3 second (Editable).
- Default No of Record 20 (Editable).
- May need updating if the website DOM or alert behavior changes.

---

## 💻 Run the Script

```bash
python tender_scraper.py
```

Make sure `tender_scraper.py` contains your full script.

---

## 📬 Author

**Saidul Ali Mallick (Sami)**  
B.Tech CSE - AIML | Backend Developer | Photographer | 
Let the code tell your story 🧡
