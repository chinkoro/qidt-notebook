import streamlit as st
import os
from datetime import datetime
import yaml
import glob

def check_password():
    def password_entered():
        if st.session_state["password"] == "qidtnote123":  # ← お好みで変更
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["authenticated"]:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        st.error("パスワードが違います")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- ページ設定 ---
st.set_page_config(
    page_title="QIDTノートアプリ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- カスタムCSS（QIDTスタイル） ---
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #0b0c10;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stTextInput>div>div>input {
        background-color: #1f1f2e;
        color: white;
        border: 1px solid #444;
    }
    .stTextArea textarea {
        background-color: #1f1f2e;
        color: white;
        border: 1px solid #444;
    }
    .stButton>button {
        background-color: #0072ff;
        color: white;
        border-radius: 0.4rem;
        padding: 0.5rem 1.2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #005fcc;
    }
    </style>
""", unsafe_allow_html=True)

# --- ヘッダーと理念 ---
st.markdown("# **QIDTノートアプリ**")
st.markdown("### *Quantum Interface for Data & Thought*")
st.markdown("> “**データの本質は『結果そのもの』ではなく『そこから何を得たか』である**”")
st.markdown("---")

# --- サイドバー ---
tab = st.sidebar.radio("ナビゲーション", ["🏠 ホーム", "📝 新規記録", "📋 一覧", "📊 構造別結果", "📉 IRスペクトル可視化", "⚙️ 設定"])

# --- 保存関数 ---
def save_entry(title, body, tags):
    today = datetime.today().strftime("%Y-%m-%d")
    slug = title.replace(" ", "_")
    dir_path = f"entries/{today}"
    os.makedirs(dir_path, exist_ok=True)
    file_path = f"{dir_path}/{slug}.md"
    
    metadata = {
        "title": title,
        "date": today,
        "tags": tags,
    }

    with open(file_path, "w") as f:
        f.write("---\n")
        yaml.dump(metadata, f)
        f.write("---\n\n")
        f.write(body)

    st.success(f"✅ 記録を保存しました： `{file_path}`")

# --- 各画面処理 ---
if tab == "🏠 ホーム":
    st.subheader("QIDTへようこそ")
    st.markdown("""
    このアプリは、量子化学的な洞察と直観を記録・構造化し、
    思考の深まりと再発見を支援する **「知のインターフェース」** です。
    """)
    

# --- 各画面処理 ---

if tab == "🏠 ホーム":
    import time
    from streamlit_lottie import st_lottie
    import requests

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_molecule = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")
    st_lottie(lottie_molecule, height=250, speed=1, key="intro")

    with st.container():
        st.markdown("## **Quantum Interface Design Theory (QIDT)**")
        time.sleep(0.5)
        st.markdown("### 分子スケールで世界を設計する")
        time.sleep(0.8)
        st.write("QIDTは、電子構造理論を用いて、界面や反応場を統一的に理解・設計する理論体系です。")
        time.sleep(1.0)
        st.write("その中核にある指標は **QIDE**：")
        st.latex(r"QIDE = E_{total}^{interface} - E_{substrate} - E_{molecule}")
        time.sleep(1.2)
        st.write("- 電子密度")
        st.write("- HOMO/LUMO")
        st.write("- SCFエネルギー")
        time.sleep(1.0)
        st.markdown("> **“分子を越えて、電子のふるまいを解明し、世界の構造を設計可能な知へと昇華する”**")

    st.markdown("""
---
## QIDTの構成と応用

### 構成要素
- 分子構造（xyz座標／結合性）
- 電子密度分布（SCF結果、ESP、軌道）
- 原子間相互作用（静電・軌道相互作用）

### QIDEの定義
```math
QIDE = E_{total}^{interface} - E_{substrate} - E_{molecule}
```
- 界面の安定性・反応性を1つのスカラーで定量評価

