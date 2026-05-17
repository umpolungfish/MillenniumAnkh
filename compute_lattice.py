import sys

# Primitive ordinal indices (confirmed from Core.lean)
# D: wedge=0, triangle=1, infty=2, odot=3
# T: network=0, in=1, bowtie=2, box=3, odot=4  
# R: super=0, cat=1, dagger=2, lr=3
# P: asym=0, psi=1, pm=2, sym=3, pm_sym=4
# F: ell=0, eth=1, hbar=2
# K: fast=0, mod=1, slow=2, trap=3, MBL=4
# G: beth=0, gimel=1, aleph=2
# Gamma: and=0, or=1, seq=2, broad=3
# Phi: sub=0, c=1, c_complex=2, EP=3, super=4
# H: H0=0, H1=1, H2=2, Hinf=3
# S: 1:1=0, n:n=1, n:m=2
# Omega: 0=0, Z2=1, Z=2, NA=3

Dn = ['Ð_;','Ð_C','Ð_ß','Ð_ω']
Tn = ['Þ_6','Þ_K','Þ_ò','Þ_¨','Þ_O']
Rn = ['Ř_¯','Ř_ý','Ř_Ť','Ř_=']
Pn = ['Φ_ɐ','Φ_υ','Φ_F','Φ_˙','Φ_}']
Fn = ['ƒ_ì','ƒ_ð','ƒ_ż']
Kn = ['Ç_-','Ç_W','Ç_@','Ç_Ù','Ç_λ']
Gn = ['Γ_β','Γ_γ','Γ_ʔ']
Gramn = ['ɢ_^','ɢ_˝','ɢ_ˌ','ɢ_Ş']
Phin = ['φ̂_ž','φ̂_ÿ','φ̂_Æ','φ̂_3','φ̂_Ţ']
Hn = ['Ħ_Ñ','Ħ_£','Ħ_A','Ħ_!']
Sn = ['Σ_S','Σ_ő','Σ_ï']
Omg = ['Ω_Å','Ω_2','Ω_z','Ω_5']

def fmt(t):
    return f'⟨{Dn[t[0]]}; {Tn[t[1]]}; {Rn[t[2]]}; {Pn[t[3]]}; {Fn[t[4]]}; {Kn[t[5]]}; {Gn[t[6]]}; {Gramn[t[7]]}; {Phin[t[8]]}; {Hn[t[9]]}; {Sn[t[10]]}; {Omg[t[11]]}⟩'

# meet = min
def meet(a,b): return tuple(min(a[i],b[i]) for i in range(12))
# tensor: max except P,F=min
def tensor(a,b):
    return tuple(min(a[i],b[i]) if i in [3,4] else max(a[i],b[i]) for i in range(12))
def mismatches(a,b): return sum(1 for i in range(12) if a[i]!=b[i])

# Encodings
mani  = (3,3,3,3,2,2,2,0,2,2,2,2)  # manifold: D_odot,T_box,R_lr,P_sym,F_hbar,K_slow,G_aleph,Gamma_and,Phi_c_complex,H2,n_m,Omega_Z
sc    = (3,4,2,3,2,2,2,2,1,3,2,2)  # sheaf cohomology: D_odot,T_odot,R_dagger,P_sym,F_hbar,K_slow,G_aleph,Gamma_seq,Phi_c,Hinf,n_m,Omega_Z
pic   = (3,4,3,2,2,2,2,0,2,2,2,2)  # picard: D_odot,T_odot,R_lr,P_pm,F_hbar,K_slow,G_aleph,Gamma_and,Phi_c_complex,H2,n_m,Omega_Z
intc  = (3,4,3,2,0,2,2,0,2,2,2,2)  # int coh: D_odot,T_odot,R_lr,P_pm,F_ell,K_slow,G_aleph,Gamma_and,Phi_c_complex,H2,n_m,Omega_Z
hol   = (3,4,3,3,2,2,2,0,0,2,2,0)  # hol coh: D_odot,T_odot,R_lr,P_sym,F_hbar,K_slow,G_aleph,Gamma_and,Phi_sub,H2,n_m,Omega_0
expseq= (3,2,2,3,2,2,2,2,1,3,2,2)  # exp sequence: D_odot,T_bowtie,R_dagger,P_sym,F_hbar,K_slow,G_aleph,Gamma_seq,Phi_c,Hinf,n_m,Omega_Z
longex= (3,4,2,3,2,2,2,2,1,3,2,2)  # long exact: D_odot,T_odot,R_dagger,P_sym,F_hbar,K_slow,G_aleph,Gamma_seq,Phi_c,Hinf,n_m,Omega_Z
hodged= (3,3,3,3,2,2,2,0,1,2,1,2)  # hodge decomp: D_odot,T_box,R_lr,P_sym,F_hbar,K_slow,G_aleph,Gamma_and,Phi_c,H2,n_n,Omega_Z
dolb  = (3,2,3,3,2,2,2,0,1,2,2,2)  # dolbeault: D_odot,T_bowtie,R_lr,P_sym,F_hbar,K_slow,G_aleph,Gamma_and,Phi_c,H2,n_m,Omega_Z
chern = (3,4,2,2,0,2,2,2,1,2,2,2)  # chern class: D_odot,T_odot,R_dagger,P_pm,F_ell,K_slow,G_aleph,Gamma_seq,Phi_c,H2,n_m,Omega_Z
int11 = (3,2,3,2,0,2,2,0,1,2,2,2)  # integral11: D_odot,T_bowtie,R_lr,P_pm,F_ell,K_slow,G_aleph,Gamma_and,Phi_c,H2,n_m,Omega_Z
i2c   = (3,1,0,0,0,0,2,0,0,0,2,0)  # int_to_complex: D_odot,T_in,R_super,P_asym,F_ell,K_fast,G_aleph,Gamma_and,Phi_sub,H0,n_m,Omega_0
hproj = (3,1,0,0,2,2,2,0,0,0,2,0)  # hodge_proj: D_odot,T_in,R_super,P_asym,F_hbar,K_slow,G_aleph,Gamma_and,Phi_sub,H0,n_m,Omega_0

