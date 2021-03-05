from MailSystem.py import MailSystem
from Telephone.py import Telephone
from Connection.py import Connection
def main():
    system = MailSystem(20)
    p = Telephone()
    c = Connection(system, p)
    p.run(c)