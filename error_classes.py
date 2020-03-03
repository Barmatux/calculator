
class CalcError(Exception):

    def __init__(self, mes='Error'):
        self.mes = mes

    def __repr__(self):
        return str(self.mes)