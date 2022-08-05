from datetime import datetime
from django import forms


from restaurante.models import Category, Product, Client, Sale, VehiculoChofer, Zonas, Chofer, Empresa, Restaurante


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = ['name', 'desc']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control'
                }
            ),
            'desc': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'cat': forms.Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_birthday': forms.DateInput(format='%Y-%m-%d',
                                       attrs={
                                           'value': datetime.now().strftime('%Y-%m-%d'),
                                       }
                                       ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': forms.Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class TestForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'date_joined': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    #'value': forms.datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }




class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nombre_restaurante', 'direccion', 'pagina_web', 'telefono', 'actividad', 'email', 'categoria']
        widgets = {
            'nombre_restaurante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su producto'
            }
            ),

            'direccion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese un producto'}),
            'pagina_web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un precio'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un precio'}),
            'actividad': forms.Select(attrs={'class': 'custom-select', 'id': 'inputState'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un precio'}),
            'categoria': forms.Select(attrs={'class': 'custom-select', 'id': 'inputState'}),
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre_empresa', 'direccion_empresa', 'telefono_empresa', 'email_empresa']
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la empresa'
            }
            ),

            'direccion_empresa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese una direccion'}),
            'telefono_empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero'}),
            'email_empresa': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Numero'}),
        }


class ChoferForm(forms.ModelForm):
    class Meta:
        model = Chofer
        fields = ['nombre_chofer', 'apellido_chofer', 'telefono_chofer', 'email_chofer', 'empresa']
        widgets = {
            'nombre_chofer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese Chofer'
            }
            ),
            'apellido_chofer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese Chofer'
            }
            ),

            'telefono_chofer': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese una direccion'}),
            'email_chofer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero'}),
            'empresa': forms.Select(attrs={'class': 'custom-select', 'id': 'inputState'}),
        }


class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zonas
        fields = ['nombre_zona', 'chofer']
        widgets = {
            'nombre_zona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese Chofer'}),
            'chofer': forms.Select(attrs={'class': 'custom-select', 'id': 'inputState'}),
        }


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = VehiculoChofer
        fields = ['marca_vehiculo', 'placa_vehiculo', 'chofer']
        widgets = {
            'marca_vehiculo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese Chofer'}),
            'placa_vehiculo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese Chofer'}),
            'chofer': forms.Select(attrs={'class': 'custom-select', 'id': 'inputState'}),
        }
