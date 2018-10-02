import random
# generates a 3d position (x,y,z) randomly

x_range = [5000, 33000]
y_range = [6000, 25000]
z_range = [0, 515]

for i in range(20):
    x_value = random.randint(x_range[0],x_range[1])
    y_value = random.randint(y_range[0],y_range[1])
    z_value = random.randint(z_range[0],z_range[1])
  
    print("{}: {} {} {}".format(i+1, x_value, y_value, z_value))
