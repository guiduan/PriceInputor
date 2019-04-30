class GrandPa:
    def __init__(self, n, a):
        self.name = n
        self.age = a

    def speak(self):
        print("%s 说：我今年 %d 岁。" % (self.name, self.age))


if __name__ == '__main__':
    grandpa = GrandPa('yeye',80)
    grandpa.speak()
