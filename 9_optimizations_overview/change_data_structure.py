count = 1000000
my_list = list(range(count))
my_set = set(range(count))

@profile
def search_in_list(my_list):
    print(123456 in my_list)

@profile
def search_in_set(my_set):
    print(123456 in my_set)


search_in_list(my_list)
search_in_set(my_set)
