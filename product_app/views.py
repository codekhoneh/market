from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = "product_app/product_list.html"
    context_object_name = "products"
    paginate_by = 3

    # def get_queryset(self):
    #     queryset = Product.objects.filter(is_available=True)
    #     price_filters = self.request.GET.getlist("price")
    #     color_filters = self.request.GET.getlist("color")
    #     size_filters = self.request.GET.getlist("size")
    #     from django.db.models import Q

    #     price_map = {
    #         "0-100": (0, 100),
    #         "100-200": (100, 200),
    #         "200-300": (200, 300),
    #     }

    #     if price_filters:
    #         q = Q()
    #         for p in price_filters:
    #             min_p, max_p = price_map[p]
    #             q |= Q(price__gte=min_p, price__lte=max_p)
    #         queryset = queryset.filter(q)

    #     if color_filters:
    #         queryset = queryset.filter(color__id__in=color_filters)

    #     if size_filters:
    #         queryset = queryset.filter(size__id__in=size_filters)

    #     return queryset.distinct()






class ProductDetailView(DetailView):
    model = Product
    template_name = "product_app/product_detail.html"
    context_object_name = "product_d"
    slug_field = "slug"
    slug_url_kwarg = "slug"


# # Create your views here.
