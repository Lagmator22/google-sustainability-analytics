# generate_charts.py
# Produces all key charts as PNG images for the presentation
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT = "charts"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "#0f172a",
    "axes.facecolor": "#1e293b",
    "axes.edgecolor": "#334155",
    "text.color": "#e2e8f0",
    "axes.labelcolor": "#e2e8f0",
    "xtick.color": "#94a3b8",
    "ytick.color": "#94a3b8",
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "grid.color": "#334155",
    "grid.alpha": 0.5,
})

COLORS = ["#6366f1", "#22d3ee", "#f59e0b", "#ef4444", "#10b981",
          "#a78bfa", "#f472b6", "#14b8a6"]

# Load all artifacts
pca_ev = pd.read_csv("artifacts/pca_explained_variance.csv")
k_sweep = pd.read_csv("artifacts/k_sweep.csv")
scores2d = pd.read_csv("artifacts/pca_scores_2d.csv")
sil = pd.read_csv("artifacts/silhouette_samples.csv")
profiles = pd.read_csv("artifacts/cluster_profiles.csv")
segments = pd.read_csv("artifacts/building_segments.csv")
loadings = pd.read_csv("artifacts/pca_loadings.csv", index_col=0)


# 1. PCA Explained Variance
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(pca_ev["component"], pca_ev["explained_variance_ratio"],
              color=COLORS[:len(pca_ev)], edgecolor="none", width=0.6, label="Individual")
ax.plot(pca_ev["component"], pca_ev["cumulative_explained_variance"],
        "o-", color="#22d3ee", linewidth=2.5, markersize=8, label="Cumulative")
for i, v in enumerate(pca_ev["explained_variance_ratio"]):
    ax.text(i + 1, v + 0.02, f"{v:.1%}", ha="center", fontsize=10, color="#e2e8f0")
cum_last = pca_ev["cumulative_explained_variance"].iloc[-1]
ax.axhline(y=0.95, color="#ef4444", linestyle="--", alpha=0.6, label="95% threshold")
ax.set_xlabel("Principal Component")
ax.set_ylabel("Variance Explained")
ax.set_title("PCA Explained Variance")
ax.legend(loc="center right")
ax.set_ylim(0, 1.1)
ax.grid(axis="y")
fig.tight_layout()
fig.savefig(f"{OUT}/pca_variance.png", dpi=200)
plt.close()
print("Saved pca_variance.png")


# 2. K-Sweep (Elbow + Silhouette)
fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()
ax1.plot(k_sweep["k"], k_sweep["inertia"], "s-", color="#ef4444",
         linewidth=2, markersize=7, label="Inertia (WCSS)")
ax2.plot(k_sweep["k"], k_sweep["silhouette"], "o-", color="#22d3ee",
         linewidth=2, markersize=7, label="Silhouette Score")
# highlight best k
best_k = k_sweep.loc[k_sweep["silhouette"].idxmax(), "k"]
best_sil = k_sweep["silhouette"].max()
ax2.axvline(x=best_k, color="#10b981", linestyle="--", alpha=0.7)
ax2.annotate(f"Best k={int(best_k)}\nSil={best_sil:.3f}",
             xy=(best_k, best_sil), xytext=(best_k + 0.8, best_sil - 0.04),
             arrowprops=dict(arrowstyle="->", color="#10b981"),
             fontsize=10, color="#10b981")
ax1.set_xlabel("Number of Clusters (k)")
ax1.set_ylabel("Inertia", color="#ef4444")
ax2.set_ylabel("Silhouette Score", color="#22d3ee")
ax1.set_title("Choosing Optimal k: Elbow Method + Silhouette Score")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")
ax1.grid(axis="y")
fig.tight_layout()
fig.savefig(f"{OUT}/k_sweep.png", dpi=200)
plt.close()
print("Saved k_sweep.png")


# 3. PCA 2D Scatter (Clusters)
fig, ax = plt.subplots(figsize=(8, 6))
clusters = sorted(scores2d["cluster"].unique())
for c in clusters:
    mask = scores2d["cluster"] == c
    ax.scatter(scores2d.loc[mask, "pc1"], scores2d.loc[mask, "pc2"],
               c=COLORS[c % len(COLORS)], label=f"Cluster {c}",
               s=90, edgecolors="white", linewidth=0.5, alpha=0.85)
ax.set_xlabel("PC1 (57.8% variance)")
ax.set_ylabel("PC2 (21.2% variance)")
ax.set_title("Building Clusters in PCA Space")
ax.legend(fontsize=8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.12))
ax.grid(True)
fig.tight_layout(rect=[0, 0.08, 1, 1])
fig.savefig(f"{OUT}/pca_clusters.png", dpi=200)
plt.close()
print("Saved pca_clusters.png")


