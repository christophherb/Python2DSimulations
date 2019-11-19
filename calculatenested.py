class Nested:
    '''calculate the parameters of a nested optic according to Oliver Zimmer
    Keyword parameters:
    L -- Distance of the focal points to the small half axis
    l -- half length of a mirror piece 
    lam -- wavelength of the expected neutrons in Angstrom
    max_m -- the critical angle in multiples of the Ni critangle
    '''
    def __init__(self,L= 600,l=60,lam= 4*10**(-10),max_m = 10):
        self.L = L
        self.l = l
        self.lam = lam
        self.max_m = max_m
        self.theta_deg = 8.782/8.86/10 * lam*10**10*max_m
        self.theta = self.theta_deg/180*np.pi
        self.bks = {}
        self.aks = {}
        self.yks = {}
        self.check = {}
    def calcb1(self):
        '''
        claculates b1 according to OLIVER ZIMMER and adds it to the bks dict  
        using the wavelength and critical angle of the mirror in a way to use most neutrons
        '''
        b1 = (-1/2*self.L**2*(1-np.tan(self.theta)**2)+self.L*(1/4*self.L**2*(1-np.tan(self.theta)**2)**2+(self.L**2-self.l**2)*np.tan(self.theta)**2)**0.5)**0.5
        self.bks['1'] =b1
        
        
    def yk(self,bk,x):
        '''
        returns the y value in an ellipse with a small half axis bk at a point x, L is taken from the class
        Keyword parameters:
        bk -- small half axis of the relevant ellipse
        x -- x value of the point on the ellipse
        '''
        return bk * (self.L**2 + bk**2 -x**2)**0.5/(self.L**2 + bk**2)**0.5
    def ykplus1(self,k):
        '''
        
        '''
        bk = self.bks['{}'.format(k)]
        a = bk*(self.L**2+bk**2-self.l**2)**0.5*(self.L-self.l)/((self.L**2+bk**2)**0.5*(self.L+self.l))
        self.bks['{}'.format(k+1)] = (((self.l**2+a**2-self.L**2)+((self.L**2-self.l**2-a**2)**2+4*a**2*self.L**2)**0.5)/2)**0.5
    def calc_bks(self,number = 5):
        for i in range(number-1):
            self.ykplus1(i+1)
    def calc_all(self,number,b1 = False):

        if b1:
            self.bks['1'] =b1
        else:
            self.calcb1()            
        for i in range(number):
            self.calc_bks(number)
            self.aks['{}'.format(i+1)] = (self.L**2+self.bks['{}'.format(i+1)]**2)**0.5
            self.yks['{}'.format(i+1)] = self.bks['{}'.format(i+1)] * (self.L**2+ self.bks['{}'.format(i+1)]**2-self.l**2)**0.5/(self.L**2+self.bks['{}'.format(i+1)]**2)**0.5
            self.check['{}'.format(i+1)] = (self.aks['{}'.format(i+1)]**2 -self.bks['{}'.format(i+1)]**2)**0.5
    def return_bs(self,number, b1 = False):
        self.calc_all(number,b1)
        bs = []
        for i in range(number):
            bs += [self.bks['{}'.format(i+1)]]
        return bs
    def return_ys(self):
        return [self.yks['{}'.format(i+1)] for i in range(len(self.yks))]