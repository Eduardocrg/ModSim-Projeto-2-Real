import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np


########################### Primeira Iteração ###########################
####################### só água a 0 graus e refri #######################

def Urefri_e_agua(Y, t):
    Tagua= Y[0]
    Trefri= Y[1]
    deltaT= Tagua- Trefri
    crefri= 4.18 #J/g K
    mrefri= 365.75  #g
    Klata= 205 #W/m K
    dlata= 8.5e-5  #m
    hagua= 650    #W/ m^2 K
    Alata= 2*math.pi*3e-2*12.5e-2+ 2*(math.pi*0.03**2)   #considerando o diametro de 6cm e altura de 12.5 cm #m^2
    magua= 0.2*0.2*0.25*997*1000 # considerando uma caixa de isopor com volume de 0.2m por 0.2m por 0.25m #g
    cagua= 4.18 #J/g K
    
    
    a= 1/(mrefri*crefri)

    b= 1/(hagua*Alata)
    c= dlata/(Klata*Alata)
    d= b+c
    e= deltaT/d

    f= a*e
    
    g= 1/(magua*cagua)
    h= -g*e
    return h, f

Y=[0,20]

lista_tempo= np.arange(0, 500, 1)

Solucao= odeint(Urefri_e_agua, Y, lista_tempo)

REFRI= Solucao[:,1]
AGUA= Solucao[:,0]

plt.plot(lista_tempo/60, REFRI, label='Refrigerante')
plt.plot(lista_tempo/60, AGUA, label='Água')
plt.legend()
plt.xlabel('Tempo (min)')
plt.ylabel('Temperatura °C')
plt.title('Variação da temperatura da água e do refrigerante no tempo')
plt.grid(True)
plt.show()

print()
print('A temperatura de equilibrio entre a agua e o refrigerante o gráfico é de aproximadamente {} graus célsius.'.format(min(REFRI)))
print()

########################### Segunda Iteração ############################
########################## água e sal e refri ###########################

def temp_equilibrio():
    Tagua= -20
    Trefri= 20
    crefri= 4.18 #J/g K
    mrefri= 365.75  #g
    calorlatente= -334 #J/g
    crefricongelado= 2.05 #J/g K 
    maguasal= 20*20*25*1.19 # considerando uma caixa de isopor com volume de 0.2m por 0.2m por 0.25m #g
    caguasal= 3.3 #J/g K  
    Tcong= -2.22
    
    parte1= -mrefri*crefri*(Tcong-Trefri) - mrefri * calorlatente + mrefri*crefricongelado*Tcong + maguasal*caguasal*Tagua
    parte2= mrefri*crefricongelado + maguasal*caguasal
    final= parte1/parte2
    return final
    
temp_equilibrio= temp_equilibrio()

def Urefri_e_aguasal(Y, t):

    Trefri= Y[1]
    
    if Trefri < -2.0 and Trefri > -2.25:
       
        def congelamento(Y, t):
            
            Taguasal= Y[0]
            Trefri= Y[1]
            Q=Y[2]
            
            f= 0 #valor para o refri            
            deltaT= Taguasal- Trefri
            Klata= 205 #W/m K
            dlata= 8.5e-5  #m
            hagua= 650    #W/ m^2 K
            Alata= 2*math.pi*3e-2*12.5e-2+ 2*(math.pi*0.03**2)   #considerando o diametro de 6cm e altura de 12.5 cm e a lata como sendo um cilindro #m^2
            maguasal= 20*20*25*1.19 # considerando uma caixa de isopor com volume de 0.2m por 0.2m por 0.25m #g
            caguasal= 3.3 #J/g K    
            calorlatente= 334 #J/g
            mrefri= 365.75  #g
            
            b= 1/(hagua*Alata)
            c= dlata/(Klata*Alata)
            d= b+c
            e= deltaT/d
            
            
            
            g= 1/(maguasal*caguasal)
            h= -g*e    #valor para a agua com sal
           
            
            if Q < calorlatente*mrefri:
                Q= maguasal*caguasal*h
                
            else:
                f= -0.174265
                
            return h, f, Q

        
    else: 
        
        def resto(Y, t):
            Q= Y[2]
            Taguasal= Y[0]
            Trefri= Y[1]
            deltaT= Taguasal- Trefri
            crefri= 4.18 #J/g K
            mrefri= 365.75  #g
            Klata= 205 #W/m K
            dlata= 8.5e-5  #m
            hagua= 650    #W/ m^2 K
            Alata= 2*math.pi*3e-2*12.5e-2+ 2*(math.pi*0.03**2)   #considerando o diametro de 6cm e altura de 12.5 cm e a lata como sendo um cilindro #m^2
            maguasal= 20*20*25*1.19 # considerando uma caixa de isopor com volume de 0.2m por 0.2m por 0.25m #g
            caguasal= 3.3 #J/g K    
            
            a= 1/(mrefri*crefri)
            
            b= 1/(hagua*Alata)
            c= dlata/(Klata*Alata)
            d= b+c
            e= deltaT/d
            
            f= a*e   #valor para o refri
            
            
            g= 1/(maguasal*caguasal)
            h= -g*e    #valor para a agua com sal
    
            return h, f, Q
        
    if Trefri < -2.0 and Trefri > -2.25:
        h, f, Q = congelamento(Y, t)
    else:
        h, f, Q = resto(Y,t)
        
        
    return h, f, Q

