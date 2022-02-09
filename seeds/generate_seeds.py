from faker import Faker
from random import randint
import datetime as dt
import json

faker = Faker()

num_users = 30
num_properties = 10
num_reservations = 25
num_property_reviews = 15

password = '$2a$10$FB/BOAVhpuLvpOREQVmvmezD4ED/.JBIDRh70tGevYzYzQgFId2u.'

str_users = 'INSERT INTO users (name,email,password) VALUES'
def gen_user():
  return json.dumps((
    faker.name(),
    faker.email(),
    '$2a$10$FB/BOAVhpuLvpOREQVmvmezD4ED/.JBIDRh70tGevYzYzQgFId2u.'
  )).replace('[','(').replace(']',')')

str_properties = 'INSERT INTO properties (owner_id,title,description,thumbnail_photo_url,cover_photo_url,cost_per_night,parking_spaces,number_of_bathrooms,number_of_bedrooms,country,street,city,province,post_code) VALUES'
def gen_property():
  return json.dumps((
    randint(1,num_users),
    'title',
    faker.paragraph(),
    'https://i.imgur.com/Kq51Mia.jpg',
    'https://i.imgur.com/Bb1WTPa.jpg',
    randint(70,500),
    randint(0,4),
    randint(1,3),
    randint(1,6),
    'USA',
    faker.street_address(),
    faker.city(),
    faker.state(),
    faker.postalcode()
  )).replace('[','(').replace(']',')')

str_reservations = 'INSERT INTO reservations (start_date,end_date,property_id,guest_id) VALUES'
def gen_reservation():
  start = dt.date.today() - dt.timedelta(days=randint(5,500))
  end = start + dt.timedelta(days=randint(1,5))
  return json.dumps((
    f'{start:%Y-%m-%d}',
    f'{end:%Y-%m-%d}',
    randint(1,num_properties),
    randint(1,num_users)
  )).replace('[','(').replace(']',')')

str_property_reviews = 'INSERT INTO property_reviews (guest_id,property_id,reservation_id,rating,message) VALUES'
def gen_review():
  return json.dumps((
    randint(1,num_users),
    randint(1,num_properties),
    randint(1,num_reservations),
    randint(1,5),
    faker.paragraph()
  )).replace('[','(').replace(']',')')


def add_insert_commands(command,generator,number):
  result = command + '\n'
  result += ',\n'.join([generator() for _ in range(number)])
  result += ';\n\n'
  return result.replace('"',"'")

# Generate result string and save it to file
result = ''
result += add_insert_commands(str_users,gen_user,num_users)
result += add_insert_commands(str_properties,gen_property,num_properties)
result += add_insert_commands(str_reservations,gen_reservation,num_reservations)
result += add_insert_commands(str_property_reviews,gen_review,num_property_reviews)
print(result)

with open('seeds/01_seeds.sql','w') as file:
  file.seek(0)
  file.write(result)

print('DONE')