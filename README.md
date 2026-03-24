# Google Sustainability Analytics System

This project is an automated end-to-end Python pipeline designed to analyze building energy consumption and provide sustainability recommendations. It uses unsupervised machine learning (PCA and K-Means clustering) to segment buildings based on their energy profiles and automatically generates professional reports for stakeholders.

### What it does

The system processes raw smart-meter data to identify energy-intensive behaviors. By clustering buildings into distinct profiles (e.g., "High Standby Load" or "Peak-Heavy Consumption"), it can target specific sustainability recommendations. Finally, it automates the most tedious part of the process: bridging pure data science analysis into a formatted PowerPoint deck.

### Key Features

- **Machine Learning Pipeline:** Uses Principal Component Analysis (PCA) for dimensionality reduction and K-Means for building segmentation.
- **Interactive Dashboard:** Built with **Streamlit** and **Plotly** to visualize cluster distributions, explained variance, and individual building "deep-dives."
- **Automated Synthesis:** Uses **python-pptx** to dynamically generate slides containing charts and model-driven suggestions.
- **Data Engineering:** Includes scripts for generating synthetic meter data and cleaning raw appliance-level readings.

### Project Structure

- `eda.ipynb` & `train_model.ipynb`: The research core where the data is analyzed and the Scikit-Learn models are trained and saved.
- `app.py`: The main entry point for the Streamlit dashboard, providing a visual interface for the model's findings.
- `recommend.py`: The logic engine that maps cluster features to specific, human-readable sustainability actions.
- `build_pptx.py` & `generate_charts.py`: The automation layer that converts data frames and Plotly figures into a standalone presentation file.
- `generate_data.py`: A utility to simulate realistic smart-meter telemetry for testing the pipeline.

### Why this project exists

In real-world sustainability consulting, moving from a data-heavy analysis to a client-ready presentation is usually a manual bottleneck. This project demonstrates how to automate that entire lifecycle—from the first line of raw data code to the final slide deck.