# 4. Silhouette by Cluster (box plot)
fig, ax = plt.subplots(figsize=(8, 5))
cluster_ids = sorted(sil["cluster"].unique())
data_by_cluster = [sil[sil["cluster"] == c]["silhouette"].values for c in cluster_ids]
bp = ax.boxplot(data_by_cluster, labels=[f"C{c}" for c in cluster_ids],
                patch_artist=True, showmeans=True,
                meanprops=dict(marker="D", markerfacecolor="#f59e0b", markersize=6))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(COLORS[i % len(COLORS)])
    patch.set_alpha(0.7)
ax.axhline(y=sil["silhouette"].mean(), color="#22d3ee", linestyle="--", alpha=0.6,
           label=f"Overall mean = {sil['silhouette'].mean():.3f}")
ax.set_xlabel("Cluster")
ax.set_ylabel("Silhouette Score")
ax.set_title("Silhouette Score Distribution by Cluster")
ax.legend()
ax.grid(axis="y")
fig.tight_layout()
fig.savefig(f"{OUT}/silhouette_box.png", dpi=200)
plt.close()
print("Saved silhouette_box.png")


# 5. Cluster Profile Heatmap
FEATURES = ["avg_kw", "peak_kw", "base_kw", "load_factor", "variability_cv",
            "peak_hour_mode", "peak_to_offpeak_ratio", "weekend_weekday_ratio",
            "hvac_share", "standby_share", "shiftable_share"]
heatmap_data = profiles.set_index("cluster")[FEATURES]
# Normalize columns to 0-1 for color
normed = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min() + 1e-9)

fig, ax = plt.subplots(figsize=(12, 5))
im = ax.imshow(normed.values, aspect="auto", cmap="coolwarm", vmin=0, vmax=1)
ax.set_xticks(range(len(FEATURES)))
ax.set_xticklabels([f.replace("_", "\n") for f in FEATURES], fontsize=8, rotation=0)
ax.set_yticks(range(len(heatmap_data)))
ax.set_yticklabels([f"Cluster {c}" for c in heatmap_data.index])
ax.set_title("Cluster Profiles: Normalized Feature Heatmap")
# Add values
for i in range(normed.shape[0]):
    for j in range(normed.shape[1]):
        val = heatmap_data.values[i, j]
        color = "white" if normed.values[i, j] < 0.5 else "#1e293b"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7, color=color)
fig.colorbar(im, ax=ax, label="Low <---> High", shrink=0.8)
fig.tight_layout()
fig.savefig(f"{OUT}/cluster_heatmap.png", dpi=200)
plt.close()
print("Saved cluster_heatmap.png")


# 6. Buildings per Cluster bar chart
fig, ax = plt.subplots(figsize=(7, 4))
counts = profiles[["cluster", "count"]].sort_values("cluster")
bars = ax.bar(counts["cluster"].astype(str), counts["count"],
              color=COLORS[:len(counts)], edgecolor="none")
for bar, cnt in zip(bars, counts["count"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            str(int(cnt)), ha="center", fontsize=11, color="#e2e8f0")
ax.set_xlabel("Cluster")
ax.set_ylabel("Number of Buildings")
ax.set_title("Buildings per Cluster")
ax.grid(axis="y")
fig.tight_layout()
fig.savefig(f"{OUT}/cluster_counts.png", dpi=200)
plt.close()
print("Saved cluster_counts.png")


# 7. PCA Loadings (what features drive each PC)
fig, ax = plt.subplots(figsize=(10, 4))
x = np.arange(len(FEATURES))
width = 0.2
for i, pc in enumerate(loadings.index[:4]):
    vals = loadings.loc[pc, FEATURES].values
    ax.bar(x + i * width, vals, width, label=pc, color=COLORS[i], alpha=0.85)
ax.set_xticks(x + 1.5 * width)
ax.set_xticklabels([f.replace("_", "\n") for f in FEATURES], fontsize=7)
ax.axhline(y=0, color="#94a3b8", linewidth=0.5)
ax.set_ylabel("Loading Value")
ax.set_title("PCA Loadings: Which Features Drive Each Component")
ax.legend(fontsize=9)
ax.grid(axis="y")
fig.tight_layout()
fig.savefig(f"{OUT}/pca_loadings.png", dpi=200)
plt.close()
print("Saved pca_loadings.png")


# 8. Feature importance style chart (using PC1 absolute loadings)
pc1_abs = loadings.loc["PC1", FEATURES].abs().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(range(len(pc1_abs)), pc1_abs.values,
               color=COLORS[0], edgecolor="none", height=0.6)
ax.set_yticks(range(len(pc1_abs)))
ax.set_yticklabels(pc1_abs.index, fontsize=9)
for i, v in enumerate(pc1_abs.values):
    ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9, color="#e2e8f0")
ax.set_xlabel("|Loading| on PC1")
ax.set_title("Feature Importance (Absolute PC1 Loadings)")
ax.grid(axis="x")
fig.tight_layout()
fig.savefig(f"{OUT}/feature_importance.png", dpi=200)
plt.close()
print("Saved feature_importance.png")


print(f"\nAll charts saved to ./{OUT}/")
