import pandas as pd
from collections import defaultdict, Counter
from sudachipy import tokenizer
from sudachipy import dictionary
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer  # 追加


# SudachiPyの設定
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C  # 分割モードCが最も細かい

# ストップワードの定義
stop_words = set([
    "の", "に", "は", "を", "た", "が", "で", "て", "と", "し", 
    "れ", "さ", "ある", "いる", "も", "する", "から", "な", 
    "こと", "として", "いく", "や", "れる", "など", "なっ", 
    "よう", "なる", "へ", "お", "これ", "それ", "あれ", 
    "この", "その", "あの", "たち", "もの", "いう", 
])

# 対象とする品詞
target_pos = {"名詞", "動詞", "形容詞"}

# Excelファイルを読み込む
input_file = 'input_data.xlsx'  # 読み込むExcelファイルのパス
df = pd.read_excel(input_file)

# 形態素解析の結果を格納するリスト
parsed_data = []
frequency_counter = defaultdict(Counter)
cooccurrence_counter = defaultdict(Counter)
documents_by_job = defaultdict(str)

# テキストが含まれている列名を指定
job_column = '職種'  # A列
text_column = 'テキスト'  # B列

# 各行のテキストを形態素解析
for index, row in df.iterrows():
    job_title = row[job_column]
    text = row.get(text_column, "")
    
    if not text:
        print(f"Warning: No text found in row {index}. Skipping this row.")
        continue

    tokens = tokenizer_obj.tokenize(text, mode)
    
    words_in_text = []
    current_phrase = []  # 名詞が連続する場合のフレーズを格納するリスト
    for token in tokens:
        surface = token.surface()
        pos = token.part_of_speech()[0]  # 品詞名
        
        # ストップワードの除去
        if surface not in stop_words:
            # 名詞、動詞、形容詞のみ対象
            if pos in target_pos:
                # ステミング（原形を使う）
                stem = token.dictionary_form()
                
                if pos == "名詞":
                    # 名詞が連続する場合、current_phraseに追加
                    current_phrase.append(stem)
                else:
                    # 名詞が終わったら、これまでのcurrent_phraseを結合して保存
                    if current_phrase:
                        combined_phrase = ''.join(current_phrase)
                        frequency_counter[job_title][(combined_phrase, "名詞")] += 1
                        words_in_text.append(combined_phrase)
                        current_phrase = []  # current_phraseをリセット
                    
                    # 名詞以外の場合も単語としてカウント
                    frequency_counter[job_title][(stem, pos)] += 1
                    words_in_text.append(stem)
                
                # 職種ごとに文書をまとめる
                documents_by_job[job_title] += f" {stem}"
                
                # Index、職種、表層形、原形 (ステム)、品詞、その他の品詞情報を追加
                parsed_data.append([index, job_title, surface, stem, pos])

    # 最後のフレーズを追加
    if current_phrase:
        combined_phrase = ''.join(current_phrase)
        frequency_counter[job_title][(combined_phrase, "名詞")] += 1
        words_in_text.append(combined_phrase)
    
    # 共起回数のカウント
    for w1, w2 in combinations(words_in_text, 2):
        cooccurrence_counter[job_title][(w1, w2)] += 1
        cooccurrence_counter[job_title][(w2, w1)] += 1

# 解析結果をデータフレームに変換
columns = ['Index', '職種', '表層形', '原形 (ステム)', '品詞']
parsed_df = pd.DataFrame(parsed_data, columns=columns)

# 職種ごとの単語出現頻度をリストに変換
frequency_data = []
for job_title, counter in frequency_counter.items():
    for (word, pos), count in counter.items():
        frequency_data.append([job_title, word, pos, count])

frequency_df = pd.DataFrame(frequency_data, columns=['職種', '単語 (原形)', '品詞', '出現頻度']).sort_values(by=['職種', '出現頻度'], ascending=[True, False])

# 職種ごとの共起回数をリストに変換
cooccurrence_data = []
for job_title, counter in cooccurrence_counter.items():
    for (w1, w2), count in counter.items():
        cooccurrence_data.append([job_title, w1, w2, count])

cooccurrence_df = pd.DataFrame(cooccurrence_data, columns=['職種', '単語1 (原形)', '単語2 (原形)', '共起回数']).sort_values(by=['職種', '共起回数'], ascending=[True, False])

# 職種ごとの文書をリストに変換
documents = [doc for doc in documents_by_job.values()]
job_titles = [job for job in documents_by_job.keys()]

# TF-IDFの計算
vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
tfidf_matrix = vectorizer.fit_transform(documents)
terms = vectorizer.get_feature_names_out()

# TF-IDFをデータフレームに変換
tfidf_data = []
for i, job_title in enumerate(job_titles):
    tfidf_scores = zip(terms, tfidf_matrix[i].toarray().flatten())
    sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
    
    for term, score in sorted_scores:
        tfidf_data.append([job_title, term, score])

tfidf_df = pd.DataFrame(tfidf_data, columns=['職種', '単語 (原形)', 'TF-IDF']).sort_values(by=['職種', 'TF-IDF'], ascending=[True, False])

# 解析結果と出現頻度、共起回数、TF-IDFを新しいExcelファイルに書き込む
with pd.ExcelWriter('解析結果_単語出現頻度_共起回数_TF-IDF.xlsx') as writer:
    parsed_df.to_excel(writer, sheet_name='解析結果', index=False)
    frequency_df.to_excel(writer, sheet_name='職種別単語出現頻度', index=False)
    cooccurrence_df.to_excel(writer, sheet_name='職種別単語共起回数', index=False)
    tfidf_df.to_excel(writer, sheet_name='職種別TF-IDFスコア', index=False)

print("解析が完了し、結果が '解析結果_単語出現頻度_共起回数_TF-IDF.xlsx' に書き込みました。")
