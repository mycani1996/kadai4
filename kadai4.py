import pandas as pd
import datetime

# 定数を定義
now = datetime.datetime.now()
LOG_FILE_PATH = f'./log/log_{now.strftime("%Y%m%d_%H%M%S")}.log'
MASTER_FILE_PATH = './master.csv'
OUT_FILE_PATH = './receipt/{export_at}.txt'

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price

    def get_code(self):
        return self.item_code

    def get_name(self):
        return self.item_name
            
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    deposit = 0
    order_price = 0
    order_count = 0
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
    
    # 注文表を作成
    def make_order(self):
        while 1:
            order_code = input("商品コード(『fin』で入力終了):")
            write_log(f"{order_code}を注文")
            if order_code != "fin":
                count = input("注文数:")
                write_log(f"{count}を入力")
                # 注文数に数値以外が入力されればエラー
                if count.isdecimal():
                    if self.add_item_order(str(order_code),int(count)) == False:
                        print(f"注文ID『{order_code}』は未登録です。")
                        write_log(f"{order_code}は未登録です")
                else:
                    print("注文数エラー")
                    write_log(f"入力エラー（数値{count}）")
            else:
                break

    # 注文を追加
    def add_item_order(self,item_code,count):
        item_flg = False #注文コードがマスタにあるか確認するフラグ
        # マスタから注文情報を取得し、注文リストへ登録
        for item in self.item_master:
            if item_code == item.get_code():
                item_flg = True
                item_data = [item,count]
                self.item_order_list.append(item_data)
                break
        return item_flg
    
    # 注文リストを表示
    def view_item_list(self):
        text = ""
        text += "======購入リスト======\n"
        for order in self.item_order_list:
            text += f"商品名:{order[0].get_name()}, ¥{order[0].get_price()}, {order[1]}個\n"
            self.order_price += order[0].get_price()*order[1]
            self.order_count += order[1]
        # print("\n")
        text += "========合計=========\n"
        text += f"合計：{self.order_count}件\n"
        text += f"合計額：¥{self.order_price}\n"
        text += "======お預かり金======\n"
        return text
    
    # お預かり処理
    def bill_function(self):
        while 1:
            deposit = int(input("お預かり金："))
            write_log(f"お預かり金{self.deposit}を入力")
            if deposit < self.order_price:
                print("不足してます。")
            else:
                self.deposit = deposit
                print(f"お釣り：¥{self.deposit-self.order_price}")
                write_log(f"お釣りは{self.deposit-self.order_price}")
                break
    
    # レシート作成
    def make_reciept(self,text):
        text = f"{text}お預：¥{self.deposit}\n"
        text = f"{text}お釣り：¥{self.deposit-self.order_price}"
        now = datetime.datetime.now()
        out_file_path = OUT_FILE_PATH.format(export_at=now.strftime('%Y%m%d_%H%M%S'))
        text = f"日時：{now.strftime('%Y/%m/%d %H:%M:%S')}\n\n{text}"
        with open(out_file_path,'w') as f:
            f.write(text)
            write_log("レシート出力完了")

## ログ機能用関数
def write_log(log_str):
    now_log = datetime.datetime.now()
    with open(LOG_FILE_PATH, mode='a+') as log_file:
        log_file.writelines(f"{str(now_log)}:{str(log_str)}\n")

# マスタ登録用関数
def set_master_item(path):
    df=pd.read_csv(path)
    list=[]
    for item in df.itertuples():
        write_log(f"マスタテーブルに{item[2]}登録")
        list.append(Item(str(item[1]),item[2],int(item[3])))
    write_log("マスタ登録完了")
    return list

### メイン処理
def main():
    # マスタ登録
    item_master = set_master_item(MASTER_FILE_PATH)
    
    # オーダー登録
    order=Order(item_master)
    order.make_order()

    # オーダー表示
    reciept = order.view_item_list()
    print(reciept)

    # 会計処理
    order.bill_function()

    # レシート出力
    order.make_reciept(reciept)

if __name__ == "__main__":
    write_log("start")
    main()