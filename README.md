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
  A = 7 # 大きな素数1
  B = 17 # 大きな素数2
  C = 23 # 大きな素数3
  hash = 37 # 初期値の素数
  for char in chars:
    hash = hash*A ^ ord(char)*B # XORを計算する
  return hash%C
```

## ところで仮想通貨のマイニングとは
仮想通貨のマイニングは複雑なハッシュ処理を行うことで、一定値以下をお金とみなす仕組みがあるようです。  
TODO:仕組みを書く

## 学習 & 評価


## 参考
- [2] [Hash function for a string](https://stackoverflow.com/questions/8317508/hash-function-for-a-string)
