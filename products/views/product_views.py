from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, UpdateView
from products.forms import *
from products.models import *


class ProductListView(ListView):
    model = Product
    # paginate_by = 12  # pagination이 필요한 경우 사용


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        reviews = product.reviews.all()
        review_data = []
        for review in reviews:
            review_images = review.images.all()
            review_data.append({
                'review': review,
                'images': review_images,
            })

        inquiries = product.inquiries.all()
        inquiry_data = []
        for inquiry in inquiries:
            try:
                inquiry_data.append({
                    'inquiry': inquiry,
                    'answer': inquiry.answer.all(),
                })
            except:
                inquiry_data.append({
                    'inquiry': inquiry,
                })

        context['category'] = product.category
        context['review_form'] = ReviewForm()
        context['review_image_form'] = ReviewImageForm() 
        context['reviews'] = review_data
        context['inquiry'] = inquiry_data
        return context


class ProductCreateView(FormMixin, TemplateView):
    model = Product
    second_model = Category
    form_class = ProductForm
    second_form_class = CategoryForm
    template_name = 'products/product_create.html'


    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'pk': self.model.objects.last().pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.form_class)
        context['category_form'] = self.get_form(self.second_form_class)
        return context
    

    def post(self, request, *args, **kwargs):
        product_form = self.get_form(self.form_class)
        category_form = self.get_form(self.second_form_class)
        if product_form.is_valid() and category_form.is_valid():
            product = product_form.save(commit=False)
            category = category_form.save()
            product.category = category
            product.save()
            return self.form_valid(product_form)
        return self.form_invalid(product_form)


    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        product_form = self.get_form(form_class)
        category_form = self.get_form(self.second_form_class)
        return self.render_to_response(self.get_context_data(product_form=product_form, category_form=category_form))


    def form_valid(self, form):
        return super().form_valid(form)
    

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    second_model = Category
    template_name = 'products/product_update.html'
    form_class = ProductForm
    second_form_class = CategoryForm


    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        product_pk = self.kwargs.get('product_pk', 0)
        product = self.model.objects.get(pk=product_pk)
        if 'product_form' not in context:
            context['product_form'] = self.form_class(instance=product)
        if 'category_form' not in context:
            context['category_form'] = self.second_form_class(instance=product.category)
        context['product_pk'] = product_pk
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_pk = kwargs['product_pk']
        product = self.model.objects.get(pk=product_pk)
        product_form = self.form_class(request.POST, request.FILES, instance=product)
        category_form = self.second_form_class(request.POST, instance=product.category)
        if product_form.is_valid() and category_form.is_valid():
            product_form.save()
            category_form.save()
            return redirect('products:product_detail', product_pk)
        else:
            return self.render_to_response(self.get_context_data(product_form=product_form, category_form=category_form))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:product_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)