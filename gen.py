import itertools
import argparse
from tqdm import tqdm

def remplacer_lettres(chaine, remplacements=None):
    if remplacements is None:
        remplacements = {
            'a': ['a', '@'],
            'o': ['o', '0'],
            'e': ['e', '3'],
            'i': ['i', '1'],
            's': ['s', '$']
        }
    
    resultats = ['']
    for char in chaine:
        if char in remplacements:
            temp = []
            for prefix in resultats:
                for remplacement in remplacements[char]:
                    temp.append(prefix + remplacement)
            resultats = temp
        else:
            resultats = [prefix + char for prefix in resultats]
    
    return resultats

def generateur_dictionnaire(mots, remplacements=None, verbose=False):
    # Générer toutes les combinaisons possibles de mots (de 1 à N mots)
    total_combinations = 0
    for longueur in range(1, len(mots) + 1):
        total_combinations += sum(1 for _ in itertools.combinations(mots, longueur))
    
    if verbose:
        print(f"Génération de {total_combinations} combinaisons de mots")

    for longueur in range(1, len(mots) + 1):
        for combinaison in itertools.combinations(mots, longueur):
            # Pour chaque combinaison, générer toutes les permutations possibles
            for permutation in itertools.permutations(combinaison):
                combinaisons = itertools.product(*[remplacer_lettres(mot, remplacements) for mot in permutation])
                for resultat in combinaisons:
                    yield ''.join(resultat)

def main():
    parser = argparse.ArgumentParser(
        description="Générateur de dictionnaire de mots de passe.",
        epilog="Exemple d'utilisation: python gen.py nom prénom date-de-naissance -r a=@ o=0 -p 123 -s 2024"
    )
    
    parser.add_argument(
        'mots', 
        nargs='+', 
        help="Liste des mots-clés pour générer les combinaisons."
    )
    parser.add_argument(
        '-o', '--output', 
        default='dictionnaire.txt', 
        help="Nom du fichier de sortie où les mots de passe seront enregistrés."
    )
    parser.add_argument(
        '-r', '--remplacements', 
        nargs='+', 
        help="Remplacements de caractères sous forme clé=valeur (ex: a=@ o=0)."
    )
    parser.add_argument(
        '-p', '--prefixes', 
        nargs='*', 
        default=[''], 
        help="Liste de préfixes à ajouter à chaque mot de passe."
    )
    parser.add_argument(
        '-s', '--suffixes', 
        nargs='*', 
        default=[''], 
        help="Liste de suffixes à ajouter à chaque mot de passe."
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help="Afficher plus d'informations pendant l'exécution."
    )

    args = parser.parse_args()

    remplacements = {r.split('=')[0]: list(r.split('=')[1]) for r in args.remplacements} if args.remplacements else None

    if args.verbose:
        print(f"Remplacements de lettres : {remplacements}")
        print(f"Préfixes : {args.prefixes}")
        print(f"Suffixes : {args.suffixes}")
        print("Démarrage de la génération du dictionnaire...")

    total_combinations = sum(1 for _ in itertools.product(args.prefixes, generateur_dictionnaire(args.mots, remplacements=remplacements), args.suffixes))

    with open(args.output, 'w') as fichier:
        for prefix, mot_de_passe, suffix in tqdm(itertools.product(args.prefixes, generateur_dictionnaire(args.mots, remplacements=remplacements, verbose=args.verbose), args.suffixes), desc="Génération des mots de passe", total=total_combinations):
            fichier.write(prefix + mot_de_passe + suffix + '\n')

    if args.verbose:
        print(f"Dictionnaire généré et enregistré dans {args.output}")

if __name__ == "__main__":
    main()