### QIDT-Reaction テンプレート
```text
QIDT-Reaction = {S, P, TS, ΔE, Δρ, ΔOrbital, ΔQIDE}
```
- S: Reactant
- P: Product
- TS: Transition State
- ΔE: エネルギー変化
- Δρ: 電子密度差分
- ΔOrbital: HOMO/LUMO変化
- ΔQIDE: エネルギー差分

### 適用領域
- ポリエステル、MMA、PLA、エポキシ系の解重合
- 有機金属錯体の選択的切断・重合反応
- 金属酸化物表面での吸着・反応設計
- フィラーと樹脂の界面設計

---
### QIDTの目標
- 構造・電子・反応・材料特性の統一記述
- 化学における“統一場理論”として機能
- 再現性ある“設計原理”の提示

> **未来に再現できる“知”を遺すために。**
""")



elif tab == "🧪 新規記録":
    st.subheader("新規記録の作成")

    title = st.text_input("タイトル", placeholder="例：MMA-MAA界面の反応場について")
    body = st.text_area("本文（Markdown形式で記述可能）", height=300, placeholder="ここに洞察や考察、発見などを記述します。")
    tags = st.text_input("タグ（カンマ区切り）", placeholder="例：MMA, MAA, QIDT, ORCA")

    # --- 添付ファイル ---
    uploaded_files = st.file_uploader(
        "ファイル添付（画像・CSV・出力ファイルなど）",
        type=["png", "jpg", "jpeg", "csv", "out", "xyz", "txt"],
        accept_multiple_files=True
    )
    if st.button("保存"):
        if title and body:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            save_entry(title, body, tag_list)

            # --- 添付ファイル保存処理 ---
            if uploaded_files:
                from pathlib import Path
                today = datetime.today().strftime("%Y-%m-%d")
                slug = title.replace(" ", "_")
                file_dir = Path(f"entries/{today}/{slug}")
                file_dir.mkdir(parents=True, exist_ok=True)

                for file in uploaded_files:
                    file_path = file_dir / file.name
                    with open(file_path, "wb") as out_file:
                        out_file.write(file.read())

            st.success("✅ 記録と添付ファイルを保存しました")
        else:
            st.warning("⚠️ タイトルと本文は必須です。")

elif tab == "📚 一覧":
    st.subheader("記録一覧")


    entry_files = glob.glob("entries/**/*.md", recursive=True)
    if not entry_files:
        st.info("記録がまだありません。")
    else:
        # --- 一覧読み込み ---
        entries = []
        all_tags = set()
        for file_path in entry_files:
            with open(file_path, "r") as f:
                lines = f.readlines()
                if lines[0].strip() == "---":
                    meta_lines = []
                    for line in lines[1:]:
                        if line.strip() == "---":
                            break
                        meta_lines.append(line)
                    metadata = yaml.safe_load("".join(meta_lines))
                    body = "".join(lines).split("---\n")[-1]
                    tag_list = metadata.get("tags", [])
                    all_tags.update(tag_list)
                    entries.append({
                        "タイトル": metadata.get("title", "不明"),
                        "日付": metadata.get("date", "不明"),
                        "タグリスト": tag_list,
                        "タグ表示": ", ".join(tag_list),
                        "本文": body,
                        "パス": file_path
                    })

        # --- フィルターUI ---
        selected_tag = st.selectbox("タグで絞り込み", ["すべて"] + sorted(all_tags))
        selected_date = st.date_input("日付で絞り込み（任意）", value=None)

        # --- フィルター処理 ---
        filtered_entries = []
        for item in entries:
            match_tag = (selected_tag == "すべて" or selected_tag in item["タグリスト"])
            match_date = (not selected_date or item["日付"] == selected_date.strftime("%Y-%m-%d"))
            if match_tag and match_date:
                filtered_entries.append(item)

        if not filtered_entries:
            st.warning("条件に一致する記録がありません。")
        else:
            for item in filtered_entries[::-1]:
                st.markdown(f"### 🧾 {item['タイトル']}")
                st.markdown(f"🗓 {item['日付']} | 🏷 {item['タグ表示']}")

                with st.expander("📖 内容を表示 / 編集"):
                    mode = st.radio("表示モード", ["読む", "編集する"], key=item["パス"])

                    if mode == "読む":
                        st.markdown(item["本文"])
                    else:
                        new_title = st.text_input("タイトル", value=item["タイトル"], key="title_"+item["パス"])
                        new_body = st.text_area("本文", value=item["本文"], height=300, key="body_"+item["パス"])
                        new_tags = st.text_input("タグ（カンマ区切り）", value=item["タグ表示"], key="tag_"+item["パス"])

                        if st.button("保存する", key="save_"+item["パス"]):
                            metadata = {
                                "title": new_title,
                                "date": item["日付"],
                                "tags": [t.strip() for t in new_tags.split(",") if t.strip()]
                            }
                            with open(item["パス"], "w") as f:
                                f.write("---\n")
                                yaml.dump(metadata, f)
                                f.write("---\n\n")
                                f.write(new_body)
                            st.success("✅ 上書き保存しました")

                    # --- 添付ファイルの表示 ---
                    file_dir = os.path.join(os.path.dirname(item["パス"]), item["タイトル"].replace(" ", "_"))
                    if os.path.exists(file_dir):
                        st.markdown("📎 添付ファイル：")
                        for file_name in os.listdir(file_dir):
                            file_path = os.path.join(file_dir, file_name)
                            ext = file_name.split(".")[-1].lower()
                            if ext in ["png", "jpg", "jpeg"]:
                                st.image(file_path, caption=file_name, use_column_width=True)
                            else:
                                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                    file_content = f.read()

                                with st.expander(f"📥 {file_name}（クリックで展開）"):
                                    st.code(file_content, language="text")

                # 🗑 削除ボタン（確認付き）
                if st.button("🗑 この記録を削除する", key="delete_"+item["パス"]):
                    try:
                        os.remove(item["パス"])  # .mdファイル削除

                        # 添付ファイルフォルダ削除（あれば）
                        file_dir = os.path.join(os.path.dirname(item["パス"]), item["タイトル"].replace(" ", "_"))
                        if os.path.exists(file_dir):
                            import shutil
                            shutil.rmtree(file_dir)

                        st.success("✅ 記録を削除しました。ページを再読み込みしてください。")
                    except Exception as e:
                        st.error(f"⚠️ 削除中にエラーが発生しました: {e}")

                st.markdown("---")

elif tab == "📊 構造別結果":
    from pathlib import Path

    st.subheader("構造別の計算結果記録")

    # --- 入力フォーム ---
    with st.form("structure_form"):
        col1, col2 = st.columns(2)
        with col1:
            structure_name = st.text_input("構造名（例：MMA-MAA Dimer）")
            scf_energy = st.number_input("SCFエネルギー [au]", format="%.6f")
            homo = st.number_input("HOMO [au]", format="%.6f")
            lumo = st.number_input("LUMO [au]", format="%.6f")
            mulliken_max = st.number_input("Mulliken最大電荷", format="%.6f")
            mulliken_min = st.number_input("Mulliken最小電荷", format="%.6f")
            e_total = st.number_input("E_total (界面全体エネルギー) [au]", format="%.6f")
            e_sub = st.number_input("E_substrate [au]", format="%.6f")
            e_mol = st.number_input("E_molecule [au]", format="%.6f")
            dipole = st.number_input("双極子モーメント [Debye]", format="%.6f")
        with col2:
            notes = st.text_area("自由記述（電荷分布、反応性など）")
            image_file = st.file_uploader("構造画像（PNGまたはJPG）", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("保存")
        if submitted and structure_name:
            mu = - (homo + lumo) / 2
            qide = e_total - e_sub - e_mol

            if "Trimer" in structure_name:
                tag = "Trimer"
            elif "Dimer" in structure_name:
                tag = "Dimer"
            elif "Tetramer" in structure_name:
                tag = "Tetramer"
            else:
                tag = "Other"

            save_dir = Path(f"results/{structure_name.replace(' ', '_')}")
            save_dir.mkdir(parents=True, exist_ok=True)

            metadata = {
                "構造名": structure_name,
                "タグ": tag,
                "SCFエネルギー": scf_energy,
                "HOMO": homo,
                "LUMO": lumo,
                "μ": mu,
                "双極子モーメント": dipole,
                "Mulliken最大": mulliken_max,
                "Mulliken最小": mulliken_min,
                "E_total": e_total,
                "E_substrate": e_sub,
                "E_molecule": e_mol,
                "QIDE": qide,
                "メモ": notes
            }
            with open(save_dir / "data.yaml", "w") as f:
                yaml.dump(metadata, f)

            if image_file:
                with open(save_dir / "structure.png", "wb") as f:
                    f.write(image_file.read())

            st.success(f"✅ 構造 `{structure_name}` を保存しました")

    # --- 一覧表示 ---
    st.markdown("---")
    st.subheader("構造別の記録一覧（表形式）")

    from glob import glob
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.cluster import KMeans

    rows = []
    for folder in glob("results/*/"):
        meta_path = Path(folder) / "data.yaml"
        img_path = Path(folder) / "structure.png"
        if meta_path.exists():
            with open(meta_path, "r") as f:
                data = yaml.safe_load(f)
            row = data
            row["画像"] = img_path if img_path.exists() else None
            row["パス"] = meta_path
            rows.append(row)

    if rows:
        display_keys = ["構造名", "タグ", "SCFエネルギー", "HOMO", "LUMO", "μ", "双極子モーメント", "Mulliken最大", "Mulliken最小", "E_total", "E_substrate", "E_molecule", "QIDE", "メモ"]
        df = pd.DataFrame([{k: r.get(k, '') for k in display_keys} for r in rows])
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📤 CSVとしてエクスポート", data=csv, file_name="qidt_structures.csv", mime="text/csv")

        st.markdown("---")
        st.subheader("構造特性の散布図（項目選択＋タグ色分け）")
        numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        x_axis = st.selectbox("X軸を選択", options=numeric_columns, index=0)
        y_axis = st.selectbox("Y軸を選択", options=numeric_columns, index=1 if len(numeric_columns) > 1 else 0)

        try:
            fig, ax = plt.subplots()
            tags = df["タグ"].unique()
            colors = sns.color_palette("husl", len(tags))
            for tag, color in zip(tags, colors):
                subset = df[df["タグ"] == tag]
                ax.scatter(subset[x_axis], subset[y_axis], label=tag, color=color)
                for i in subset.index:
                    ax.annotate(subset["構造名"][i], (subset[x_axis][i], subset[y_axis][i]), fontsize=8)
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"{y_axis} vs {x_axis} by タグ")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.warning("⚠️ 散布図を描画できませんでした。")

        st.markdown("---")
        st.subheader("クラスタリング（KMeans）")
        try:
            n_clusters = st.slider("クラスタ数を選択", min_value=2, max_value=6, value=3)
            clustering_data = df[[x_axis, y_axis]].dropna()
            kmeans = KMeans(n_clusters=n_clusters, n_init=10)
            clusters = kmeans.fit_predict(clustering_data)
            df_clust = clustering_data.copy()
            df_clust["Cluster"] = clusters

            fig2, ax2 = plt.subplots()
            palette = sns.color_palette("Set2", n_clusters)
            for cl in range(n_clusters):
                cluster_data = df_clust[df_clust["Cluster"] == cl]
                ax2.scatter(cluster_data[x_axis], cluster_data[y_axis], label=f"Cluster {cl+1}", color=palette[cl])
            ax2.set_xlabel(x_axis)
            ax2.set_ylabel(y_axis)
            ax2.set_title(f"クラスタリング結果: {y_axis} vs {x_axis}")
            ax2.legend()
            st.pyplot(fig2)
        except Exception as e:
            st.warning("⚠️ クラスタリングに失敗しました。")

        st.markdown("---")
        st.subheader("構造別の詳細表示・編集")

        for row in rows:
            with st.expander(f"🧬 {row['構造名']}"):
                mode = st.radio("モード", ["表示", "編集"], key=f"mode_{row['構造名']}")

                if mode == "表示":
                    for key in display_keys:
                        st.write(f"**{key}**: {row.get(key, '')}")
                    if row["画像"]:
                        st.image(str(row["画像"]), caption="構造画像", use_container_width=True)
                else:
                    new_values = {}
                    for key in ["SCFエネルギー", "HOMO", "LUMO", "Mulliken最大", "Mulliken最小", "E_total", "E_substrate", "E_molecule", "双極子モーメント"]:
                        new_values[key] = st.number_input(key, value=float(row.get(key, 0.0)), format="%.6f", key=f"{key}_{row['構造名']}")
                    new_values["μ"] = - (new_values["HOMO"] + new_values["LUMO"]) / 2
                    new_values["構造名"] = row["構造名"]
                    new_values["タグ"] = row.get("タグ", "Other")
                    new_values["QIDE"] = new_values["E_total"] - new_values["E_substrate"] - new_values["E_molecule"]
                    new_values["メモ"] = st.text_area("メモ", value=row.get("メモ", ""), key=f"memo_{row['構造名']}")

                    if st.button("保存", key=f"save_{row['構造名']}"):
                        with open(row["パス"], "w") as f:
                            yaml.dump(new_values, f)
                        st.success("✅ 上書き保存しました。再読み込みしてください。")

                if st.button(f"🗑 削除する：{row['構造名']}", key=f"delete_{row['構造名']}"):
                    import shutil
                    try:
                        shutil.rmtree(f"results/{row['構造名'].replace(' ', '_')}")
                        st.success(f"✅ 「{row['構造名']}」を削除しました。ページを再読み込みしてください。")
                    except Exception as e:
                        st.error(f"⚠️ 削除できませんでした: {e}")

            st.markdown("---")
    
elif tab == "📉 IRスペクトル可視化":
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    st.subheader("IR Spectrum Simulator")
    st.markdown("""
    このセクションでは、アップロードされたCSVファイルの離散的なIRピークデータをガウス関数で平滑化し、連続的なスペクトルとして表示します。  
    **CSV形式：1列目 = 波数 (cm⁻¹)、2列目 = 強度 (km/mol)** を想定。
    """)

    uploaded_file = st.file_uploader("IRデータのCSVファイルをアップロードしてください", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, header=None, names=["freq", "intensity"])
            st.dataframe(df.head())

            x = np.linspace(400, 4000, 5000)
            y = np.zeros_like(x)
            sigma = st.slider("ガウス平滑化幅 σ (cm⁻¹)", 1, 50, 10)

            def gaussian(x, mu, sigma):
                return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

            for _, row in df.iterrows():
                y += row["intensity"] * gaussian(x, row["freq"], sigma)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, color="blue", lw=2)
            ax.set_xlabel("Wavenumber (cm⁻¹)")
            ax.set_ylabel("Intensity (a.u.)")
            ax.set_title("Simulated IR Spectrum")
            ax.invert_xaxis()
            ax.grid(True)
            st.pyplot(fig)

        　　spectrum_name = st.text_input("保存ファイル名（例：sample_spectrum）", value="spectrum")
           result_df = pd.DataFrame({
               "Wavenumber (cm⁻¹)": x,
               "Intensity (a.u.)": y
           })
           csv_bytes = result_df.to_csv(index=False).encode("utf-8")
           st.download_button("📥 平滑化スペクトルをCSVで保存", data=csv_bytes, file_name=f"{spectrum_name}.csv", mime="text/csv")

        except Exception as e:
            st.error(f"CSVファイルの読み込みや処理中にエラーが発生しました: {e}")
    
    
