# new file for the contact energies ande the relation between them 



# e=epiblast, p=PrE, m=medium, w= wall 

# define 3 times (for Epi_1, epi_2 etc): J_ee, J_ep, J_pp, J_me, J_mp, J_we, J_wp

###### warm-up cells & warm-up cells
# in fase 1 en 2 maak ik alle J's gelijk, niet alle gammas. Want ik wil dat de blob cellen een blob blijft en dus dat de surface tension tussen ep lager is dan tussen ee en pp. 
# als ik J_ee, J_pp en J_ep gelijk maak, dan is gamma_ep > 0 en voor J=10, zijn gamma_ee en gamma_pp 5. Lijkt me prima. Ook J_me en J_mp worden dan gelijk aan J_ep, J_ee en J_pp dus dat klopt. 

adhesion_difference = 1
neutral = 0

if adhesion_difference: 
    if {{run}} == 1 or {{run}} == 6 or {{run}} == 11 or {{run}} == 16 or {{run}} == 21: 
       gamma_ep_3 = 0.3
       J3_ee = 10
       J3_pp = 11
    elif {{run}} == 2 or {{run}} == 7 or {{run}} == 12 or {{run}} == 17 or {{run}} == 22:
       gamma_ep_3 = 3
       J3_ee = 9
       J3_pp = 12
    elif {{run}} == 3 or {{run}} == 8 or {{run}} == 13 or {{run}} == 18 or {{run}} == 23:
       gamma_ep_3 = 30
       J3_ee = 2
       J3_pp = 15
    elif {{run}} == 4 or {{run}} == 9 or {{run}} == 14 or {{run}} == 19 or {{run}} == 24:
       gamma_ep_3 = 50
       J3_ee = 1.8
       J3_pp = 17
    elif {{run}} == 5 or {{run}} == 10 or {{run}} == 15 or {{run}} == 20 or {{run}} == 25:
       gamma_ep_3 = 300
       J3_ee = 1.2
       J3_pp = 19

    J3_ep = gamma_ep_3 + (J3_ee+J3_pp)/2   # gamma_ep_3 = J3_ep - (J3_ee+J3_pp)/2

    # In a neutral system J_cell_cell = 2* J_cell_medium
    # I use J_ee = J_em to make sure that the cells stay in a blob. 
    # Say that gamma_em = gamma_pm. Derive Jmp from that. (could've also done it other way around)

    vary = 'J_pp'

    #gamma_me_3 = J3_me - J3_ee/2 = gamma_mp_3 = J3_mp - J3_pp/2
    if vary == 'J_ee': 
        J3_me = J3_ee
        J3_mp = J3_me + 0.5*(J3_pp - J3_ee) #with J_me = J_ee, this is the same as 0.5*(J_ee+J_pp)
    elif vary == 'J_pp': 
        J3_mp = 20*J3_pp
        J3_me = J3_mp + 0.5*(J3_ee - J3_pp)

    #For now, set the interaction with the wall equal to interaction with the medium. 
    #Later: make interaction with wall lower since the cells stick to the well in the experiment.
    J3_we = 0.5*J3_me
    J3_wp = 0.5*J3_mp

    gamma_me_3 = J3_me - J3_ee/2
    gamma_mp_3 = J3_mp - J3_pp/2 

elif neutral: 
    J3_ee = 10
    J3_pp = 10
    J3_ep = 10 
    
    J3_me = J3_ee
    J3_mp = J3_pp
    
    J3_we = 0.5*J3_me
    J3_wp = 0.5*J3_mp