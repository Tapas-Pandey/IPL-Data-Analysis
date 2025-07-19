---

# 🏏 IPL Data Analysis Dashboard (2008–2024)

An interactive, visually rich **IPL Data Analysis Dashboard** built with **Streamlit**, **Pandas**, **Plotly**, and **Seaborn**. It leverages official match and delivery data from IPL seasons **2008 through 2024** to help fans, analysts, and developers explore performance trends, player stats, head-to-head comparisons, venue records, and more.

---

## 📁 Dataset Source

* Data used:

  * `matches.csv` – match-level information (season, date, teams, result, etc.)
  * `deliveries.csv` – ball-by-ball delivery-level data

> 📌 Dataset has been updated to include all IPL matches up to and including **IPL 2024**.

---

## 🚀 Features

### 📊 Team & Match Insights

* Filter matches by **team** and **season**
* See wins, toss decisions, and MVPs per year
* Head-to-head breakdown between any two teams

### 🧮 Key Performance Indicators (KPIs)

* Total matches, win %, most runs/wickets in history
* Dynamic cards for each season and team

### 🔍 Player Analytics

* Search any player (batter or bowler)
* View total runs, strike rate, 4s/6s, wickets, economy, and matches played

### 🆚 Team Comparison Tool

* Compare two teams on:

  * Total wins, average runs/wickets
  * Top batters and bowlers
  * Head-to-head stats

### 🏟️ Venue Analysis

* Matches per venue
* Team-wise win percentage across stadiums

### ⚔️ Player vs Player (PvP)

* Analyze how a batter performed against a specific bowler
* Track runs, balls faced, strike rate, boundaries, dismissals

---

## 🛠️ Tech Stack

| Tool                     | Purpose                   |
| ------------------------ | ------------------------- |
| `Streamlit`              | Web app framework         |
| `Pandas`                 | Data manipulation         |
| `Plotly`                 | Interactive plots         |
| `Matplotlib` & `Seaborn` | Static plots and heatmaps |
| `CSV` files              | Raw data input            |

---

## 📸 Screenshots

| Dashboard Sections       | Preview                                 |
| ------------------------ | --------------------------------------- |
| KPI Cards + Team Filters | ![KPI Section](docs/kpi-section.png)    |
| Player Search            | ![Player Stats](docs/player-search.png) |
| Head-to-Head             | ![H2H](docs/h2h-comparison.png)         |

> *(You can capture your own screenshots and place them in a `/docs/` folder to link them above.)*

---

## 🏁 Getting Started

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/ipl-dashboard.git
cd ipl-dashboard
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add your dataset

Place the following files in the project root:

* `matches.csv`
* `deliveries.csv`

These can be sourced from [Kaggle IPL Dataset](https://www.kaggle.com/datasets) or your own compiled IPL 2008–2024 records.

### 4️⃣ Run the app

```bash
streamlit run main.py
```

---

## 📦 Folder Structure

```
.
├── main.py               # Main Streamlit app
├── matches.csv           # IPL match data (till 2024)
├── deliveries.csv        # Ball-by-ball data (till 2024)
├── requirements.txt      # Python dependencies
└── README.md             # You’re here!
```

---

## ✅ To-Do / Improvements

* [ ] Add download/export buttons for filtered data
* [ ] Incorporate live match data using API (e.g., Cricbuzz, ESPNcricinfo)
* [ ] Deploy on Streamlit Cloud or HuggingFace Spaces
* [ ] Add predictive modeling for match outcome

---

## 🤝 Contributing

Feel free to fork, improve, and open pull requests. For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

* [Kaggle IPL Dataset](https://www.kaggle.com/datasets)
* Streamlit Community & Open Source Contributors
* IPL fans and data science enthusiasts 🎉

---
