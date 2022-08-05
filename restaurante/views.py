import json
import os

from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views.generic import CreateView,View
from django.shortcuts import render, redirect, get_object_or_404


from pedidos import settings
from restaurante.forms import CategoryForm, RestauranteForm, EmpresaForm,ProductForm
from restaurante.models import Category, Restaurante, Chofer, Zonas, VehiculoChofer, Empresa, DetSale
from restaurante.forms import SaleForm
from restaurante.models import Sale, Product


def restaurante(request):
    return render(request, "admin_restaurante.html")


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('inicio')
    permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


def consultar_categoria(request):
    categoria = Category.objects.all()
    count_c = categoria.count()
    return render(request, "categoria/consultar_categoria.html", {'categoria_ls': categoria, 'count_ca': count_c})


def crear_categoria(request):
    if request.method == "POST":
        categoryForm = CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('consultar_categoria')
        else:
            categoryForm = CategoryForm()
    else:
        categoryForm = CategoryForm()
    return render(request, "categoria/crear_categoria.html", {'categoryForm': categoryForm})


def editar_categoria(request, id):
    if request.method == "POST":
        categoria = get_object_or_404(Category, pk=id)
        categoryForm = CategoryForm(request.POST or None, instance=categoria)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('consultar_categoria')
        else:
            categoryForm = CategoryForm(instance=categoria)
    else:
        categoria = get_object_or_404(Category, pk=id)
        categoryForm = CategoryForm(instance=categoria)
    return render(request, "categoria/editar_categoria.html", {'categoryForm': categoryForm})


def eliminar_categoria(request, id):
    if request.method == "POST":
        categoria = get_object_or_404(Category, pk=id)
        categoryForm = CategoryForm(request.POST or None, instance=categoria)
        if categoryForm.is_valid():
            categoria.estado = 0
            categoria.save()
            return redirect('consultar_categoria')
    else:  ##GET
        categoria = get_object_or_404(Categoria, pk=id)
        categoryForm = CategoryForm(instance=categoria)
    return render(request, "categoria/eliminar_categoria.html", {'categoryForm': categoryForm})


def consultar_restaurante(request):
    restaurante = Restaurante.objects.all()
    return render(request, "restaurante/consultar_restaurante.html", {'restaurante_ls': restaurante})


def crear_restaurante(request):
    if request.method == "POST":
        restauranteForm = RestauranteForm(request.POST)
        if restauranteForm.is_valid():
            restauranteForm.save()
            return redirect('consultar_restaurante')
        else:
            restauranteForm = RestauranteForm()
    else:
        restauranteForm = RestauranteForm()
    return render(request, "restaurante/crear_restaurante.html", {'restauranteForm': restauranteForm})


def editar_restaurante(request, id):
    if request.method == "POST":
        restaurante = get_object_or_404(Restaurante, pk=id)
        restauranteForm = RestauranteForm(request.POST or None, instance=restaurante)
        if restauranteForm.is_valid():
            restauranteForm.save()
            return redirect('consultar_restaurante')
        else:
            restauranteForm = RestauranteForm(instance=restaurante)
    else:
        restaurante = get_object_or_404(Restaurante, pk=id)
        restauranteForm = RestauranteForm(instance=restaurante)
    return render(request, "restaurante/editar_restaurante.html", {'restauranteForm': restauranteForm})


def eliminar_restaurante(request, id):
    if request.method == "POST":
        restaurante = get_object_or_404(Restaurante, pk=id)
        restauranteForm = RestauranteForm(request.POST or None, instance=restaurante)
        if restauranteForm.is_valid():
            restaurante.estado = 0
            restaurante.save()
            return redirect('consultar_restaurante')
    else:  ##GET
        restaurante = get_object_or_404(Restaurante, pk=id)
        restauranteForm = RestauranteForm(instance=restaurante)
    return render(request, "restaurante/eliminar_restaurante.html", {'restauranteForm': restauranteForm})


def consultar_producto(request):
    productos = Product.objects.all()
    return render(request, "productos/consultar_productos.html", {'producto_ls': productos})


def crear_producto(request):
    if request.method == "POST":
        productoForm = ProductForm(request.POST)
        if productoForm.is_valid():
            productoForm.save()
            return redirect('consultar_restaurante')
        else:
            productoForm = ProductForm()
    else:
        productoForm = ProductForm()
    return render(request, "restaurante/crear_restaurante.html", {'restauranteForm': productoForm})


