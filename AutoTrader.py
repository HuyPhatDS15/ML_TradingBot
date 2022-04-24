from VirtualAccount import VirtualAccount
import numpy as np
from Config import *
import time

class AutoTrader:

    #Import data, model
    def __init__(self,model):
        self.advisor = model
        self.account = VirtualAccount()
        self.trade_amount = 100

    #Hàm mua btc
    def buy(self):
        prev_bought_at = self.account.bought_btc_at # How much did I buy BTC for before
        #gán giá mua dự đoán = giá mua tại trc đó

        if self.account.usd_balance - self.trade_amount >= 0:
        # Nếu số dư usd - giá trị gd >=0 (check đủ tiền gd ko)
            if prev_bought_at == 0 or self.account.last_transaction_was_sell or (prev_bought_at > self.account.btc_price): #or (self.account.btc_price/prev_bought_at -1 > 0.005):
            # Nếu giá mua dự đoán = 0 /hoặc/ giao dịch bán cuối cùng /hoặc/ giá mua dự đoán = giá mua trước đó (lơn hơn)> giá trị btc hiện tại (nghĩa là btc đang giảm, đặt lệnh mua)
                print(">> BUYING $",self.trade_amount," WORTH OF BITCOIN")
                # Mua "bao nhiu"
                self.account.btc_amount += self.trade_amount / self.account.btc_price
                # Số lượng btc += số lượng giao dịch/giá trị btc
                self.account.usd_balance -= self.trade_amount
                # Số dư usd -= số đã mua
                self.account.bought_btc_at = self.account.btc_price
                # Mua btc tại = giá btc lúc đó
                self.account.last_transaction_was_sell = False
                # giao dich cuối là bán = False
            else:
                print(">> Not worth buying more BTC at the moment")
        else:
            print(">> Not enough USD left in your account to buy BTC ")

    #Hàm bán btc
    def sell(self):
        if self.account.btc_balance - self.trade_amount >= 0:
        # Nếu số dư > số lượng gd (có btc để bán ko)
            if self.account.btc_price > self.account.bought_btc_at: # Is it profitable?
            # Nếu giá trị (bán) > giá mua tại (giá mua trc đó) -> bán (có lãi)   (giá btc hiện tại > giá mua trc đó ==> btc đang tăng, đặt lệnh bán) 
                print(">> SELLING $",self.trade_amount," WORTH OF BITCOIN")
                self.account.btc_amount -= (self.trade_amount / self.account.btc_price)
                # Số lượng btc -= (số lượng giao dịch/ giá trị)
                self.account.usd_balance += self.trade_amount
                # Số dư usd += số lượng giao dịch (+ tiền vốn & lãi)
                self.account.last_transaction_was_sell = True
                # Giao dịch cuối là bán = True
            else:
                print(">> Declining sale: Not profitable to sell BTC")
        else:
            print(">> Not enough BTC left in your account to buy USD ")

    #Hàm trading & update số dư
    def runSimulation(self,samples,prices):
        print("> Trading Automatically for ",TESTING_MONTHS)
        day_count = 0
        for i in range(0,len(samples)):
            # print("#    Account Balance Before: $ ", (self.account.usd_balance + self.account.btc_balance))

            if i % 24 == 0: #Thống kê giao dịch trong 1 ngày
                day_count += 1
                print("#################################################################################################")
                print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
                      self.account.btc_balance, " USD: $", self.account.usd_balance, "")
                print("#################################################################################################")
                print("##########################################   DAY ",day_count,"   #########################################")


            if i % 6 == 0: # Perform a prediction every 6 hours (#dự doán mỗi 6h)
                prediction = self.advisor.predict(np.array([samples[i]]))
                ## giá dự doán
                #btc_price = samples[i][len(samples[i])-1]
                btc_price = prices[i]
                ## giá btc thực tế

                if self.account.btc_price != 0:
                # Nếu giá thực tế khác 0
                    self.account.btc_balance = self.account.btc_amount * btc_price
                    # số dư btc = số lượng btc * giá trị btc 

                self.account.btc_price = btc_price
                #cập nhật giá btc

                if prediction == 1:
                #nếu dự doán = 1 -> đặt lệnh mua
                    self.buy()
                else:
                #Còn lại, đặt lệnh bán
                    self.sell()

                self.account.btc_balance = self.account.btc_amount * btc_price
                #update lại số dư btc = số lượng * giá trị
                time.sleep(1)  # Only for Visual Purposes

        print("#################################################################################################")
        print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
              self.account.btc_balance, " USD: $", self.account.usd_balance, "")
        print("#################################################################################################")