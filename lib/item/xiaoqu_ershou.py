class XiaoQuErShou(object):
    def __init__(self, xiaoqu_id, total_price, price, name, house_type, house_size, house_dir):
        self.xiaoqu_id = xiaoqu_id
        self.total_price = total_price
        self.price = price
        self.name = name
        self.house_type = house_type
        self.house_size = house_size
        self.house_dir = house_dir

    def text(self):
        return self.xiaoqu_id + ',' + \
                self.total_price + ',' + \
                self.price + ',' + \
                self.name + ',' + \
                self.house_type + ',' + \
                self.house_size + ',' + \
                self.house_dir + '\n'
