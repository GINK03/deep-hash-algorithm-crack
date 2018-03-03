# Deep Hash Algorithm Crack

ディープラーニングで素数を用いたハッシングをある程度推定できないでしょうか。  

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
仮想通貨のマイニングは複雑なハッシュ処理を行うことで、一定値以下をお金とみなす仕組みがあるようです。  

Gunosyさまのブログ[1]が詳しく参考になります
> ビットコインでは、 SHA256(トランザクション全体とか、前のブロックハッシュとか、nonce値) で計算されるハッシュ値が、運良くある値以下になった場合のみ検証成功となります。nonce値(なんでもいい)をドンドン変えて、その条件を満たすまで死ぬほど計算するのです。その検証の難しさを difficulty と呼び、期待される必要計算回数と比例します。

## 学習 & 評価
以下のコマンドで学習を行えます  

0~1までの値をハッシュ値が取るように調整しているので、val_lossが0.5より小さいので、完全なランダムネスではないようです。  

```console
$ python3 generate.py # ハッシュ値の計算
$ python3 make_dense.py # 密行列に変換

$ python3 spectre.py --train # 学習
...
Epoch 99/100
25152/25152 [==============================] - 3s 122us/step - loss: 0.0351 - val_loss: 0.3185
Epoch 100/100
25152/25152 [==============================] - 3s 122us/step - loss: 0.0353 - val_loss: 0.3190
```

## 参考
- [1] [仮想通貨マイニングに関するまとめ](http://tech.gunosy.io/entry/crypto-mining-summary)
- [2] [Hash function for a string](https://stackoverflow.com/questions/8317508/hash-function-for-a-string)
