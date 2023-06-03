from django.db import models

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # product_set
class Collections(models.Model):
    title = models.CharField(max_length=255)
    featured_products = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name="+")

class product(models.Model):
    sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='-')
    descriotion = models.TextField()
    unitprice = models.DecimalField(max_digits=6, decimal_places=2)
    inverntory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(Collections, on_delete=models.CASCADE)
    promotions = models.ManyToManyField(Promotion, related_name='products')

class Customer(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateTimeField(null=True)
    # class Meta:
    #     db_table = 'store_Customer'
    #     indexes = [
    #         models.Index(fields=['last_name', 'first_name'])
    #     ]
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]
    membership = models.CharField(
    max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Address(models.Model):
    street = models.CharField(max_length=255)
    ciry = models.CharField(max_length=255)
    # customer = models.OneToOneField(Customer, on_delete=models.SET_NULL)    #if the custemer get deleted the amount of this field will be none
    # if the custemer get deleted the associated address will also be deleted
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)
    zip1 = models.CharField(max_length=50)
    

class Order(models.Model):
    PAYMENT_STATUS = [
        ("P", "Pending"),
        ("C", "Complete"),
        ("F", "Failed"),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default="P")
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quanity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_At = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quanity = models.PositiveSmallIntegerField()
