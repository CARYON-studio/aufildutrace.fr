# ⚠️ FICHIER GENERE par 04_SCRIPTS/build-et-sync.py — NE PAS EDITER.
# La source est 04_SCRIPTS/build/context.py.
# -*- coding: utf-8 -*-

ICO = [
  { 'titre': 'Attention', 'texte': "L’écriture mobilise et soutient la concentration, réduit les distractions.", 'couleur': '#6B705C',
    'd1': 'M28 12.5 C 28.5 21.5 17.5 27 10.5 22 C 4.5 17.7 10 9 16.8 12.4 C 20.3 14.2 19.6 18.2 17 18.8' },
  { 'titre': 'Mémoire', 'texte': "Elle favorise l’encodage, l’organisation et la rétention des informations.", 'couleur': '#6B4548',
    'd1': 'M3.5 24 C 3.5 14 12 8.5 16 14.5 C 19 19 13 22.5 11 18.4 C 8.4 13 17.5 6 22.5 11 C 27 15.6 24.5 22.5 28.5 24' },
  { 'titre': 'Fonctions exécutives', 'texte': 'Elle aide à planifier, organiser et persévérer dans une tâche.', 'couleur': '#3D5A3E',
    'd1': 'M3 26 C 6.5 26 6 20.5 9.5 20.5 C 13 20.5 12.5 15 16 15 C 19.5 15 19 9.5 22.5 9.5 L 28.5 9.5',
    'd2': 'M25.5 6.5 L 28.8 9.6 L 25.5 12.6' },
  { 'titre': 'Créativité', 'texte': "Elle libère les idées et encourage l’imagination.", 'couleur': '#6B4548',
    'd1': 'M4 28 C 10.5 24.5 15.5 19.5 19.8 13.2',
    'd2': 'M20.2 13 c 4.6 -1.3 7.2 -5 7.6 -9.6 c -5.2 0.6 -8.2 4 -7.6 9.6 Z', 'fill': True },
  { 'titre': 'Langage', 'texte': 'Elle enrichit le vocabulaire et la formulation des idées.', 'couleur': '#6B705C',
    'd1': 'M7 21.5 C 2.5 13 8.5 5.5 16.5 5.5 C 24 5.5 29 11 27.3 17.6 C 26 22.4 20.2 24.8 14.8 23.6 L 8.6 27 L 10 21.8',
    'd2': 'M10.5 14.5 c 2 -2.4 3.2 2.4 5.2 0 c 2 -2.4 3.2 2.4 5.2 0' },
  { 'titre': 'Métacognition', 'texte': 'Elle permet de prendre du recul et de mieux se comprendre.', 'couleur': '#6B4548',
    'd1': 'M5.5 21.5 C 3 11.5 12 5.5 19 8.6 C 26.4 11.9 26 22 18.8 24.2 C 14.2 25.6 11 22.5 12.6 19.4',
    'd2': 'M9.4 21.9 L 12.7 19.1 L 15.6 22.2' },
  { 'titre': 'Régulation émotionnelle', 'texte': 'Elle aide à exprimer ses émotions et à retrouver un équilibre intérieur.', 'couleur': '#3D5A3E',
    'd1': 'M2.5 16 c 2.2 -10.5 4.8 10.5 7.2 0 c 2 -8.6 4.2 8.6 6.2 0 c 1.7 -6.4 3.4 6.4 5 0 c 1.3 -4.4 2.7 4.4 4 0 c 1 -2.6 2 2.6 3.6 0' },
  { 'titre': 'Estime de soi', 'texte': "Elle valorise l’expression de soi et renforce la confiance.", 'couleur': '#6B4548',
    'd1': 'M3.5 27.5 C 11 26.5 18.5 20.5 23.5 10.5',
    'd2': 'M24.5 3.5 L 24.5 6.6 M29.6 6.4 L 27.4 8.6 M30 13 L 27 12.6' },
]

