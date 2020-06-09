# ジャンケンアルゴリズムを書いてみましょう

# a は自分のジャンケンの手（htmlのボタンで選択した数値を入れる）
a = 1
# b には相手のジャンケンの手を入れる（random関数で生成した数値を入れる？）
b = 2

# c の変数の中にはジャンケンの結果を入れる
c = (a - b + 3)%(3)

if c == 0:
    print("draw")
elif c == 2:
    print("win")
else:
    print("lose")
    
print(c)