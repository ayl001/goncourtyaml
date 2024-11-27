class grand_pere:
    a = 42

    def methode_a_leguer(self):
        return 42


class pere(grand_pere):
    def do_some_staff(self):
        print("a ? connaîs pas")


class petit_fils(pere):
    def methode_demarrage(self):
        print(self.methode_a_leguer())


if __name__ == '__main__':
    albert = petit_fils()
    albert.methode_demarrage()
else:
    print("Caramba! Encore raté")