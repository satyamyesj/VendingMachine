from vm_state import VMState
from vm_errors import *

class VendingMachine:
    def __init__(self, coin_reserve, product_reserve, product_price):
        self.coin_reserve=coin_reserve
        self.product_reserve=product_reserve
        self.product_price=product_price
        self.inserted_coins={}
        self.selected_product=None
        self.current_state=Ready(self)

    def reset_prodcut_reserve(self, product_reserve):
        self.product_reserve=product_reserve

    def update_coin_reserve(self, coin_reserve):
        self.coin_reserve=coin_reserve

    def return_change(self, change):
        for coin in self.coin_reserve.keys():
            if change.__contains__(coin):
                self.coin_reserve[coin]=self.coin_reserve[coin]-change[coin]

    def add_coins(self, coins):
        for coin in self.coin_reserve.keys():
            if coins.__contains__(coin):
                self.coin_reserve[coin]=self.coin_reserve[coin]+coins[coin]

    def calculate_change(self):
        if self.selected_product==None:
            raise NoProductError
        else: 
            insereted_coin_value=VendingMachine.coins_value(self.inserted_coins)
            #print(insereted_coin_value)
            change_value=insereted_coin_value-self.product_price[self.selected_product]
            #print(change_value)
            change=dict()
            for coin in self.coin_reserve:
                if change_value>=coin.value:
                    coin_req=int(change_value/coin.value)
                    change_value=change_value-(min(coin_req, self.coin_reserve[coin])*coin.value)
                    if min(coin_req, self.coin_reserve[coin])!=0:
                        change[coin]=min(coin_req, self.coin_reserve[coin])
            if(change_value==0):
                return change
            else:
                return None

    def insert_coins(self, inserted_coins):
        self.current_state.insert_coins(inserted_coins)

    def select_product(self, product):
        self.current_state.select_product(product)

    def dispense_change(self):
        self.current_state.dispense_change()

    def dispense_product(self):
        self.current_state.dispense_product()

    def cancel_transaction(self):
        self.current_state.cancel_transaction()

    @staticmethod
    def coins_value(coins):
        value=0
        for coin in coins.keys():
            value+=coin.value*coins[coin]
        return value

    def __str__(self):
        return "\tVM[\n\tcoin_reserve:{},\n\tproduct_reserve:{},\n\tproduct_price:{},\n\tinserted_coin:{},\n\tselected_product:{}\n\t]".format(self.coin_reserve, self.product_reserve, self.product_price, self.inserted_coins, self.selected_product)



class Ready(VMState):
    def __init__(self, VM):
        self.VM=VM
        print("READY_STATE")
        print(self.VM)

    def insert_coins(self, coins):
        self.VM.inserted_coins=coins
        self.VM.current_state=CoinsInserted(self.VM)

    def select_product(self, product):
        raise NoCoinsError

    def dispense_change(self):
        raise NoTransactionError

    def dispense_product(self):
        raise NoTransactionError

    def cancel_transaction(self):
        raise NoTransactionError

class CoinsInserted(VMState):
    def __init__(self, VM):
        self.VM=VM
        print("COINS_INSERTED_STATE")
        print(self.VM)
        print("you have inserted", self.VM.inserted_coins)

    def insert_coins(self, coins):
        raise TransactionExistError

    def select_product(self, product):
        self.VM.selected_product=product
        self.VM.current_state=ProductSelected(self.VM)

    def dispense_change(self):
        raise NoProductError

    def dispense_product(self):
        raise NoProductError

    def cancel_transaction(self):
        self.VM.current_state=CancellingTransaction(self.VM)
        

class ProductSelected(VMState):
    def __init__(self, VM):
        self.VM=VM
        print("PRODUCT_SELECTED_STATE")
        print(self.VM)
        if self.VM.product_reserve[self.VM.selected_product]>=1 and self.VM.product_price[self.VM.selected_product]<=VendingMachine.coins_value(self.VM.inserted_coins):
            print("you have selected", self.VM.selected_product)
        elif self.VM.product_reserve[self.VM.selected_product]==0:
            print("selected product is out of stock")
            self.VM.current_state=CancellingTransaction(self.VM)
        else:
            print("product costs more than inserted money")
            self.VM.current_state=CancellingTransaction(self.VM)
            

    def insert_coins(self, coins):
        raise TransactionExistError

    def select_product(self, product):
        raise TransactionExistError

    def dispense_change(self):
        self.VM.current_state=DispensingChange(self.VM)
                
    def dispense_product(self):
        raise ChangeExistError

    def cancel_transaction(self):
        self.VM.current_state=CancellingTransaction(self.VM)


class DispensingChange(VMState):
    def __init__(self, VM):
        self.VM=VM
        print("DISPENSING_CHANGE_STATE")
        print(self.VM)
        self.VM.add_coins(self.VM.inserted_coins)
        change=self.VM.calculate_change()
        if change==None:
            print("no enough change for selected product")
            self.VM.return_change(self.VM.inserted_coins)
            self.VM.current_state=CancellingTransaction(self.VM)
        else:   
            print("please collect your change", change)
            self.VM.return_change(change)
            self.VM.inserted_coins={}
            self.VM.current_state=DispensingProduct(self.VM)

    def insert_coins(self, coins):
        raise TransactionExistError

    def select_product(self, product):
        raise TransactionExistError

    def dispense_change(self):
        raise NoChangeError

    def dispense_product(self):
        self.VM.current_state=DispensingProduct(self.VM)

    def cancel_transaction(self):
        raise CantCancelTransaction


class DispensingProduct(VMState):
    def __init__(self, VM):
        self.VM=VM
        print("DISPENSING_PRODUCT_STATE")
        print(self.VM)
        print("please collect your product", self.VM.selected_product)
        self.VM.product_reserve[self.VM.selected_product]=self.VM.product_reserve[self.VM.selected_product]-1
        self.VM.select_product=None
        self.VM.current_state=Ready(self.VM)

    def insert_coins(self, coins):
        raise TransactionExistError

    def select_product(self, product):
        raise TransactionExistError

    def dispense_change(self):
        raise NoChangeError

    def dispense_product(self):
        raise NoTransactionError

    def cancel_transaction(self):
        raise CantCancelTransaction


class CancellingTransaction(VMState):
    def __init__(self, VM):
        self.VM=VM
        print("CANCELLING_TXN_STATE")
        print(self.VM)
        print("cancelling transaction")
        print("please collect your money", self.VM.inserted_coins)
        self.VM.inserted_coins={}
        self.VM.selected_product=None
        self.VM.current_state=Ready(self.VM)

    def insert_coins(self, coins):
        raise TransactionExistError

    def select_product(self, product):
        raise TransactionExistError

    def dispense_change(self):
        raise TransactionExistError

    def dispense_product(self):
        raise TransactionExistError

    def cancel_transaction(self):
        raise CantCancelTransaction

