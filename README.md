# Deep Hash Algorithm Crack

ディープラーニングでハッシュ値ををある程度推定できないでしょうか。

## 世間一般における議論
StackExchangeにこのような投稿がありました。  

**質問**  
> Can a neural network crack hashing algorithms?

**答え**  
> No.
> Neural networks are pattern matchers. They're very good pattern matchers, but pattern matchers just the same. No more advanced than the biological brains they are intended to mimic. More thorough, more tireless, but not more sophisticated.

パターン構造が見て取れないから無理ですよねって答えになっています。  

## シンプルなハッシュ処理
素数を用いたハッシュ処理で文字列をハッシュ化するのにこのようなことを行っています[2]  
```python
def hashing(chars):
  A = 179424691 # 大きな素数1
  B = 15485867 # 大きな素数2
  C = 32416187567 # 大きな素数3
  hash = 105733 # 初期値の素数
  for char in chars:
    hash = hash*A ^ ord(char)*B # XORを計算する
  return hash%C
```

## ところで仮想通貨のマイニングとは
仮想通貨のマイニングは複雑なハッシュ処理を行うことで、一定値以下とき検証成功となります  

Gunosyさまのブログ[1]が詳しく参考になります
> ビットコインでは、 SHA256(トランザクション全体とか、前のブロックハッシュとか、nonce値) で計算されるハッシュ値が、運良くある値以下になった場合のみ検証成功となります。nonce値(なんでもいい)をドンドン変えて、その条件を満たすまで死ぬほど計算するのです。その検証の難しさを difficulty と呼び、期待される必要計算回数と比例します。

hashの計算自体はとても軽いので、そもそも、機械学習で判別するコストをかけるまでもない。。。かもしれませんが、nonce値に関してある程度の当て推量を行えたらどうでしょうか。

## 学習 & 評価
以下のコマンドで学習を行えます  

0~1までの値をハッシュ値が取るように調整しているので、val_lossが0.5より小さいので、完全なランダムネスではなく、validatin(テストデータ)に対してMean Absolute Error（平均絶対誤差）で0.013程度になりかなり確信度の高い結果を得ることができました。  

**学習**  
```console
$ python3 generate.py # ハッシュ値の計算
$ python3 make_dense.py # 密行列に変換

$ python3 spectre.py --train # 学習
...
```
**評価**  
テストデータで評価すると、このように近しいhash値を得ることができました  
```console
$ python3 spectre.py --predict | less # 予想
input=i a m l, real=0.8755711807954124, predict=0.8816601037979126
input=n ! w f, real=0.22271613308754315, predict=0.22165605425834656
input=t e v n, real=0.9822465533733343, predict=0.971804141998291
input=l v t k, real=0.5375446331578566, predict=0.5378258228302002
input=i k e k, real=0.3398879642441816, predict=0.3512294292449951
input=q ? j m, real=0.8622401894856249, predict=0.8548359870910645
input=m v h p, real=0.5774709391115539, predict=0.5751619338989258
...
```

## 本当にDeepLearningでhashを推測したほうが得なのか？
DeepLearningの計算コスト < Hashの全探索が成り立っているうちは、正直、計算しても仕方がないという感じでして、非常に計算が困難なhash関数を使った暗号化通貨で計算リソースが必要でマイニングが難しいとき、DeepLearningである程度、推測しつつ、候補群の中から、Hash値を計算するという流れが良いかと存じます  

(一部の仮想通貨はCPUしか対応しているバイナリを配っていなかったりして、GPUでフィルタリングして最初から候補軍を絞るとかもできるかもしれません)  

FPGAやASICで高速にSHA256が計算できるようにできるようになってしまっているので、ハードフォークを積極的に行うと宣言している通貨もあるようで、作り込みを前提としたASICはすぐ新しいアルゴリズムに対応するのが難しいですが、hash値をサンプリングできる場合、傾向を学習してすぐさま予想モデルを構築することができます。  

## 参考
- [1] [仮想通貨マイニングに関するまとめ](http://tech.gunosy.io/entry/crypto-mining-summary)
- [2] [Hash function for a string](https://stackoverflow.com/questions/8317508/hash-function-for-a-string)
