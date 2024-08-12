# Nginx Log Analysis

This repository contains two scripts for analyzing Nginx logs: `Parse-nginx.py` and `nginx_streamLit.py`.

## Parse-nginx.py

`Parse-nginx.py` is a script designed to parse Nginx access and error logs. It extracts relevant information such as source IP, timestamp, status codes, and error messages from the logs and stores the parsed data for further analysis.

### Features

- Parses Nginx access logs and extracts source IP, timestamp, status codes, request size, response size, and upstream IP.
- Parses Nginx error logs and extracts timestamp, error level, request ID, error message, source IP, and upstream IP.
- Stores the parsed data in a structured format for further analysis.

### Usage

1. **Set the Log Directory**:
   - Ensure that the `log_dir` variable in the script points to the directory containing your Nginx log files.

2. **Run the Script**:
   - Execute the script using Python:
     ```sh
     python Parse-nginx.py
     ```

## nginx_streamLit.py

`nginx_streamLit.py` is a Streamlit application that provides a visual analysis of the parsed Nginx logs. It displays various charts and tables to help you understand the most troublesome connections and other relevant metrics.

### Features

- Displays the most troublesome connections based on the number of failed requests.
- Shows a bar chart of problematic connections per IP address.
- Displays a pie chart of the most problematic source IPs and upstream IPs.
- Plots the number of problematic connections over time.
- Provides a detailed view of affected IPs during the period.

### Usage

1. **Ensure Dependencies**:
   - Install the required dependencies using the `requirements.txt` file:
     ```sh
     pip install -r requirements.txt
     ```

2. **Run the Streamlit Application**:
   - Execute the Streamlit application:
     ```sh
     streamlit run nginx_streamLit.py
     ```

3. **View the Application**:
   - Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`):
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `tqdm`

## Installation

1. **Clone the Repository**:
   - Clone this repository to your local machine:
     ```sh
     git clone https://github.com/yourusername/nginx-log-analysis.git
     cd nginx-log-analysis
     ```

2. **Install Dependencies**:
   - Install the required Python packages:
     ```sh
     pip install -r requirements.txt
     ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [TQDM](https://tqdm.github.io/)
