# Modern Mill Monte Carlo Simulation 🎲

Monte Carlo simulation and data analysis for a **Modern MtG Mill deck**.  
This project  simulates thousands of games **without opponent interaction** and does statistical analysis on the resulting data.

---
## 📂 Project Structure

```plaintext
monte_carlo_mill/
├── code/              # Core Python simulation scripts
├── data/              # Generated datasets (ignored in Git, can be regenerated)
├── notebooks/         # Jupyter notebooks for analysis & visualization
├── results/           # Output: plots, figures, HTML exports (from notebooks)
├── requirements.txt   # Python dependencies for simulation & analysis
├── .gitignore         # Ignore rules (keeps large/scratch files out of Git)
└── README.md          # Project documentation

text
---
## ⚡ Getting Started

### 1. Clone the repository
Use SSH:

git clone git@github.com:altinus01/modern-mill-monte-carlo.git
cd modern-mill-monte-carlo

### 2. Create environment & install dependencies
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows (PowerShell)
pip install -r requirements.txt

### 3. Run the simulation
cd code
python simulation.py

### 4. Analyze results
jupyter notebook notebooks/


✨ Features
Monte Carlo engine simulating thousands of games
Flexible deck setup
Generates detailed CSV outputs
Results explored via Jupyter notebooks (plots, histograms, descriptive stats)
Modular code for easy modification of rules/parameters

📊 Example Outputs
Expected turns to win via mill
Outlier analysis (low/mid/high probability outcomes)

🚫 Data & Storage Notice
Large raw datasets (data/*.csv) are not tracked in Git because they exceed GitHub’s size limits.
They can be regenerated locally by running the simulation or downloaded if shared via release assets.

🔮 Future Improvements
Add opponent interaction (disruption effects, counter-play)
Parameterize deck strategies
Optimize simulation performance
Automate result visualization

📄 License
This project is licensed under the MIT License – see LICENSE for details.