def editar_producto(request, id):
    if request.method == "POST":
        producto = get_object_or_404(Product, pk=id)
        productoForm = ProductForm(request.POST or None, instance=producto)
        if productoForm.is_valid():
            productoForm.save()
            return redirect('consultar_producto')
        else:
            productoForm = ProductForm(instance=producto)
    else:
        producto = get_object_or_404(Product, pk=id)
        productoForm = ProductForm(instance=producto)
    return render(request, "productos/editar_productos.html", {'productoForm': productoForm})


def eliminar_producto(request, id):
    if request.method == "POST":
        producto = get_object_or_404(Product, pk=id)
        productoForm = ProductForm(request.POST or None, instance=producto)

        if productoForm.is_valid():
            producto.estado = 0
            producto.save()
            return redirect('consultar_producto')
    else:  ##GET
        producto = get_object_or_404(Product, pk=id)
        productoForm = ProductForm(instance=producto)

    return render(request, "productos/eliminar_productos.html", {'productoForm': productoForm})


def consultar_empresa(request):
    empresa = Empresa.objects.all()
    return render(request, "empresa/consultar_empresa.html", {'empresa_ls': empresa})


def crear_empresa(request):
    if request.method == "POST":
        empresaForm = EmpresaForm(request.POST)
        if empresaForm.is_valid():
            empresaForm.save()
            return redirect('consultar_empresa')
        else:
            empresaForm = EmpresaForm()
    else:
        empresaForm = EmpresaForm()
    return render(request, "empresa/crear_empresa.html", {'empresaForm': empresaForm})


def editar_empresa(request, id):
    if request.method == "POST":
        empresa = get_object_or_404(Empresa, pk=id)
        empresaForm = EmpresaForm(request.POST or None, instance=empresa)
        if empresaForm.is_valid():
            empresaForm.save()
            return redirect('consultar_empresa')
        else:
            empresaForm = EmpresaForm(instance=empresa)
    else:
        empresa = get_object_or_404(Empresa, pk=id)
        empresaForm = EmpresaForm(instance=empresa)
    return render(request, "empresa/editar_empresa.html", {'empresaForm': empresaForm})


def eliminar_empresa(request, id):
    if request.method == "POST":
        empresa = get_object_or_404(Empresa, pk=id)
        empresaForm = EmpresaForm(request.POST or None, instance=empresa)
        if empresaForm.is_valid():
            empresa.estado = 0
            empresa.save()
            return redirect('consultar_empresa')
    else:  ##GET
        empresa = get_object_or_404(Empresa, pk=id)
        empresaForm = EmpresaForm(instance=empresa)
    return render(request, "empresa/eliminar_empresa.html", {'empresaForm': empresaForm})


def consultar_chofer(request):
    chofer = Chofer.objects.all()
    return render(request, "chofer/consultar_chofer.html", {'chofer_ls': chofer})


def crear_chofer(request):
    if request.method == "POST":
        choferForm = ChoferForm(request.POST)
        if choferForm.is_valid():
            choferForm.save()
            return redirect('consultar_chofer')
        else:
            choferForm = ChoferForm()
    else:
        choferForm = ChoferForm()
    return render(request, "chofer/crear_chofer.html", {'choferForm': choferForm})


def editar_chofer(request, id):
    if request.method == "POST":
        chofer = get_object_or_404(Chofer, pk=id)
        choferForm = ChoferForm(request.POST or None, instance=chofer)
        if choferForm.is_valid():
            choferForm.save()
            return redirect('consultar_chofer')
        else:
            choferForm = ChoferForm(instance=chofer)
    else:
        chofer = get_object_or_404(Chofer, pk=id)
        choferForm = ChoferForm(instance=chofer)
    return render(request, "chofer/editar_chofer.html", {'choferForm': choferForm})


def eliminar_chofer(request, id):
    if request.method == "POST":
        chofer = get_object_or_404(Chofer, pk=id)
        choferForm = ChoferForm(request.POST or None, instance=chofer)
        if choferForm.is_valid():
            chofer.estado = 0
            chofer.save()
            return redirect('consultar_chofer')
    else:  ##GET
        chofer = get_object_or_404(Chofer, pk=id)
        choferForm = ChoferForm(instance=chofer)
    return render(request, "chofer/eliminar_chofer.html", {'choferForm': choferForm})


