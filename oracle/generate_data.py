from faker import Faker
fake = Faker('es_ES')

name = fake.name()
address = fake.address()
text = fake.text()

print(name, address)
print(text)