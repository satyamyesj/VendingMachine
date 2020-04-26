class NoCoinsError(Exception):
    def __str__(self):
        return "coins not inserted"

class NoTransactionError(Exception):
    def __str__(self):
        return "transaction does not exits"

class TransactionExistError(Exception):
    def __str__(self):
        return "transaction already present"

class NoProductError(Exception):
    def __str__(self):
        return "product is not selected"

class ProductExistError(Exception):
    def __str__(self):
        return "product is already selected"

class ChangeExistError(Exception):
    def __str__(self):
        return "change exist with system"

class NoChangeError(Exception):
    def __str__(self):
        return "no change exist"

class CantCancelTransaction(Exception):
    def __str__(self):
        return "transaction can't be cancelled"
