# Worker Cloudflare `aufildutrace-contact`

Copie de référence du code déployé sur Cloudflare (Workers et Pages > aufildutrace-contact).
Ce fichier n'est pas exécuté par GitHub Pages : le déploiement se fait dans le tableau de bord Cloudflare.

Variables du Worker : ALLOWED_ORIGIN, SENDER_EMAIL, SENDER_NAME, TO_EMAIL.
Secrets : BREVO_API_KEY, `Secret` (clé secrète Turnstile du widget « aufildutrace.fr — formulaire contact »).

Anti-spam (16/11/2026) : origine, champ piège, délai minimal 3 s, Turnstile, refus des liens (422).