ICO_FORM = [
  { 'd1': 'M3.5 9 C 8 6.5 13 7 16 9.6 C 19 7 24 6.5 28.5 9 L 28.5 24 C 24 21.6 19 22.1 16 24.6 C 13 22.1 8 21.6 3.5 24 Z',
    'd2': 'M16 9.6 L 16 24.6' },
  { 'd1': 'M16 16 C 13 11 8.5 10 5.5 12.5 C 2.8 14.8 2.8 17.2 5.5 19.5 C 8.5 22 13 21 16 16 C 19 11 23.5 10 26.5 12.5 C 29.2 14.8 29.2 17.2 26.5 19.5 C 23.5 22 19 21 16 16 Z' },
  { 'd1': 'M9 27.5 L 9 17.2 C 9 14.4 12.2 14 13.2 16 L 13.2 10.4 C 13.2 7.8 16.6 7.8 16.6 10.4 L 16.6 14.4 L 16.6 8.6 C 16.6 6 20 6 20 8.6 L 20 14.4 L 20 10.8 C 20 8.2 23.4 8.2 23.4 10.8 L 23.4 19.4 C 23.4 24.4 20 27.5 16.4 27.5' },
  { 'd1': 'M16 28.5 C 16 21 16 16 16 11.4',
    'd2': 'M15.8 16.4 c -6 -0.6 -8.2 -4.6 -7.6 -9.4 c 5 0 8.2 3.6 7.6 9.4 Z M16.2 13.4 c 6 -0.6 8.2 -4.6 7.6 -9.4 c -5 0 -8.2 3.6 -7.6 9.4 Z', 'fill': True },
]

def _interets():
    out = []
    for o in ICO:
        hasD2 = 'd2' in o
        out.append({
            'titre': o['titre'], 'texte': o['texte'], 'couleur': o['couleur'], 'd1': o['d1'],
            'hasD2': hasD2, 'd2': o.get('d2', ''),
            'd2fill': 'currentColor' if o.get('fill') else 'none',
            'd2stroke': 'none' if o.get('fill') else 'currentColor',
            'd2dash': 'none' if o.get('fill') else '1',
        })
    return out

INTERETS = _interets()

# FAQ regroupée par thème (validé Béatrice 22/08/2026) : les 9 questions
# arrivaient d'un bloc, sans point de repère. Trois familles permettent à un
# parent pressé de trouver sa réponse sans tout lire.
# Réponses passées en FALC : phrases courtes, une idée par phrase, sigles développés.
FAQ_GROUPS = [
  ("Avant de commencer", [
    ("À partir de quel âge peut-on commencer ?",
     "La graphothérapie, c’est la rééducation du geste d’écriture. Elle s’adresse aux enfants dès 6 ou 7 ans, lorsque l’écriture est suffisamment installée pour être évaluée. Elle accompagne aussi les adolescents confrontés à des difficultés persistantes. Les adultes peuvent en bénéficier pour gagner en confort et retrouver une écriture plus fluide au quotidien."),
    ("Comment savoir si une rééducation de l’écriture est utile ?",
     "Plusieurs signes peuvent vous alerter. Une écriture difficile à lire, très lente ou fatigante. Des douleurs à la main, au poignet ou au bras. Un stress ou un découragement dès qu’il faut écrire. Une gêne à l’école, dans les études ou au travail. Un bilan permet d’évaluer les difficultés et de dire si une rééducation est adaptée."),
    ("Est-ce utile pour les adultes ?",
     "Oui. La graphothérapie aide les adultes à gagner en fluidité, en lisibilité et en confort. Par exemple pour reprendre des études, préparer un concours, ou retrouver une écriture fonctionnelle après un accident de la vie. Des progrès sont généralement observés avec une pratique régulière."),
  ]),
  ("Comment se passent les séances", [
    ("En quoi consiste une séance ?",
     "Les séances sont pratiques, progressives et adaptées à chaque personne. Nous travaillons la posture et l’installation, la tenue du stylo et le geste. Puis la fluidité, la lisibilité, et la confiance dans l’acte d’écrire. Les exercices sont variés, et ludiques pour les plus jeunes."),
    ("Quelle est la fréquence idéale des séances ?",
     "Chaque accompagnement est personnalisé : la fréquence s’adapte à l’âge, aux difficultés et aux objectifs. En général, une séance toutes les deux semaines favorise une progression durable."),
    ("Y a-t-il du travail entre les séances ?",
     "Pour les plus jeunes, quelques exercices à la maison peuvent être utiles et efficaces. Pour les plus grands, bien appliquer les conseils donnés en séance tout au long des travaux écrits suffit."),
    ("Combien de séances faut-il prévoir en tout ?",
     "Le besoin varie selon la nature des difficultés, l’âge, la motivation et l’assiduité de la personne. La moyenne se situe autour de 12 à 15 séances. Il est ensuite intéressant de revenir une fois par trimestre ou semestre pour vérifier l’évolution."),
  ]),
  ("Tarifs, remboursement et matériel", [
    ("Y a-t-il une prise en charge de la <abbr title='Caisse Primaire d’Assurance Maladie'>CPAM</abbr> ou des mutuelles ?",
     "Aucune prise en charge n’est prévue par l’Assurance Maladie, comme pour les psychologues ou les ergothérapeutes. Quelques mutuelles indemnisent sur la base d’un forfait annuel de 3 à 6 séances. La MDPH (Maison Départementale des Personnes Handicapées) ne rembourse pas directement. Mais dans certaines situations de handicap reconnu, une participation est parfois possible via la PCH (Prestation de Compensation du Handicap). Renseignez-vous auprès de la MDPH de votre département."),
    ("Faut-il des stylos particuliers pendant et après la rééducation ?",
     "Une rééducation réussie permet à son terme de bien écrire avec n’importe quel stylo. Pour les plus jeunes, certains stylos sont plus adaptés pour éviter une rechute : je vous conseille le cas échéant."),
  ]),
]

