from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': 'Nombre de la categoría'}),
            'icon': forms.TextInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': 'Emoji (🥦) o clase Bootstrap (bi-tag)'}),
        }
        help_texts = {
            'icon': 'Puedes usar un emoji o una clase de Bootstrap Icons (ej: bi-apple).',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'is_on_offer', 'offer_price', 'unit', 'stock', 'min_stock', 'description', 'image', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': 'Nombre del producto'}),
            'category': forms.Select(attrs={'class': 'form-select border-0 px-4'}),
            'price': forms.NumberInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': '0.00'}),
            'is_on_offer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_price': forms.NumberInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': '0.00'}),
            'unit': forms.Select(attrs={'class': 'form-select border-0 px-4'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': 'Cantidad'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control border-0 px-4', 'placeholder': 'Mínimo'}),
            'description': forms.Textarea(attrs={'class': 'form-control shadow-sm rounded-4 border-2 px-4', 'rows': 4, 'placeholder': 'Describe el producto...', 'style': 'border-color: var(--brand-light) !important;'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control d-none', 'id': 'product-image-input'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
