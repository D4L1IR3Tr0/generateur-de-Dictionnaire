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

    def variations_de_casse(chaine):
        """Génère toutes les variations de casse pour la chaîne donnée."""
        def gen_variations(index=0):
            if index == len(chaine):
                yield ""
            else:
                char = chaine[index]
                for suffix in gen_variations(index + 1):
                    if char.isalpha():
                        yield char.lower() + suffix
                        yield char.upper() + suffix
                    else:
                        yield char + suffix

        return gen_variations()

    def appliquer_remplacements(chaine, remplacements):
        """Applique les remplacements de caractères selon les règles données."""
        def gen_remplacements(index=0):
            if index == len(chaine):
                yield ""
            else:
                char = chaine[index]
                if char in remplacements:
                    for remplacement in remplacements[char]:
                        for suffix in gen_remplacements(index + 1):
                            yield remplacement + suffix
                else:
                    for suffix in gen_remplacements(index + 1):
                        yield char + suffix

        return gen_remplacements()

    # Étape 1 : Génération des variations de casse
    variations = variations_de_casse(chaine)

    # Étape 2 : Application des remplacements
    for var in variations:
        for resultat in appliquer_remplacements(var, remplacements):
            yield resultat

def generateur_dictionnaire(mots, remplacements=None, min_length=1, max_length=None, verbose=False):
    if max_length is None:
        max_length = len(mots)

    for longueur in range(min_length, max_length + 1):
        for combinaison in itertools.combinations(mots, longueur):
            for permutation in itertools.permutations(combinaison):
                if verbose:
                    print(f"Permutation: {permutation}")
                combinaisons = itertools.product(*(remplacer_lettres(mot, remplacements) for mot in permutation))
                for resultat in combinaisons:
                    yield ''.join(resultat)

def main():
    parser = argparse.ArgumentParser(
        description="Générateur de dictionnaire de mots de passe.",
        epilog="Exemple d'utilisation: python gen.py nom prénom date-de-naissance -r a=@ o=0 -p 123 -s 2024 -min 8 -max 12 -v"
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
    parser.add_argument(
        '-min', '--min-length', 
        type=int, 
        default=1, 
        help="Longueur minimale des mots de passe."
    )
    parser.add_argument(
        '-max', '--max-length', 
        type=int, 
        help="Longueur maximale des mots de passe."
    )

    args = parser.parse_args()

    remplacements = {r.split('=')[0]: list(r.split('=')[1]) for r in args.remplacements} if args.remplacements else None

    if args.verbose:
        print(f"Remplacements de lettres : {remplacements}")
        print(f"Préfixes : {args.prefixes}")
        print(f"Suffixes : {args.suffixes}")
        print(f"Longueur minimale : {args.min_length}")
        print(f"Longueur maximale : {args.max_length}")
        print("Démarrage de la génération du dictionnaire...")

    with open(args.output, 'w') as fichier:
        total_combinations = 0
        for prefix, mot_de_passe, suffix in itertools.product(args.prefixes, generateur_dictionnaire(args.mots, remplacements=remplacements, min_length=args.min_length, max_length=args.max_length, verbose=args.verbose), args.suffixes):
            fichier.write(prefix + mot_de_passe + suffix + '\n')
            total_combinations += 1

            if args.verbose and total_combinations % 10000 == 0:
                print(f"{total_combinations} mots de passe générés...")

    if args.verbose:
        print(f"Dictionnaire généré et enregistré dans {args.output} avec un total de {total_combinations} mots de passe.")

if __name__ == "__main__":
    main()
