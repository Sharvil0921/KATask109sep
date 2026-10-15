def calculateElectronicsGST(a, b):
 subtotal = a + b
 return subtotal + (subtotal * 0.18)
def calculateFashionGST(c, d):
 subtotal = c + d
 return subtotal + (subtotal * 0.13)
def calculateFoodGST(e):
 return e + (e * 0.07)
def totalBill(a, b, c, d, e):
 return (
 calculateElectronicsGST(a, b)
 + calculateFashionGST(c, d)
 + calculateFoodGST(e)
 )
def calculateDiscountedBill(a, b, c, d, e):
 total = totalBill(a, b, c, d, e)
 discount = total * 0.20
 return total - discount
if __name__ == "__main__":
 total = totalBill(100, 100, 100, 100, 100)
 discount = total * 0.20
 payable = calculateDiscountedBill(100, 100, 100, 100, 100)
 print(f"Total after GST = {total:.2f}")
 print(f"Discount = {discount:.2f}")
 print(f"Final payable amount = {payable:.2f}")