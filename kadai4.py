import pandas as pd
import datetime

# 定数を定義
LOG_FILE_PATH = './log/log_{export_at}.log'
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


## ログ機能用関数
def write_log(path,log_str):
    now_log = datetime.datetime.now()
    with open(path, mode='a+') as log_file:
        log_file.writelines(f"{str(now_log)}:{str(log_str)}\n")

### メイン処理
def main():
    # ログ用ファイル指定
    now = datetime.datetime.now()
    log_file_path = LOG_FILE_PATH.format(export_at=now.strftime('%Y%m%d_%H%M%S'))
    write_log(log_file_path,"start")

    # マスタ登録
    df=pd.read_csv("./master.csv")
    item_master=[]
    for master_item in df.itertuples():
        write_log(log_file_path,f"マスタテーブルに{master_item[2]}登録")
        item_master.append(Item(str(master_item[1]),master_item[2],int(master_item[3])))
    write_log(log_file_path,"マスタ登録完了")

    # オーダー登録
    order=Order(item_master)
    while 1:
        order_code = input("商品コード(『fin』で入力終了):")
        write_log(log_file_path,f"{order_code}を注文")
        if order_code != "fin":
            count = input("注文数:")
            write_log(log_file_path,f"{count}を入力")
            if count.isdecimal():
                if order.add_item_order(str(order_code),int(count)) == False:
                    print(f"注文ID『{order_code}』は未登録です。")
                    write_log(log_file_path,f"{order_code}は未登録")
            else:
                print("注文数エラー")
                write_log(log_file_path,f"入力エラー（数値{count}）")
        else:
            break

    # オーダー表示
    reciept = order.view_item_list()
    print(reciept)

    # お預かり額入力
    while 1:
        deposit = int(input("お預かり金："))
        write_log(log_file_path,f"お預かり金{deposit}を入力")
        if deposit < order.order_price:
            print("不足してます。")
            write_log(log_file_path,f"お預かり金{deposit}では不足")
        else:
            order.deposit = deposit
            break
    reciept += f"お預：¥{order.deposit}\n"

    # お釣り表示
    change_txt = f"お釣り：¥{order.deposit-order.order_price}"
    print(change_txt)
    reciept += f"{change_txt}\n"
    
    # レシート出力
    now = datetime.datetime.now()
    out_file_path = OUT_FILE_PATH.format(export_at=now.strftime('%Y%m%d_%H%M%S'))
    reciept = f"日時：{now.strftime('%Y/%m/%d %H:%M:%S')}\n\n{reciept}"
    with open(out_file_path,'w') as f:
        f.write(reciept)
        write_log(log_file_path,"レシート出力完了")

if __name__ == "__main__":
    main()