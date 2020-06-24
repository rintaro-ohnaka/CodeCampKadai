# CodeCampの課題を載せています
現在弊社ではCodeCampの教材を利用し、新卒エンジニア研修を行っています。  

## 18章課題：自動販売機
18章の課題：自動販売機について説明します。  
自動販売機のプログラムです。  
商品を追加、購入することができます。  

### 管理者ページでできること  
主に4つの機能があります。  
①商品を追加すること  
②追加した商品の在庫数を変更すること  
③追加した商品を購入者ページで公開するか否かを選択すること  
④追加した商品の一覧を確認すること  

## 自動販売機の基本的な処理はapp.pyに保存してあります。  
### １、app.pyの691行目〜921行目
  管理者ページの処理
### ２、app.pyの926行目〜1092行目
  購入者ページの処理

## 自動販売機のHTMLは３つ存在します。  
### １、templates/vending_machine_admin.html  
  管理者ページのHTMLです。  
### ２、templates/vending_machine_buy.html  
  購入者ページのHTMLです。  
### ３、templates/vending_machine_result.html  
  購入結果ページのHTMLです。  
  
## テーブル作成に使用するSQLファイルは以下の通りです。  
### １、create.sql  
  自動販売機のテーブル作成で使用するSQLは、104行目〜129行目までです。  

