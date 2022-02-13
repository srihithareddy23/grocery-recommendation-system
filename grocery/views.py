from django.shortcuts import render
import csv
import os

# Create your views here.
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from .models import *
from .forms import  CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import joblib
from models_and_data import model
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import *
import requests
from django.contrib.auth.decorators import login_required

'''
def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		print("hello")
		form = CreateUserForm(request.POST)
		
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			role = form.cleaned_data.get('first_name')
			print("username=",username,"password=",password,"role=",role)
			
			

			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
	context = {'form':form}



	return render(request, 'register.html', context)
'''
@login_required(login_url='login')
def grocery(request,pk):
	objs=grocery_store.objects.all()
	list=[]
	for i in objs:
		if(i.Category not in list):
			list.append(i.Category)
	context={}
	for i in range(0,len(list)):
		x=grocery_store.objects.filter(Category=pk)

	print("hi.....",x)
		

	
	
	num={'x':x}
	return render (request,"grocery.html",num)
def home(request):
	
	context={'userid':request.user.id}
	return render (request,"home1.html",context)
'''
def login_request(request):
	if request.method == 'POST':
		
		username = request.POST.get('username')
		password =request.POST.get('password1')
		role = request.POST.get('first_name')
	

		
		
		

		user = authenticate(request, username=username, password=password)



		

		if user is not None:
			print("hey yo....",user.id)
			context={'userid':user.id}

			return render(request, 'home.html', context)

		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)
'''
@login_required(login_url='login')
def result(request,pk):
	x=joblib.load("finalized_model.sav")
	lis=pk
	print(lis)
	list1=[]
	list2=[]
	context={}
	
	for i in model.fun(lis)['Title']:
		list1.append(i)
	
	products=[]
	m=[]
	
	for i in list1:
		
		m+=grocery_store.objects.filter(Title=i)
		
		
	
	context={'x':m}
	print("hello.......",context)
	
	return render(request,"suggested_items.html",context)


	

	

	

	
	return render(request,"suggested_items.html")



class HomeView(TemplateView):
    template_name = "grocery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_products = Product.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        print(page_number)
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class AllProductsView( TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context

class ProductDetailView( TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context

class AddToCartView( TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = grocery_store.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
              
                cartproduct.save()
                
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, quantity=1)
             
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, quantity=1)
          
            cart_obj.save()

        return context

class ManageCartView( View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1

            cp_obj.save()
 
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
     
            cp_obj.save()
     
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
        
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("grocery:mycart")

class EmptyCartView( View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("grocery:mycart")

class MyCartView( TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class CheckoutView( CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("grocery:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)


   



            for cp in cart_obj.cartproduct_set.all():
                
                var=history.objects.create(CustomerID=self.request.user.id,Title=cp.product.Title)
                with open('C:/Users/snigdha/Documents/miniproject-master/models_and_data/history.csv', 'a',newline="") as File:
                    writer=csv.writer(File)
                
                    writer.writerow([self.request.user.id,cp.product.Title])
                var.save()
                print("saved:)",var)
            File.close()
           
                

        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "Khalti":
                return redirect(reverse("grocery:khaltirequest") + "?o_id=" + str(order.id))
            elif pm == "Esewa":
                return redirect(reverse("grocery:esewarequest") + "?o_id=" + str(order.id))
        else:
            return redirect("grocery:home")
        return super().form_valid(form)





class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("grocery:customerlogin")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("grocery:customerlogin")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("grocery:home1")

	# form_valid method is a type of post method and is available in createview formview and updateview

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        print("username=",uname,"password=",pword)
        usr = authenticate(username=uname, password=pword)
        if usr is not None :
            login(self.request, usr)
            context={'userid':usr.id}
            return render(self.request, 'home1.html', context)
            

        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AboutView( TemplateView):
    template_name = "about.html"



class ContactView(TemplateView):
    template_name = "contactus.html"



class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("grocery:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
	template_name = "search.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		kw = self.request.GET.get("keyword")
		print("hello=====",kw)
		results = grocery_store.objects.filter(
			Q(Title__icontains=kw) )
		print(results)
		context["results"] = results
		return context

class PasswordForgotView(FormView):
	template_name = "forgotpassword.html"
	form_class = PasswordForgotForm
	success_url = "/forgot-password/?m=s"


	def form_valid(self, form):
		# get email from user
		email = form.cleaned_data.get("email")
		# get current host ip/domain
		url = self.request.META['HTTP_HOST']
		# get customer and then user
		customer = Customer.objects.get(user__email=email)
		user = customer.user
		# send mail to the user with email
		text_content = 'Please Click the link below to reset your password. '
		html_content = url + "/password-reset/" + email + \
			"/" + password_reset_token.make_token(user) + "/"
		send_mail(
			'Password Reset Link | Django Ecommerce',
			text_content + html_content,
			settings.EMAIL_HOST_USER,
			[email],
			fail_silently=False,
		)
		return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("grocery:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

# admin pages


class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("grocery:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"


class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("grocery:adminorderdetail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("grocery:adminproductlist")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)