PAGES = [
  ('accueil', 'Accueil'), ('presentation', 'Qui suis-je ?'), ('prestations', 'Prestations'),
  ('exercices', 'Exercices'), ('coin', 'Le coin des curieux'), ('faq', 'FAQ'),
]

POUR_QUI_CARDS = [
  { 'tag': 'Chez l’enfant', 'titre': 'Écrire fatigue, fait mal, décourage', 'texte': 'Écriture illisible ou lente, douleurs, stylo mal tenu, cahiers peu soignés, refus face à l’écrit…' },
  { 'tag': 'Au collège, au lycée', 'titre': 'Suivre le rythme devient dur', 'texte': 'Relecture difficile, évaluations non terminées, douleurs sur les textes longs, remarques des professeurs…' },
  { 'tag': 'Chez l’adulte', 'titre': 'Retrouver une écriture efficace', 'texte': 'Se relire difficilement, préparer un concours ou un examen, remarques de l’entourage sur la lisibilité…' },
]

FORMATIONS_RAW = [
  { 'titre': 'Troubles Dys', 'texte': 'Dyslexie, dyspraxie, dysorthographie, dyscalculie, dysphasie. Des troubles qui touchent la lecture, le geste, l’orthographe, le calcul ou le langage.' },
  { 'titre': '<abbr title="Trouble du spectre de l’autisme">TSA</abbr> &amp; <abbr title="Trouble déficitaire de l’attention avec ou sans hyperactivité">TDAH</abbr>', 'texte': 'Troubles du spectre de l’autisme, trouble de l’attention avec ou sans hyperactivité.' },
  { 'titre': 'Handicaps moteurs & polyhandicap', 'texte': 'Déficiences intellectuelles, troubles psychiques, situations de polyhandicap — c’est-à-dire l’association de plusieurs handicaps.' },
  { 'titre': 'Psychologie de l’adolescent', 'texte': 'Formation certifiante, pour mieux accompagner cette période charnière.' },
]

def _formations():
    out = []
    for i, f in enumerate(FORMATIONS_RAW):
        icon = ICO_FORM[i]
        out.append({
            'titre': f['titre'], 'texte': f['texte'],
            'd1': icon['d1'], 'hasD2': 'd2' in icon, 'd2': icon.get('d2',''),
            'd2fill': 'currentColor' if icon.get('fill') else 'none',
            'd2stroke': 'none' if icon.get('fill') else 'currentColor',
            'd2dash': 'none' if icon.get('fill') else '1',
        })
    return out

