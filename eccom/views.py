from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
# Create your views here.
from eccom.carrito import Carrito
from eccom.context_processor import total_carrito
from eccom.models import producto
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Obtener los datos adicionales del formulario
            edad = request.POST.get('edad')
            juego_favorito = request.POST.get('juego_favorito')
            plataforma_favorita = request.POST.get('plataforma_favorita')
            lugar_residencia = request.POST.get('lugar_residencia')
            sexo = request.POST.get('sexo')
            genero = request.POST.get('genero')
            # Crear un perfil de usuario con los datos adicionales
            perfil_usuario = PerfilUsuario.objects.create(
                usuario=user,
                edad=edad,
                juego_favorito=juego_favorito,
                plataforma_favorita=plataforma_favorita,
                lugar_residencia=lugar_residencia,
                sexo=sexo,
                genero=genero
            )
            perfil_usuario.save()
            messages.success(request, "El usuario ha sido registrado exitosamente!")
            return render(request, 'registration/login.html')
        else:
            messages.error(request, "No se pudo registrar el usuario, por favor inténtalo de nuevo.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    
def login(request):
    return render(request,'login.html')
def exit(request):
    logout(request)
    return redirect('/');
def perfil(request):
    usuario = request.user
    
    # Obtener el perfil del usuario actual
    perfil = PerfilUsuario.objects.get(usuario=usuario)
    return render(request, 'perfil.html', {"perfil": perfil, 'usuario': usuario})
def index(request):
    
    articulos = producto.objects.all()
    paginator = Paginator(articulos, 12)  # Cambia 4 al número deseado de artículos por página
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'articulos': articulos})

def todo(request):
    query = request.GET.get('q')
    categoria = request.GET.get('categoria')  # Obtener el valor de la categoría seleccionada, si lo hay
    
    # Filtrar los productos por nombre, categoría o plataforma si hay una consulta de búsqueda
    if query:
        articulos = producto.objects.filter(Q(nombre__icontains=query) | Q(categoria__icontains=query) | Q(platform__icontains=query))
    else:
        articulos = producto.objects.all()
    
    # Filtrar por categoría si se ha seleccionado una
    if categoria and categoria != '0':
        articulos = articulos.filter(categoria=categoria)  # Ajusta esto según tu modelo de Producto
        
    paginator = Paginator(articulos, 6)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    
    return render(request, 'todos.html', {'articulos': articulos})

def detalle_articulo(request, producto_id):
    usuario = request.user
    carrito = Carrito(request)
    articulo = producto.objects.get(id=producto_id)
    return render(request, 'detalle_articulo.html', {'articulo': articulo, 'usuario': usuario})
@login_required
def carrito(request):
    usuario = request.user
    return render(request,'carrito_index.html', {'usuario': usuario});

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
   # `Producto = producto.objects.get(id=producto_id)` is a query in Django that retrieves a single
   # instance of the `producto` model from the database based on the `id` provided in the
   # `producto_id` variable. This line of code is fetching a specific product object with the given
   # `id` for further processing in the view functions.
    Producto = producto.objects.get(id=producto_id)
    carrito.agregar(Producto)
    return redirect("carrito")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    Producto = producto.objects.get(id=producto_id)
    carrito.eliminar(Producto)
    return redirect("carrito")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    Producto = producto.objects.get(id=producto_id)
    carrito.restar(Producto)
    return redirect("carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carrito")


