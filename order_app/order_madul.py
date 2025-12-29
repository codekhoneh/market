from product_app.models import Product
from itertools import takewhile

ORDER_SESSION_ID = 'cart'

class Order:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(ORDER_SESSION_ID, {})

    def _unique_id(self, product_id, color, size):
        return f"{product_id}--{color}--{size}"

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for key, raw in list(self.cart.items()):
            item = dict(raw)

            pid = item.get('id') or str(key).split('--', 1)[0]
            try:
                pid_int = int(pid)
            except:
                continue

            try:
                product_d = Product.objects.get(id=pid_int)
            except Product.DoesNotExist:
                continue

            quantity = int(item.get('quantity', 0))
            price = float(item.get('price', 0))

            item['product_d'] = product_d
            item['total'] = quantity * price
            item['unique_id'] = self._unique_id(
                product_d.id,
                item.get('color'),
                item.get('size')
            )

            yield item

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()
    def add(self, product, quantity=1, color=None, size=None):
      unique = self._unique_id(product.id, color, size)

      if unique not in self.cart:
            self.cart[unique] = {
                  'id': product.id,
                  'quantity': 0,
                  'price': str(product.price),
                  'color': color,
                  'size': size,
            }

      self.cart[unique]['quantity'] += int(quantity)
      self.save()