from rest_framework.test import APITestCase
from store.models import Product

class ProductCreateTest(APITestCase):
	def test_create_product(self):
		initial_product_count = Product.objects.count()
		prod_attrs = {
		'name' : 'test',
		'description': 'tests description',
		'price': '12.09',
		}

		response = self.client.post('/api/v1/products/new', prod_attrs)
		if response.status_code != 201:
			print(response.data)
		self.assertEqual(response.status_code, 201)

		for attr, values in prod_attrs.items():
			self.assertEqual(response.data[attr], values)
		self.assertEqual(response.data['current_price'], float(prod_attrs['price']))
		self.assertEqual(response.data['is_on_sale'], False)
		self.assertEqual(Product.objects.count(), initial_product_count+1)

class ProductDestroyTest(APITestCase):

	def test_product_delete(self):
		initial_product_count = Product.objects.count()
		product_id = Product.objects.first().id
		response = self.client.delete('/api/v1/products/{}/'.format(product_id))
		self.assertEqual(Product.objects.count(), initial_product_count-1)
		self.assertRaises(Product.DoesNotExist, Product.objects.get, id=product_id)

class ProductListTest(APITestCase):
	def test_Product_List(self):
		response = self.client.get('/api/v1/products/')
		product_count = Product.objects.count()
		self.assertEqual(response.data['count'], product_count)
		self.assertIsNone(response.data['next'])
		self.assertIsNone(response.data['previous'])
		self.assertEqual(len(response.data['results']), product_count)

class ProductUpdateTest(APITestCase):	
	def test_update_product(self):
		product = Product.objects.first()
		response = self.client.patch('/api/v1/products/{}/'.format(product.id), {
					'name' : 'New Product',
					'description' : 'Test new product',
					'price' : 122.12,

				}, 
				format='json',)
		updated = Product.objects.get(id=product.id)
		self.assertEqual(updated.name, 'New Product')	