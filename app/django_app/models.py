from django.db import models

# Create your models here.

class TimedBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")


class Manager(TimedBaseModel):
    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(verbose_name="Имя", max_length=100)
    username = models.CharField(verbose_name="Username", max_length=100, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name="Телеграм ID", unique=True)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)

    def __str__(self):
        return self.full_name


class Customer(TimedBaseModel):
    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(verbose_name="Имя пользователя", max_length=100)
    username = models.CharField(verbose_name="Username", max_length=100, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name="Телеграм ID", unique=True)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)

    def __str__(self):
        return str(dict(id=self.id,
                        full_name=self.full_name,
                        username=self.username,
                        phone=self.phone,
                        telegram_id=self.telegram_id,
                        email=self.email))


class Store(TimedBaseModel):
    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    id = models.AutoField(primary_key=True, verbose_name="Артикул")
    name = models.CharField(verbose_name="Название магазина", max_length=100)
    city = models.CharField(verbose_name="Город", max_length=100)
    street = models.CharField(verbose_name="Улица", max_length=100)
    house = models.CharField(verbose_name="Дом", max_length=100)
    latitude = models.CharField(verbose_name="Широта", max_length=100)
    longitude = models.CharField(verbose_name="Долгота", max_length=100)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=50)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)

    def __str__(self):
        return f"№{self.id} - {self.name})"


class Product(TimedBaseModel):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название товара", max_length=50)
    # photo = models.CharField(verbose_name="Фото file_id", max_length=200)
    photo = models.ImageField(upload_to='flowers_img/')
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=8)
    description = models.TextField(verbose_name="Описание", max_length=3000, null=True)

    def __str__(self):
        return str(dict(id=self.id,
                        name=self.name,
                        photo=self.photo,
                        price=self.price,
                        description=self.description,
                        ))


class ProductInStore(TimedBaseModel):
    class Meta:
        verbose_name = "Товар в магазине"
        verbose_name_plural = "Товары в магазине"

    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, verbose_name="Идентификатор магазина", on_delete=models.SET(0))
    product = models.ForeignKey(Product, verbose_name="Идентификатор Товара", on_delete=models.SET(0))
    quantity = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return f"№{self.id} {self.store} {self.product} {self.quantity}"


class Order(TimedBaseModel):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, verbose_name="Покупатель", on_delete=models.SET(0))
    product_id = models.ForeignKey(Product, verbose_name="Идентификатор Товара", on_delete=models.SET(0))
    purchase_time = models.DateTimeField(verbose_name="Время покупки", auto_now_add=True)
    shipping_address = models.CharField(verbose_name="Адрес Доставки", max_length=100)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=50)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)
    successful = models.BooleanField(verbose_name="Исполнен", default=False)

    def __str__(self):
        return f"№{self.id} - {self.customer_id} ({self.product_id})"
