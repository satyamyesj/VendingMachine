from coin import Coin
from product import Product
from vm import VendingMachine


def main():
    product_reserve={Product.coke: 4, Product.pepsi: 6, Product.soda:3}
    product_price={Product.coke:30, Product.pepsi:25, Product.soda:45}
    coin_reserve={Coin.quarter:3, Coin.dime: 6, Coin.nickel: 4, Coin.penny: 10}
    vm=VendingMachine(coin_reserve, product_reserve, product_price)
    coins={Coin.quarter:1, Coin.dime: 2, Coin.nickel: 1}
    vm.insert_coins(coins)
    #vm.dispense_change()
    #vm.cancel_transaction()
    vm.select_product(Product.soda)
    #vm.cancel_transaction()
    vm.dispense_change()



if __name__=="__main__":
    main()