print("=== MEET COMPUTATIONS ===")
print(f"meet(sc,pic) = {fmt(meet(sc,pic))}")
print(f"  crit: {Phin[meet(sc,pic)[8]]}, gram: {Gramn[meet(sc,pic)[7]]}, prot: {Omg[meet(sc,pic)[11]]}")
print()
print(f"meet(intc,hol) = {fmt(meet(intc,hol))}")
print(f"  crit: {Phin[meet(intc,hol)[8]]}, rel: {Rn[meet(intc,hol)[2]]}")
print()
print(f"meet(hodged,int11) = {fmt(meet(hodged,int11))}")
print(f"  top: {Tn[meet(hodged,int11)[1]]}")
print()
print(f"meet(int11,dolb) = {fmt(meet(int11,dolb))}")
print(f"  crit: {Phin[meet(int11,dolb)[8]]}")
print(f"meet(int11,hol) = {fmt(meet(int11,hol))}")
print(f"  crit: {Phin[meet(int11,hol)[8]]}")
print()

print("=== TENSOR COMPUTATIONS ===")
print(f"tensor(pic,expseq) = {fmt(tensor(pic,expseq))}")
print(f"  rel: {Rn[tensor(pic,expseq)[2]]}, prot: {Omg[tensor(pic,expseq)[11]]}")
print()
print(f"tensor(pic,longex) = {fmt(tensor(pic,longex))}")
print(f"  prot: {Omg[tensor(pic,longex)[11]]}")
print(f"meet(intc,hol).prot: {Omg[meet(intc,hol)[11]]}")
print()
print(f"tensor(pic,chern) = {fmt(tensor(pic,chern))}")
print(f"  prot: {Omg[tensor(pic,chern)[11]]}, crit: {Phin[tensor(pic,chern)[8]]}, gran: {Gn[tensor(pic,chern)[6]]}")
print(f"int11.prot: {Omg[int11[11]]}, int11.crit: {Phin[int11[8]]}, int11.gran: {Gn[int11[6]]}")
print()
print(f"tensor(hproj,hodged) = {fmt(tensor(hproj,hodged))}")
print(f"  top: {Tn[tensor(hproj,hodged)[1]]}")
print()

print("=== DISTANCE COMPUTATIONS ===")
print(f"mismatches(pic,intc) = {mismatches(pic,intc)}")
print(f"mismatches(dolb,sc) = {mismatches(dolb,sc)}")
print()
print(f"meet(intc,dolb) = {fmt(meet(intc,dolb))}")
print(f"  crit: {Phin[meet(intc,dolb)[8]]}")
print(f"meet(intc,hol) = {fmt(meet(intc,hol))}")
print(f"  crit: {Phin[meet(intc,hol)[8]]}")
print()

# Key: what is the ACTUAL truth?
print("=== TRUTH VALUES ===")
# mismatches(pic,intc): pic=P_pm, intc=P_pm, differ only in F: pic=hbar, intc=ell → 1
print(f"mismatches(pic,intc) == 1: {mismatches(pic,intc) == 1}")
# mismatches(dolb,sc): dolb=(3,2,3,3,2,2,2,0,1,2,2,2), sc=(3,4,2,3,2,2,2,2,1,3,2,2)
# diffs: T(bowtie2≠odot4), R(lr3≠dagger2), Gamma(and0≠seq2), H(H2≠Hinf3) → 4
print(f"mismatches(dolb,sc) == 4: {mismatches(dolb,sc) == 4}")