SIGNES = [
  { 'tag': 'Chez un enfant', 'titre': 'Des signes au quotidien', 'items': ['Son écriture est illisible', 'Il se plaint de douleurs lorsqu’il écrit', 'Il écrit trop lentement', 'Il tient mal son stylo', 'Ses cahiers sont peu soignés', 'Il montre une anxiété, voire un refus, face à l’écrit'] },
  { 'tag': 'Chez un collégien ou lycéen', 'titre': 'L’écrit devient un frein', 'items': ['Il se relit difficilement', 'Il ne termine pas ses évaluations par manque de temps', 'Il a des douleurs lorsqu’il écrit longtemps', 'Il a du mal à prendre les cours en note', 'Ses professeurs font des remarques sur son écriture'] },
  { 'tag': 'Chez un adulte', 'titre': 'Un besoin d’efficacité', 'items': ['Vous vous relisez difficilement', 'Vous préparez un concours ou un examen', 'Votre entourage fait des remarques sur votre écriture'] },
]

TARIFS = [
  { 'prix': '110 €', 'label': 'Bilan graphomoteur', 'detail': 'Entretien et passage des tests (1 h 30 à 2 h). Évaluation à l’échelle d’Ajuriaguerra (un test de référence pour mesurer l’écriture). Compte-rendu écrit envoyé par mail.' },
  { 'prix': '45 €', 'label': 'Séance — enfant / adolescent', 'detail': '45 min + 5-10 min de restitution avec le parent.' },
  { 'prix': '50 €', 'label': 'Séance — adulte', 'detail': '45 min de rééducation de l’écriture.' },
]

EXERCICES = [
  { 'num': '01', 'duree': '10 min', 'titre': 'Je contrôle ma main', 'but': 'bien maîtriser sa main pour écrire.', 'texte': 'Avec un morceau de pâte à modeler : former une petite boule en la faisant tourner entre les doigts, puis un boudin en ouvrant et fermant les doigts. Recommencer 2 fois.', 'pourquoi': 'Ces gestes entraînent le cerveau à mieux contrôler les doigts qui tiennent le crayon.' },
  { 'num': '02', 'duree': '5 min', 'titre': 'Une bonne posture', 'but': 'écrire sans se fatiguer.', 'texte': 'Pieds à plat au sol. Dos droit. Jambes à angle droit. Avant-bras sur le bureau. Cahier légèrement incliné, glissé sous l’avant-bras.', 'pourquoi': 'Une bonne posture aide la main et le corps à mieux écrire, et évite la fatigue.' },
  { 'num': '03', 'duree': '20 min', 'titre': 'Les lettres liées', 'but': 'écrire en cursive sans lever le crayon.', 'texte': 'Tracer des mots comme « tulipe », « tempête », « humilité » en liant les lettres, puis s’entraîner avec de petites phrases amusantes.', 'pourquoi': 'Lever le crayon ralentit l’écriture : les lettres liées la rendent plus fluide et plus rapide.' },
  { 'num': '04', 'duree': '10 min', 'titre': 'Les suites alternées', 'but': 'gagner en rapidité de traitement.', 'texte': 'Chronomètre en main : recopier des suites de lettres puis de chiffres en alternant les couleurs. Variante avec des noms d’animaux ou de fruits.', 'pourquoi': 'Plus on repère l’information vite et précisément, plus on recopie efficacement.' },
]

PHOTO_URL = '/img/beatrice-portrait.jpg'
TELEPHONE = '07 82 11 00 29'
DATE_MAJ = '15 août 2026'

ROUTES = {
    'accueil': '/', 'presentation': '/qui-suis-je/', 'prestations': '/prestations/',
    'exercices': '/exercices/', 'coin': '/le-coin-des-curieux/', 'faq': '/faq/',
    'contact': '/contact/', 'mentions': '/mentions-legales/', 'confidentialite': '/politique-de-confidentialite/',
}