def orde(request):
    if request.method == 'POST':
        carrito = Carrito(request)
        if carrito.carrito:  # Verifica si hay elementos en el carrito
            for key, value in carrito.carrito.items():
                plataforma = value['plataforma']
                categoria = value['categoria']
               
               
                
                if categoria=="Aventura":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.ventas_compradas is None:
                     perfil_usuario.ventas_compradas = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Aventura":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coaventura is None:
                     perfil_usuario.coaventura = 0 # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coaventura += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Plataforma":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coplataforma is None:
                     perfil_usuario.coplataforma = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coplataforma += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Accion":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coaccion is None:
                     perfil_usuario.coaccion = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coaccion += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Estrategia":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coestrategia is None:
                     perfil_usuario.coestrategia = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coestrategia += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Deportivo":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.codeportivo is None:
                     perfil_usuario.codeportivo = 0  # o cualquier otro valor predeterminado que desees
                    
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.codeportivo += 1
                    perfil_usuario.ventas_compradas += 1
                   
                    perfil_usuario.save()
                if categoria=="Terror":
                        # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coterror is None:
                     perfil_usuario.coterror = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coterror += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Rol":
                        # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.corol is None:
                     perfil_usuario.corol = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.corol += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Musicales":
                        # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.comusicales is None:
                     perfil_usuario.comusicales = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.comusicales += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                
                    
                
                if plataforma == "X360":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coxbox is None:
                     perfil_usuario.coxbox = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.coxbox += 1
                    perfil_usuario.save()
                if plataforma == "PS3" or plataforma == "PSP" or plataforma == "PS4":
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coplay is None:
                     perfil_usuario.coplay = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.coplay += 1
                    perfil_usuario.save()
                if plataforma == "WII" or plataforma == "3DS" or plataforma == "WIIU":
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.conintendo is None:
                     perfil_usuario.conintendo = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.conintendo += 1
                    perfil_usuario.save()

            # Limpia el carrito después de guardar los elementos en la base de datos
            carrito.limpiar()

            return render(request,'confirmacion.html')

    total_carrito_value = total_carrito(request)
    
    host = request.get_host()
    
  
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_carrito_value['total_carrito'],  # Utiliza el total del carrito obtenido
        'invoice': uuid.uuid4(),
        'currency_code': 'MXN',
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        
        'paypal': paypal_payment,
         
    }
    
    return render(request,'orde.html',context)
def confirmacion(request):
    return render(request, "confirmacion.html")
@login_required
def favorito(request):
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)

    # Obtener la lista de favoritos del usuario
    favoritos_usuario = perfil_usuario.favoritos.all()

    # Renderizar la página de favoritos con los productos favoritos del usuario
    return render(request, 'favoritos.html', {'favoritos_usuario': favoritos_usuario})
@login_required
def agregar_favorito(request, producto_id):
     # Obtener el producto por su ID
    Producto = producto.objects.get(id=producto_id)

    # Obtener o crear el perfil de usuario asociado al usuario actual
    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)

    # Agregar el ID del producto a la lista de favoritos del usuario
    perfil_usuario.favoritos.add(producto_id)
    carrito = Carrito(request)
    Producto = producto.objects.get(id=producto_id)
    carrito.agregar(Producto)

    # Redirigir a la página de favoritos o a donde desees
    return redirect('fav')


@login_required
def eliminar_favorito(request, producto_id):
    # Obtener el producto por su ID
    Producto_a_eliminar = producto.objects.get(id=producto_id)

    # Obtener el perfil de usuario asociado al usuario actual
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)

    # Eliminar el producto de la lista de favoritos del usuario
    perfil_usuario.favoritos.remove(Producto_a_eliminar)

    # Redirigir a la página de favoritos o a donde desees
    return redirect('fav')



def buscar_productops3(request):
    # Realiza la búsqueda en la base de datos
    articulos = producto.objects.filter(platform='PS3')
    
    
    paginator = Paginator(articulos, 3)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    # Pasa los resultados a la plantilla
    return render(request, 'todos.html', {'articulos': articulos})

def buscar_productowii(request):
    # Realiza la búsqueda en la base de datos
   
    articulos = producto.objects.filter(platform='3DS')
    paginator = Paginator(articulos, 3)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    # Pasa los resultados a la plantilla
    # Pasa los resultados a la plantilla
    return render(request, 'todos.html', {'articulos': articulos})

def buscar_productox360(request):
    # Realiza la búsqueda en la base de datos
    
    articulos = producto.objects.filter(platform='X360')
    
    paginator = Paginator(articulos, 3)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    # Pasa los resultados a la plantilla
    return render(request, 'todos.html', {'articulos': articulos})