def consultar_zona(request):
    zona = Zonas.objects.all()
    return render(request, "zonas/consultar_zona.html", {'zona_ls': zona})


def crear_zona(request):
    if request.method == "POST":
        zonaForm = ZonaForm(request.POST)
        if zonaForm.is_valid():
            zonaForm.save()
            return redirect('consultar_zona')
        else:
            zonaForm = ZonaForm()
    else:
        zonaForm = ZonaForm()
    return render(request, "zonas/crear_zona.html", {'zonaForm': zonaForm})


def editar_zona(request, id):
    if request.method == "POST":
        zona = get_object_or_404(Zonas, pk=id)
        zonaForm = ZonaForm(request.POST or None, instance=zona)
        if zonaForm.is_valid():
            zonaForm.save()
            return redirect('consultar_zona')
        else:
            zonaForm = ZonaForm(instance=zona)
    else:
        zona = get_object_or_404(Zonas, pk=id)
        zonaForm = ZonaForm(instance=zona)
    return render(request, "zonas/editar_zona.html", {'zonaForm': zonaForm})


def eliminar_zona(request, id):
    if request.method == "POST":
        zona = get_object_or_404(Zonas, pk=id)
        zonaForm = ZonaForm(request.POST or None, instance=zona)
        if zonaForm.is_valid():
            zona.estado = 0
            zona.save()
            return redirect('consultar_zona')
    else:  ##GET
        zona = get_object_or_404(Zonas, pk=id)
        zonaForm = ZonaForm(instance=zona)
    return render(request, "zonas/eliminar_zona.html", {'zonaForm': zonaForm})


def consultar_vehiculo(request):
    vehiculo = VehiculoChofer.objects.all()
    return render(request, "vehiculos/consultar_vehiculo.html", {'vehiculo_ls': vehiculo})


def consultar_factura(request):
    factura = Sale.objects.all()
    return render(request, "sale/consultar_factura.html", {'factura_ls': factura})


def editar_factura(request, id):
    if request.method == "POST":
        sale = get_object_or_404(Sale, pk=id)
        saleForm = SaleForm(request.POST or None, instance=sale)
        if saleForm.is_valid():
            saleForm.save()
            return redirect('consultar_vehiculo')
        else:
            saleForm = SaleForm(instance=sale)
    else:
        sale = get_object_or_404(Sale, pk=id)
        saleForm = SaleForm(instance=sale)
    return render(request, "sale/editar_factura.html", {'saleForm': saleForm})


def crear_vehiculo(request):
    if request.method == "POST":
        vehiculoForm = VehiculoForm(request.POST)
        if vehiculoForm.is_valid():
            vehiculoForm.save()
            return redirect('consultar_vehiculo')
        else:
            vehiculoForm = VehiculoForm()
    else:
        vehiculoForm = VehiculoForm()
    return render(request, "vehiculo/crear_vehiculo.html", {'vehiculoForm': vehiculoForm})


def editar_vehiculo(request, id):
    if request.method == "POST":
        vehiculo = get_object_or_404(VehiculoChofer, pk=id)
        vehiculoForm = VehiculoForm(request.POST or None, instance=vehiculo)
        if vehiculoForm.is_valid():
            vehiculoForm.save()
            return redirect('consultar_vehiculo')
        else:
            vehiculoForm = VehiculoForm(instance=vehiculo)
    else:
        vehiculo = get_object_or_404(VehiculoChofer, pk=id)
        vehiculoForm = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculo/editar_vehiculo.html", {'vehiculoForm': vehiculoForm})


def eliminar_vehiculo(request, id):
    if request.method == "POST":
        vehiculo = get_object_or_404(VehiculoChofer, pk=id)
        vehiculoForm = VehiculoForm(request.POST or None, instance=zona)
        if vehiculoForm.is_valid():
            vehiculo.estado = 0
            vehiculo.save()
            return redirect('consultar_vehiculo')
    else:  ##GET
        vehiculo = get_object_or_404(VehiculoChofer, pk=id)
        vehiculoForm = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculo/eliminar_vehiculo.html", {'vehiculoForm': vehiculoForm})


class SaleInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/pdf.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('consultar_categoria'))