def rel(current_page, target_page):
    """Relative href from current_page's file to target_page's file.
    Points at the literal index.html (not just the folder) so links work
    when double-clicked locally too -- Chrome's file:// handler shows a
    directory listing for a bare folder link instead of loading index.html.
    All routes are depth 0 (accueil, at site root) or depth 1 (everyone else,
    in their own subfolder) -- so this only needs to handle those two cases."""
    target_slug = ROUTES[target_page].strip('/')
    target_file = 'index.html' if target_slug == '' else f'{target_slug}/index.html'
    if current_page == 'accueil':
        return target_file
    else:
        return '../' + target_file

def build_context(page):
    nav_items = []
    for pid, label in PAGES:
        active = (page == pid)
        nav_items.append({
            'label': label, 'go': rel(page, pid), 'color': '#3D5A3E' if active else '#2E3025',
            # WCAG 1.4.11 : le soulignement de la page courante etait a 1,68:1
            # sur creme -- seul repere visuel de "ou suis-je". Passe a --terref (7,11:1).
            'underline': 'var(--terref)' if active else 'transparent',
            # WCAG 2.4.8 : double l'indication visuelle d'une indication programmatique.
            'ariaCurrent': ' aria-current="page"' if active else '',
            'weight': 600 if active else 400,
        })
    faq_groups = []
    n = 0
    for theme, questions in FAQ_GROUPS:
        items = []
        for q, r in questions:
            n += 1
            items.append({
                'question': q, 'reponse': r,
                # WCAG 4.1.2 : chaque bouton pointe vers son panneau par aria-controls.
                'panelId': f'faq-panel-{n}',
            })
        faq_groups.append({'theme': theme, 'items': items})

    prix = True
    ctx = {
        'showAccueil': page == 'accueil', 'showPresentation': page == 'presentation',
        'showPrestations': page == 'prestations', 'showExercices': page == 'exercices',
        'showCoin': page == 'coin', 'showFaq': page == 'faq', 'showContact': page == 'contact',
        'showMentions': page == 'mentions', 'showConfidentialite': page == 'confidentialite',
        'goAccueil': rel(page, 'accueil'), 'goPresentation': rel(page, 'presentation'),
        'goPrestations': rel(page, 'prestations'), 'goExercices': rel(page, 'exercices'),
        'goFaq': rel(page, 'faq'), 'goContact': rel(page, 'contact'), 'goCoin': rel(page, 'coin'),
        'goMentions': rel(page, 'mentions'), 'goConfidentialite': rel(page, 'confidentialite'),
        'navItems': nav_items, 'faqGroups': faq_groups,
        'heroA': True, 'heroB': False, 'heroC': False,
        'signature': True, 'sigStyle': 'animation:traceFrom 2.4s linear .6s both',
        'ctaHero': 'Posez-moi une question', 'ctaBilan': 'Poser une question sur le bilan',
        'hasPhoto': True, 'noPhoto': False, 'photoUrl': PHOTO_URL,
        'photoBg': f"width:100%;height:100%;background-image:url('{PHOTO_URL}');background-size:cover;background-position:50% 28%",
        'photoBgCenter': f"width:100%;height:100%;background-image:url('{PHOTO_URL}');background-size:cover;background-position:50% 50%",
        'photoSrc': PHOTO_URL,
        'telephone': TELEPHONE, 'telHref': 'tel:' + TELEPHONE.replace(' ', ''),
        'dateMaj': DATE_MAJ,
        'prixBilanSuffixe': ' · 110 €' if prix else '',
        'prixSeanceSuffixe': ' · dès 45 €' if prix else '',
        'showAtelier': True,
        'showStickyCta': False,
        'formSent': False, 'formNotSent': True,
        'prenomValue': '', 'emailValue': '', 'telValue': '', 'messageValue': '',
        'prenomHasError': False, 'emailHasError': False, 'messageHasError': False,
        'prenomError': '', 'emailError': '', 'messageError': '',
        'prenomBorder': 'var(--kaki)', 'emailBorder': 'var(--kaki)', 'messageBorder': 'var(--kaki)',
        'pourQuiCards': POUR_QUI_CARDS,
        'formations': _formations(),
        'interetsEcriture': INTERETS,
        'signes': SIGNES,
        'tarifs': TARIFS,
        'exercices': EXERCICES,
    }
    return ctx