Y=[-20,20,0]

delta_t= 3

lista_tempo= np.arange(0, 1000, delta_t)

Solucao= odeint(Urefri_e_aguasal, Y, lista_tempo)

AGUASAL= Solucao[:,0]
REFRI2= Solucao[:,1]

#plt.plot(lista_tempo/60, Solucao)
plt.plot(lista_tempo/60, REFRI2, label='Refrigerante')
plt.plot(lista_tempo/60, AGUASAL, label='Água')
plt.legend()
plt.xlabel('Tempo (minutos)')
plt.ylabel('Temperatura °C')
plt.title('Variação da temperatura da água com sal e do refrigerante no tempo')
plt.grid(True)
plt.show()

print()

print('Na teoria, a temperatura de equilíbrio entre a água com sal e o refrigerante é de {}'.format(temp_equilibrio))

print()

print('No gráfico, o valor de equilibrio para a agua com sal e o refrigerante é de {}, devido a simplificações feitas no código.'.format(min(REFRI2)))

print()

#print(np.interp(477, lista_tempo, REFRI2))
#print(np.interp(65.9999999, lista_tempo, REFRI2))

print('De acordo com este gráfico, o refrigerante chegaria aproximadamente no seu ponto de fusão em cerca de 66 segundos e congela totalmente em perto de 477 segundos. Ou seja, o refrigerante, na teoria, demoraria 411 segundos para congelar.')

########################### Todos junto ###########################

def Urefri_e_agua(Y, t):
    Tagua= Y[0]
    Trefri= Y[1]
    deltaT= Tagua- Trefri
    crefri= 4.18 #J/g K
    mrefri= 365.75  #g
    Klata= 205 #W/m K
    dlata= 8.5e-5  #m
    hagua= 650    #W/ m^2 K
    Alata= 2*math.pi*3e-2*12.5e-2+ 2*(math.pi*0.03**2)   #considerando o diametro de 6cm e altura de 12.5 cm #m^2
    magua= 0.2*0.2*0.25*997*1000 # considerando uma caixa de isopor com volume de 0.2m por 0.2m por 0.25m #g
    cagua= 4.18 #J/g K
    
    
    a= 1/(mrefri*crefri)

    b= 1/(hagua*Alata)
    c= dlata/(Klata*Alata)
    d= b+c
    e= deltaT/d

    f= a*e
    
    g= 1/(magua*cagua)
    h= -g*e
    return h, f

Y=[0,20]

lista_tempo= np.arange(0, 1000, 3)

Solucao= odeint(Urefri_e_agua, Y, lista_tempo)

REFRI= Solucao[:,1]
AGUA= Solucao[:,0]

plt.plot(lista_tempo/60, REFRI2, label='Refrigerante (Agua com sal)')
plt.plot(lista_tempo/60, AGUASAL, label='Água com Sal')
plt.plot(lista_tempo/60, REFRI, label='Refrigerante')
plt.plot(lista_tempo/60, AGUA, label='Água')
plt.legend()
plt.xlabel('Tempo (minutos)')
plt.ylabel('Temperatura °C')
plt.title('Variação da temperatura nos diferentes experimentos')
plt.grid(True)
plt.show()

########################### Todos junto ###########################