# build_ppt.py
# Creates a self-contained HTML presentation with embedded chart images
import base64, os

CHARTS_DIR = "charts"

def img_to_b64(filename):
    path = os.path.join(CHARTS_DIR, filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

pca_var = img_to_b64("pca_variance.png")
k_sweep = img_to_b64("k_sweep.png")
pca_clust = img_to_b64("pca_clusters.png")
sil_box = img_to_b64("silhouette_box.png")
heatmap = img_to_b64("cluster_heatmap.png")
counts = img_to_b64("cluster_counts.png")
loadings = img_to_b64("pca_loadings.png")
feat_imp = img_to_b64("feature_importance.png")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Google Sustainability Analytics - Presentation</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Inter', -apple-system, sans-serif;
  background: #0a0a0a;
  color: #e2e8f0;
  overflow: hidden;
  height: 100vh;
}}

.slide {{
  display: none;
  width: 100vw;
  height: 100vh;
  padding: 50px 70px;
  position: relative;
  overflow: hidden;
}}

.slide.active {{ display: flex; flex-direction: column; }}

/* Title slide */
.slide-title {{
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #0f172a 100%);
  justify-content: center;
  align-items: center;
  text-align: center;
}}
.slide-title h1 {{
  font-size: 52px;
  font-weight: 800;
  background: linear-gradient(135deg, #818cf8, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
  margin-bottom: 20px;
}}
.slide-title .subtitle {{
  font-size: 22px;
  color: #94a3b8;
  font-weight: 400;
  margin-bottom: 40px;
}}
.slide-title .meta {{
  font-size: 15px;
  color: #64748b;
}}

/* Standard slides */
.slide-std {{
  background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
}}
.slide-std h2 {{
  font-size: 34px;
  font-weight: 700;
  margin-bottom: 30px;
  color: #f1f5f9;
}}
.slide-std h2 span {{
  background: linear-gradient(135deg, #818cf8, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.content {{ flex: 1; display: flex; gap: 40px; align-items: center; }}
.content-full {{ flex: 1; display: flex; flex-direction: column; gap: 20px; }}

.text-col {{ flex: 1; }}
.img-col {{ flex: 1.2; display: flex; align-items: center; justify-content: center; }}
.img-col img {{ max-width: 100%; max-height: 70vh; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }}
.img-full {{ max-width: 90%; max-height: 60vh; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }}

.point {{
  padding: 14px 20px;
  background: rgba(99, 102, 241, 0.08);
  border-left: 3px solid #6366f1;
  border-radius: 0 8px 8px 0;
  margin-bottom: 12px;
  font-size: 16px;
  line-height: 1.5;
  color: #cbd5e1;
}}
.point strong {{ color: #a5b4fc; }}

.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; flex: 1; }}
.grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; flex: 1; }}

.card {{
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 24px;
}}
.card h3 {{
  font-size: 16px;
  color: #818cf8;
  margin-bottom: 10px;
  font-weight: 600;
}}
.card p {{ font-size: 14px; line-height: 1.6; color: #94a3b8; }}

.stat-row {{
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-top: 20px;
}}
.stat {{
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  padding: 20px 30px;
  text-align: center;
}}
.stat .num {{
  font-size: 32px;
  font-weight: 800;
  background: linear-gradient(135deg, #818cf8, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}
.stat .label {{ font-size: 13px; color: #94a3b8; margin-top: 4px; }}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}}
table th {{
  text-align: left;
  padding: 10px 14px;
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  font-weight: 600;
  border-bottom: 2px solid #334155;
}}
table td {{
  padding: 8px 14px;
  border-bottom: 1px solid #1e293b;
  color: #cbd5e1;
}}
table tr:hover td {{ background: rgba(99, 102, 241, 0.05); }}

/* Navigation */
.nav {{
  position: fixed;
  bottom: 24px;
  right: 30px;
  display: flex;
  gap: 10px;
  z-index: 100;
}}
.nav button {{
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #e2e8f0;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
}}
.nav button:hover {{ background: rgba(99, 102, 241, 0.4); }}

.slide-num {{
  position: fixed;
  bottom: 28px;
  left: 30px;
  font-size: 14px;
  color: #475569;
  z-index: 100;
}}

.accent {{ color: #818cf8; }}
.cyan {{ color: #22d3ee; }}
.green {{ color: #10b981; }}

/* end slide */
.slide-end {{
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #0f172a 100%);
  justify-content: center;
  align-items: center;
  text-align: center;
}}
.slide-end h1 {{
  font-size: 48px;
  font-weight: 800;
  background: linear-gradient(135deg, #818cf8, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 20px;
}}
</style>
</head>
<body>

<!-- SLIDE 1: TITLE -->
<div class="slide slide-title active" id="s1">
  <h1>Google Sustainability Analytics<br>Suggestion System</h1>
  <p class="subtitle">PCA + K-Means Clustering for Smart Building Energy Segmentation</p>
  <p class="meta">AI/ML Project Presentation</p>
</div>

<!-- SLIDE 2: PROBLEM STATEMENT -->
<div class="slide slide-std" id="s2">
  <h2><span>Problem</span> Statement</h2>
  <div class="content-full">
    <div class="point"><strong>The Challenge:</strong> Buildings account for over 30% of global energy consumption and 55% of global electricity demand, yet most lack data-driven energy management strategies.</div>
    <div class="point"><strong>Why it matters:</strong> Every building wastes energy differently. A residential apartment's problems are nothing like an office's. You cant give everyone the same generic advice and expect results.</div>
    <div class="point"><strong>Our Solution:</strong> Use unsupervised machine learning (PCA + K-Means) to automatically discover energy consumption patterns, group buildings by their energy "personality", and generate personalized sustainability recommendations for each group.</div>
    <div class="stat-row">
      <div class="stat"><div class="num">30%+</div><div class="label">Global Energy by Buildings</div></div>
      <div class="stat"><div class="num">55%</div><div class="label">Electricity Demand</div></div>
      <div class="stat"><div class="num">15-30%</div><div class="label">Potential Savings</div></div>
    </div>
  </div>
</div>

<!-- SLIDE 3: PROJECT WORKFLOW -->
<div class="slide slide-std" id="s3">
  <h2><span>Project</span> Workflow</h2>
  <div class="content-full">
    <div class="grid-3" style="margin-bottom: 20px;">
      <div class="card"><h3>1. Data Generation</h3><p>Simulated 30 days of 15-minute smart meter readings for 25 buildings, covering 11 appliance types across residential, office, and mixed-use building types.</p></div>
      <div class="card"><h3>2. Feature Engineering</h3><p>Extracted 11 meaningful features from raw power readings: avg_kw, peak_kw, base_kw, load_factor, variability, peak hour, peak-to-offpeak ratio, weekend ratio, HVAC/standby/shiftable shares.</p></div>
      <div class="card"><h3>3. Preprocessing</h3><p>Applied StandardScaler (mean=0, std=1) to normalize all features to the same scale, preventing high-magnitude features from dominating the analysis.</p></div>
    </div>
    <div class="grid-3">
      <div class="card"><h3>4. PCA Reduction</h3><p>Reduced 11 features to 4 principal components capturing 94.8% of total variance. This removes noise and correlation while enabling 2D visualization.</p></div>
      <div class="card"><h3>5. K-Means Clustering</h3><p>Applied K-Means on PCA-transformed data. Swept k=2 to k=10 and selected k=8 based on highest silhouette score (0.598).</p></div>
      <div class="card"><h3>6. Recommendations</h3><p>Rule-based recommendation engine analyzes each building's cluster profile and appliance usage to generate targeted sustainability advice.</p></div>
    </div>
  </div>
</div>

<!-- SLIDE 4: DATA & FEATURES -->
<div class="slide slide-std" id="s4">
  <h2><span>Data</span> & Feature Engineering</h2>
  <div class="content">
    <div class="text-col">
      <div class="point"><strong>Data:</strong> 25 buildings, 30 days, 15-min intervals, 11 appliance types (HVAC, Fridge, EV Charger, Washer, Lighting, etc.)</div>
      <div class="point" style="margin-top: 10px;"><strong>11 Engineered Features:</strong></div>
      <table style="margin-top: 8px;">
        <tr><th>Feature</th><th>What It Captures</th></tr>
        <tr><td>avg_kw, peak_kw, base_kw</td><td>Consumption magnitude</td></tr>
        <tr><td>load_factor</td><td>How flat vs peaky the load is</td></tr>
        <tr><td>variability_cv</td><td>How unpredictable usage is</td></tr>
        <tr><td>peak_hour_mode</td><td>When peak demand occurs</td></tr>
        <tr><td>peak_to_offpeak_ratio</td><td>Evening vs night usage ratio</td></tr>
        <tr><td>weekend_weekday_ratio</td><td>Occupancy pattern indicator</td></tr>
        <tr><td>hvac/standby/shiftable share</td><td>Appliance category breakdown</td></tr>
      </table>
    </div>
    <div class="img-col">
      <img src="data:image/png;base64,{feat_imp}" alt="Feature Importance">
    </div>
  </div>
</div>

<!-- SLIDE 5: PCA EXPLAINED -->
<div class="slide slide-std" id="s5">
  <h2><span>PCA</span> - Dimensionality Reduction</h2>
  <div class="content">
    <div class="text-col">
      <div class="point"><strong>What PCA does:</strong> Finds the directions in which the data varies the most, and projects everything onto those axes. Think of it as finding the "most informative camera angles" for your data.</div>
      <div class="point"><strong>Why we need it:</strong> 11 features is too many dimensions to visualize or cluster effectively. PCA compresses them to 4 components while keeping 94.8% of the information.</div>
      <div class="point"><strong>PC1 (57.8%):</strong> Captures overall building size and consumption level (avg_kw, peak_kw, base_kw)</div>
      <div class="point"><strong>PC2 (21.2%):</strong> Captures behavioral patterns (weekend ratio, variability, shiftable share)</div>
    </div>
    <div class="img-col">
      <img src="data:image/png;base64,{pca_var}" alt="PCA Explained Variance">
    </div>
  </div>
</div>

<!-- SLIDE 6: PCA LOADINGS -->
<div class="slide slide-std" id="s6">
  <h2><span>PCA</span> Loadings: What Drives Each Component</h2>
  <div class="content-full">
    <img class="img-full" src="data:image/png;base64,{loadings}" alt="PCA Loadings">
    <div class="point" style="max-width: 900px; margin: 0 auto;"><strong>How to read this:</strong> Each bar shows how strongly a feature contributes to that PC. PC1 is driven by power metrics and HVAC share (building size). PC2 is driven by weekend ratio, variability, and shiftable share (behavioral patterns).</div>
  </div>
</div>

<!-- SLIDE 7: K-MEANS ALGORITHM -->
<div class="slide slide-std" id="s7">
  <h2><span>K-Means</span> Clustering Algorithm</h2>
  <div class="content">
    <div class="text-col">
      <div class="point"><strong>What K-Means does:</strong> Groups data points into k clusters by minimizing within-cluster distances. Its unsupervised - no labels needed.</div>
      <div class="point"><strong>Algorithm steps:</strong><br>
        1. Pick k random centroids<br>
        2. Assign each building to its nearest centroid<br>
        3. Move each centroid to the mean of its cluster<br>
        4. Repeat 2-3 until convergence</div>
      <div class="point"><strong>Choosing k:</strong> We swept k=2 to k=10 and evaluated using silhouette score (cluster separation quality) and inertia (compactness). k=8 gave the best silhouette score of 0.598.</div>
      <div class="point"><strong>Objective:</strong> Minimize J = sum of squared distances from each point to its cluster centroid</div>
    </div>
    <div class="img-col">
      <img src="data:image/png;base64,{k_sweep}" alt="K Sweep">
    </div>
  </div>
</div>

<!-- SLIDE 8: CLUSTER VISUALIZATION -->
<div class="slide slide-std" id="s8">
  <h2><span>Cluster</span> Visualization in PCA Space</h2>
  <div class="content">
    <div class="text-col">
      <div class="point"><strong>What this shows:</strong> Each dot is a building, projected onto PC1 vs PC2. Colors represent the cluster each building was assigned to.</div>
      <div class="point"><strong>Key observation:</strong> Buildings on the right (high PC1) are high-consumption buildings. Buildings on the left are low-consumption. The vertical spread (PC2) separates by behavioral pattern.</div>
      <div class="point"><strong>Clear separation:</strong> Most clusters form distinct, visually separable groups, confirming that our PCA + K-Means pipeline found real, meaningful patterns in the data.</div>
    </div>
    <div class="img-col">
      <img src="data:image/png;base64,{pca_clust}" alt="PCA Clusters">
    </div>
  </div>
</div>

<!-- SLIDE 9: EVALUATION -->
<div class="slide slide-std" id="s9">
  <h2><span>Evaluation</span> Metrics</h2>
  <div class="content">
    <div class="text-col">
      <div class="point"><strong>Silhouette Score (0.598):</strong> Measures how well-separated the clusters are. Ranges from -1 to +1. Above 0.5 indicates strong cluster structure.</div>
      <div class="point"><strong>How it works:</strong> For each building, compares the average distance to buildings in its own cluster vs the nearest other cluster. Higher = better separation.</div>
      <div class="point"><strong>Per-cluster analysis:</strong> Clusters 3-5 and 7 have scores above 0.7 (excellent fit). Clusters 0-1 are around 0.15-0.20, indicating some overlap between small-building profiles.</div>
      <div class="stat-row">
        <div class="stat"><div class="num">0.598</div><div class="label">Silhouette Score</div></div>
        <div class="stat"><div class="num">8</div><div class="label">Optimal k</div></div>
        <div class="stat"><div class="num">94.8%</div><div class="label">PCA Variance</div></div>
      </div>
    </div>
    <div class="img-col">
      <img src="data:image/png;base64,{sil_box}" alt="Silhouette Box Plot">
    </div>
  </div>
</div>

<!-- SLIDE 10: CLUSTER PROFILES -->
<div class="slide slide-std" id="s10">
  <h2><span>Cluster</span> Profiles Heatmap</h2>
  <div class="content-full">
    <img class="img-full" src="data:image/png;base64,{heatmap}" alt="Cluster Heatmap">
    <div style="display: flex; gap: 20px; justify-content: center; margin-top: 10px;">
      <div class="point" style="flex: 1; max-width: 420px;"><strong>Cluster 0:</strong> Low consumption, low load factor, high standby share - small buildings with lots of always-on devices</div>
      <div class="point" style="flex: 1; max-width: 420px;"><strong>Cluster 3:</strong> Highest avg_kw, high HVAC share, high load factor - large HVAC-dominated buildings with steady consumption</div>
      <div class="point" style="flex: 1; max-width: 420px;"><strong>Cluster 5:</strong> Very high peak, highest peak-to-offpeak ratio - extremely peaky buildings needing load shifting</div>
    </div>
  </div>
</div>

<!-- SLIDE 11: RECOMMENDATIONS -->
<div class="slide slide-std" id="s11">
  <h2><span>Sustainability</span> Recommendations</h2>
  <div class="content">
    <div class="text-col">
      <div class="point"><strong>Building-Level Rules:</strong> Based on cluster features, the system triggers specific recommendations when thresholds are crossed.</div>
      <table style="margin-top: 12px;">
        <tr><th>Condition Detected</th><th>Recommendation</th></tr>
        <tr><td>Peak-to-offpeak > 1.7</td><td>Shift flexible loads to off-peak hours</td></tr>
        <tr><td>Base load > 0.55 kW + high standby</td><td>Investigate always-on devices, use smart strips</td></tr>
        <tr><td>HVAC share > 40%</td><td>Tune setpoints, improve insulation</td></tr>
        <tr><td>High variability (CV > 0.9)</td><td>Stagger high-power appliances</td></tr>
        <tr><td>Peak in evening window</td><td>Pre-cool/heat earlier, reduce simultaneous loads</td></tr>
      </table>
      <div class="point" style="margin-top: 12px;"><strong>Appliance Diagnostics:</strong> Detects frequent short cycles, excessive standby, and peak-hour concentration for each individual appliance.</div>
    </div>
    <div class="img-col">
      <img src="data:image/png;base64,{counts}" alt="Cluster Counts">
    </div>
  </div>
</div>

<!-- SLIDE 12: TECH STACK & DASHBOARD -->
<div class="slide slide-std" id="s12">
  <h2><span>Technology</span> Stack & Dashboard</h2>
  <div class="content-full">
    <div class="grid-2">
      <div>
        <div class="point"><strong>Tech Stack:</strong></div>
        <table style="margin-top: 10px;">
          <tr><th>Technology</th><th>Purpose</th></tr>
          <tr><td>Python</td><td>Core programming language</td></tr>
          <tr><td>pandas + NumPy</td><td>Data manipulation & feature engineering</td></tr>
          <tr><td>scikit-learn</td><td>PCA, K-Means, Silhouette scoring</td></tr>
          <tr><td>joblib</td><td>Model serialization (save/load models)</td></tr>
          <tr><td>Streamlit</td><td>Interactive web dashboard</td></tr>
          <tr><td>Plotly</td><td>Interactive data visualizations</td></tr>
        </table>
      </div>
      <div>
        <div class="point"><strong>Dashboard (Streamlit app):</strong></div>
        <div class="card" style="margin-top: 10px;"><h3>4 Interactive Tabs</h3><p>
          1. Summary - cluster bar chart + profile table<br>
          2. PCA - explained variance + 2D scatter plot<br>
          3. K-Means Quality - k-sweep + silhouette analysis<br>
          4. Building Deep-Dive - select any building, see its load curve, appliance breakdown, and personalized recommendations
        </p></div>
        <div class="card" style="margin-top: 10px;"><h3>Upload Your Own Data</h3><p>
          The dashboard also accepts CSV uploads and classifies new buildings on-the-fly using the saved PCA + K-Means model.
        </p></div>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 13: CONCLUSION -->
<div class="slide slide-std" id="s13">
  <h2><span>Conclusion</span> & Key Takeaways</h2>
  <div class="content-full">
    <div class="grid-2" style="margin-bottom: 20px;">
      <div class="card"><h3>What We Achieved</h3><p>
        Built a complete end-to-end ML pipeline: from synthetic data generation through feature engineering, PCA dimensionality reduction, K-Means clustering, to a web-based recommendation dashboard.
      </p></div>
      <div class="card"><h3>Why Unsupervised Learning</h3><p>
        Real building data rarely comes with labels. Unsupervised clustering discovers natural patterns without needing pre-labeled training data, making it practical for real-world energy analytics deployment.
      </p></div>
    </div>
    <div class="grid-2">
      <div class="card"><h3>Key Results</h3><p>
        8 distinct energy profiles identified. Silhouette score of 0.598 (strong separation). PCA captured 94.8% of variance in just 4 components. Standby share and avg_kw identified as most influential features.
      </p></div>
      <div class="card"><h3>Sustainability Impact</h3><p>
        Targeted recommendations per cluster enable 15-30% energy savings. Load shifting, HVAC optimization, and standby reduction are the top three actionable strategies.
      </p></div>
    </div>
    <div class="stat-row" style="margin-top: 10px;">
      <div class="stat"><div class="num">11</div><div class="label">Features Engineered</div></div>
      <div class="stat"><div class="num">8</div><div class="label">Clusters Identified</div></div>
      <div class="stat"><div class="num">0.598</div><div class="label">Silhouette Score</div></div>
      <div class="stat"><div class="num">94.8%</div><div class="label">PCA Variance</div></div>
      <div class="stat"><div class="num">25</div><div class="label">Buildings Analyzed</div></div>
    </div>
  </div>
</div>

<!-- SLIDE 14: THANK YOU -->
<div class="slide slide-end" id="s14">
  <h1>Thank You!</h1>
  <p class="subtitle" style="color: #94a3b8; font-size: 20px;">Google Sustainability Analytics Suggestion System</p>
  <p style="color: #64748b; margin-top: 20px;">PCA + K-Means Clustering for Smart Building Energy Segmentation</p>
</div>

<!-- Navigation -->
<div class="nav">
  <button onclick="prev()">&larr;</button>
  <button onclick="next()">&rarr;</button>
</div>
<div class="slide-num" id="slideNum">1 / 14</div>

<script>
let cur = 0;
const slides = document.querySelectorAll('.slide');
const total = slides.length;

function show(n) {{
  slides[cur].classList.remove('active');
  cur = ((n % total) + total) % total;
  slides[cur].classList.add('active');
  document.getElementById('slideNum').textContent = (cur + 1) + ' / ' + total;
}}

function next() {{ show(cur + 1); }}
function prev() {{ show(cur - 1); }}

document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight' || e.key === ' ') next();
  if (e.key === 'ArrowLeft') prev();
  if (e.key === 'Home') show(0);
  if (e.key === 'End') show(total - 1);
}});
</script>
</body>
</html>"""

with open("presentation.html", "w") as f:
    f.write(html)

print("Created presentation.html")
print(f"Total slides: 14")
print(f"Open in browser: file:///Users/lagmator22/Google-Sustainability-Analytics-Suggestion-system/presentation.html")
