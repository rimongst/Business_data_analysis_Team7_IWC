
---

# **BDA: Business Data Analytics Pipeline** 📊  

## **📌 Project Overview**
This project is part of the Business Data Analysis (BDA) course at EDHEC Business School, developed by Group 7.

The BDA (Big Data Analytics) Pipeline is designed to ingest, clean, visualize, and analyze market data for the luxury watch brand IWC. 
The project provides insights into pricing trends, exchange rates, and demand patterns using advanced data analytics techniques.
---

## **⚙️ Features**
✅ **Data Ingestion**: Load and preprocess large-scale datasets  
✅ **Data Cleaning**: Convert currencies, filter outliers, standardize fields  
✅ **Data Merging**: Combine multiple datasets for a unified analysis  
✅ **Data Visualization**: Generate insightful plots (price distribution, trends, etc.)  
✅ **Cloud Integration**: Upload cleaned data to **Google BigQuery** and files to **Google Cloud Storage**  
✅ **Automated Pipeline**: Run the full pipeline with a single command  
✅ **Testing & Linting**: Built-in **unit tests**, **code formatters**, and **static analysis**  

---

## **📥 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/BDA.git
cd BDA
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### **3️⃣ Install Dependencies**
```bash
make install
```
This will install all required Python packages.

### **4️⃣ Install the Project in Editable Mode**
```bash
pip install -e .
```
This allows you to make changes to the source code without reinstalling the package.

### **5️⃣ Configure Google Cloud Credentials**
Rename `.env.example` to `.env` and set up your Google Cloud credentials:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/your-gcp-key.json
```
Ensure that your GCP **service account** has access to **BigQuery & Cloud Storage**.

---

## **🛠 Usage Guide**
### **Run the Full Data Pipeline**
To execute the entire data processing pipeline:
```bash
make run-pipeline
```
This will:
1. **Fetch exchange rates**
2. **Load and clean datasets**
3. **Merge multiple datasets**
4. **Generate visualizations**
5. **Upload cleaned data to BigQuery**
6. **Upload additional files to Cloud Storage**

---

### **Run Individual Steps**
| Command                | Description |
|------------------------|-------------|
| `make fetch-rates`     | Fetch latest exchange rates |
| `make clean-data`      | Clean raw datasets |
| `make combine-data`    | Merge multiple datasets |
| `make visualize`       | Generate data visualizations |
| `make upload`          | Upload cleaned data to BigQuery |
| `make upload-file`     | Upload images/files to Google Cloud Storage |
| `make clean`           | Remove temporary files and cache |

---

## **✅ Running Tests**
To run unit tests and check for errors:
```bash
make test
```
This will execute all tests under `tests/` and generate a **code coverage report (Not fully completed)**.

---

## **📂 Project Structure**
```
BDA/
├── .venv/                 # Virtual environment
├── data/                  # Raw datasets & exchange rates
│   ├── dataset_1.csv
│   ├── exchange_rates.json
│   ├── PM_extract_Jan_2025_10_brands.csv
├── requirements/          # Dependency files
│   ├── base.txt           # Core dependencies
│   ├── dev.txt            # Development dependencies
├── scripts/               # Standalone scripts (empty for now)
├── src/                   # Source code
│   ├── api/               # API interactions
│   │   ├── upload_new_exchange_rate.py  # Fetch exchange rates
│   ├── data_ingestion/    # Data processing scripts
│   │   ├── cleaner.py      # Data cleaning
│   │   ├── combine_data.py # Dataset merging
│   │   ├── data_viz.py     # Data visualization
│   │   ├── download_from_bigquery.py  # Fetch data from BigQuery
│   │   ├── load_data.py    # Load data from CSV
│   │   ├── upload_csv.py   # Upload data to BigQuery
│   │   ├── upload_to_bucket.py # Upload files to GCS
│   ├── main.py            # Main pipeline script
├── tests/                 # Unit tests（Not fully completed）
├── .env                   # Environment variables
├── config.json            # Configuration settings
├── Makefile               # Automation commands
├── README.md              # Project documentation
├── setup.py               # Package setup script
```

---

## **🔧 Development Guidelines**
### **📝 Code Formatting**
Format all Python files:
```bash
make format
```
Uses **Black** for automatic formatting.

### **🔍 Linting & Type Checking**
Run static analysis on the codebase:
```bash
make lint
```
This checks **code quality** using **Flake8** and **MyPy**.

---

## **☁️ Uploading Data to Google BigQuery**
Ensure that your **Google Cloud credentials** are set up before running:
```bash
make upload
```
This will:
1. **Read the `config.json` file**  
2. **Upload the cleaned dataset to Google BigQuery**

---

## **📦 Packaging & Deployment**
To package the project as a **Python module**, use:
```bash
python setup.py sdist bdist_wheel
```
To deploy via **Docker**, build and run:
```bash
docker build -t bda-project .
docker run -it --rm -v $(pwd):/app bda-project
```

---

## **🔮 Future Enhancements**
🚀 **Web-based dashboard** for visualization  
🚀 **CI/CD pipeline** with automated testing  
🚀 **Advanced data validation** & outlier detection  

---

## **📬 Contact**
For questions or issues, please **open an issue** on GitHub or contact me at:  
📩 **shitan.gao@edhec.com**

---

### **🎉 Now you're ready to start using the BDA Project! Happy coding! 🚀**
---

## **🆕 Key Updates in This Version**
✅ **Added missing features** such as `fetch-rates`, `upload-file`, and `upload-data`  
✅ **Updated project structure** to reflect all modules  
✅ **Expanded Makefile commands** for better automation  
✅ **Improved installation & setup instructions** for new users  

This **README.md** is now fully detailed and structured for both **beginners** and **experienced developers**. Let me know if you need any modifications! 🚀🔥