import os
import itertools

def demander_date(prompt):
    """Force l'utilisateur à entrer une date au format DDMMYYYY ou à laisser vide."""
    while True:
        val = input(prompt).strip()
        if not val:
            return val
        if len(val) == 8 and val.isdigit():
            return val
        print("[-] Erreur : Format invalide. Entrez exactement 8 chiffres sans slashes (ex: 19032007).")

def demander_liste(prompt):
    """Force l'utilisation de virgules et supprime les espaces internes."""
    while True:
        val = input(prompt).strip().lower()
        if not val:
            return []
        
        # Rejette la saisie s'il y a des espaces mais aucune virgule
        if " " in val and "," not in val:
            print("[-] Erreur : S'il y a plusieurs éléments, séparez-les obligatoirement par des virgules (ex: bondy,paris).")
            continue
            
        # Découpe par virgule et supprime tous les espaces de chaque élément
        mots = [mot.replace(" ", "") for mot in val.split(',')]
        return [m for m in mots if m]

def demander_texte(prompt):
    """Supprime automatiquement les espaces pour les champs simples."""
    val = input(prompt).strip().lower()
    return val.replace(" ", "")

def demander_infos():
    """Récupère les informations détaillées de la cible."""
    print("="*50)
    print("      🎯 CUSTOM PASSWORD PROFILER (CUPP-like) 🎯")
    print("="*50)
    print("\n[!] INSTRUCTIONS : Remplissez les informations sur votre cible.")
    print("[!] Laissez vide et appuyez sur ENTRÉE pour ignorer une question.")
    print("[!] Les espaces seront automatiquement supprimés.\n")
    
    infos = {}
    
    infos['prenom'] = demander_texte("> Prénom de la cible : ")
    infos['nom'] = demander_texte("> Nom de la cible : ")
    infos['surnom'] = demander_texte("> Surnom : ")
    infos['ddn'] = demander_date("> Date de naissance (format DDMMYYYY, ex: 19032007) : ")
    
    infos['villes'] = demander_liste("> Ville(s) (format ville1,ville2) : ")
    
    infos['animal'] = demander_texte("> Nom de l'animal de compagnie : ")
    infos['pere'] = demander_texte("> Prénom du père : ")
    infos['mere'] = demander_texte("> Prénom de la mère : ")
    
    infos['partenaire_prenom'] = demander_texte("> Prénom du partenaire : ")
    infos['partenaire_nom'] = demander_texte("> Nom du partenaire : ")
    infos['partenaire_ddn'] = demander_date("> Date de naissance du partenaire (DDMMYYYY) : ")
    
    infos['enfants'] = demander_liste("> Prénoms des enfants (format enfant1,enfant2) : ")
    
    infos['travail'] = demander_texte("> Travail ou entreprise : ")
    infos['telephone'] = demander_texte("> Numéro de téléphone : ")
    
    infos['hobbies'] = demander_liste("> Hobbies (format hobby1,hobby2) : ")

    return infos

def extraire_mots_cles(infos):
    """Extrait tous les mots simples des informations fournies pour la base du dictionnaire."""
    mots_base = []
    
    champs_simples = ['prenom', 'nom', 'surnom', 'animal', 'pere', 'mere', 'partenaire_prenom', 'partenaire_nom', 'travail']
    for champ in champs_simples:
        if infos.get(champ):
            mots_base.append(infos[champ])
            
    if infos['villes']: mots_base.extend(infos['villes'])
    if infos['enfants']: mots_base.extend(infos['enfants'])
    if infos['hobbies']: mots_base.extend(infos['hobbies'])
    
    return [mot for mot in mots_base if mot]

def generer_mutations(infos):
    """Génère le dictionnaire complet en combinant les informations."""
    mots_de_passe = set()
    mots_base = extraire_mots_cles(infos)
    
    annees = []
    if infos['ddn'] and len(infos['ddn']) == 8: annees.append(infos['ddn'][4:])
    if infos['partenaire_ddn'] and len(infos['partenaire_ddn']) == 8: annees.append(infos['partenaire_ddn'][4:])
    annees.extend(['2024', '2025', '2026', '123', '1234'])
    
    caracteres_speciaux = ['!', '?', '@', '*']

    for mot in mots_base:
        mots_de_passe.add(mot.lower())
        mots_de_passe.add(mot.capitalize())
        mots_de_passe.add(mot.upper())

    if infos['ddn']: mots_de_passe.add(infos['ddn'])
    if infos['partenaire_ddn']: mots_de_passe.add(infos['partenaire_ddn'])
    if infos['telephone']: mots_de_passe.add(infos['telephone'])

    mots_actuels = list(mots_de_passe)
    for mot in mots_actuels:
        for annee in annees:
            mots_de_passe.add(f"{mot}{annee}")
            for spec in caracteres_speciaux:
                mots_de_passe.add(f"{mot}{annee}{spec}")
                mots_de_passe.add(f"{mot}{spec}{annee}")

    if infos['prenom'] and infos['nom']:
        mots_de_passe.add(f"{infos['prenom']}{infos['nom']}")
        mots_de_passe.add(f"{infos['prenom'].capitalize()}{infos['nom'].capitalize()}")
        for annee in annees:
            mots_de_passe.add(f"{infos['prenom']}{infos['nom']}{annee}")

    mots_leet = set()
    for mot in mots_de_passe:
        leet = mot.replace('a', '@').replace('e', '3').replace('i', '1').replace('s', '5').replace('o', '0')
        if leet != mot:
            mots_leet.add(leet)
    
    mots_de_passe.update(mots_leet)
    return mots_de_passe

def formatter_taille(taille_octets):
    """Convertit la taille en octets vers un format lisible (Ko, Mo)."""
    if taille_octets < 1024:
        return f"{taille_octets} Octets"
    elif taille_octets < 1024 * 1024:
        return f"{taille_octets / 1024:.2f} Ko"
    else:
        return f"{taille_octets / (1024 * 1024):.2f} Mo"

def sauvegarder_dictionnaire(mots_de_passe, prenom_cible):
    """Sauvegarde le résultat et affiche les statistiques finales."""
    nom_fichier = f"{prenom_cible if prenom_cible else 'unknown'}.txt"
    
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        for mdp in sorted(mots_de_passe):
            f.write(mdp + '\n')
            
    taille_fichier = os.path.getsize(nom_fichier)
    taille_formatee = formatter_taille(taille_fichier)
    
    print("\n" + "="*50)
    print("✅ PROFILAGE TERMINÉ ✅")
    print("="*50)
    print(f"[*] Fichier généré       : {nom_fichier}")
    print(f"[*] Mots de passe créés  : {len(mots_de_passe):,} (uniques)".replace(',', ' '))
    print(f"[*] Taille du fichier    : {taille_formatee}")
    print("="*50 + "\n")

if __name__ == "__main__":
    infos_cibles = demander_infos()
    
    if any(infos_cibles.values()):
        print("\n[*] Analyse des informations et génération des combinaisons en cours...")
        dictionnaire = generer_mutations(infos_cibles)
        sauvegarder_dictionnaire(dictionnaire, infos_cibles['prenom'])
    else:
        print("\n[-] Aucune information n'a été saisie, le programme s'arrête.")