from MailSystem.py import MailSystem
# from Scanner.py import Scanner
from Telephone.py import Telephone
from Connection.py import Connection
def main():
    system = MailSystem(20)
    #console = Scanner()
    p = Telephone()
    c = Connection(system, p)
    p.run(c)