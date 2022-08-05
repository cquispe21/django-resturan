from datetime import datetime

from django.db import models
from django.forms import model_to_dict
from .choices import actividad

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    usuario_creacion = models.CharField(max_length=15, blank=None, null=True)
    usuario_modificacion = models.CharField(max_length=15, blank=None, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=None, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Restaurante(models.Model):
    nombre_restaurante = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    pagina_web = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    actividad = models.CharField(max_length=10, choices=actividad, default='Abierto')
    email = models.EmailField(null=True, blank=True)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "tp_restaurante"
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"

    def __str__(self):
        return "{}".format(self.nombre_restaurante)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.IntegerField(default=1)

    def __str__(self):
        return self.cli.names

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=50)
    direccion_empresa = models.CharField(max_length=50)
    telefono_empresa = models.CharField(max_length=10)
    email_empresa = models.EmailField(null=True, blank=True)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)
    class Meta:
        db_table = "tp_empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return "{}".format(self.nombre_empresa)

class Chofer(models.Model):
    nombre_chofer = models.CharField(max_length=50)
    apellido_chofer = models.CharField(max_length=50)
    telefono_chofer = models.CharField(max_length=10)
    email_chofer = models.EmailField(null=True, blank=True)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    class Meta:
        db_table = "tp_chofer"
        verbose_name = "Chofer"
        verbose_name_plural = "Choferes"

    def __str__(self):
        return "{}".format(self.nombre_chofer)


class Zonas(models.Model):
    nombre_zona = models.CharField(max_length=50)
    chofer = models.ForeignKey(Chofer,on_delete=models.CASCADE)
    usuario_modificacion = models.CharField(max_length=15,blank=True,null=True,)
    fecha_creacion = models.DateTimeField(auto_now_add=True,blank=True,null=True,)
    fecha_modificacion = models.DateTimeField(auto_now=True,blank=True,null=True,)
    estado = models.IntegerField(blank=True,null=True,default=1)
    class Meta:
        db_table = "tp_zona"
        verbose_name = "Zona"
        verbose_name_plural= "Zonas"

    def __str__(self):
        return "{}",format(self.nombre_zona)

class VehiculoChofer(models.Model):
    marca_vehiculo = models.CharField(max_length=50)
    placa_vehiculo = models.CharField(max_length=100)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    class Meta:
        db_table = "tp_vehiculo"
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"

    def __str__(self):
        return "{}".format(self.marca_vehiculo)


class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=50)
    apellido_cliente = models.CharField(max_length=100)
    cedula_cliente = models.CharField(max_length=100)
    telefono_cliente = models.CharField(max_length=10)
    correo_cliente = models.CharField(max_length=100)

    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "tp_cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return "{}".format(self.nombre_cliente)


class direccionesCliente(models.Model):
    direccion_cliente = models.CharField(max_length=50)
    referencia_cliente = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)


    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "tp_direccion_cliente"
        verbose_name = "Direccione Cliente"
        verbose_name_plural = "Direcciones Clientes"