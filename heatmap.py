import seaborn as sns
import matplotlib.pyplot as plt

# ヒートマップの描画
plt.figure(figsize=(10, 8))  # 図のサイズを設定
sns.heatmap(df, annot=True, cmap="coolwarm", fmt="d", linewidths=.5)

# タイトルを設定
plt.title("職種ごとの単語出現頻度のヒートマップ")

# グラフの表示
plt.show()
