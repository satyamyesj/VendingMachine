from abc import ABC, abstractmethod

class VMState(ABC):
    @abstractmethod
    def insert_coins(self, coins):
        pass

    @abstractmethod
    def select_product(self, product):
        pass

    @abstractmethod
    def dispense_change(self):
        pass

    @abstractmethod
    def dispense_product(self):
        pass

    @abstractmethod
    def cancel_transaction(self):
        pass
    


