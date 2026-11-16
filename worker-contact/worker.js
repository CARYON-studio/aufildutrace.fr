/**
 * Worker Cloudflare — relais formulaire de contact "Au fil du tracé" → Brevo
 *
 * Anti-spam (16/11/2026) :
 *  1. Origine : seules les requêtes venant de aufildutrace.fr sont acceptées.
 *  2. Champ piège (site_web) rempli → faux succès, rien n'est envoyé.
 *  3. Délai : formulaire rempli en moins de 3 s (ou durée absente) → faux succès.
 *  4. Cloudflare Turnstile : jeton vérifié côté serveur (secret « Secret » ou TURNSTILE_SECRET).
 *  5. Liens dans le prénom ou le message → refus 422 avec un message lisible,
 *     pour qu'une vraie personne puisse reformuler.
 */

const ALLOWED_ORIGINS = ['https://aufildutrace.fr', 'https://www.aufildutrace.fr'];
const MIN_DUREE_MS = 3000;

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowedOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : (env.ALLOWED_ORIGIN || 'https://aufildutrace.fr');

    const corsHeaders = {
      'Access-Control-Allow-Origin': allowedOrigin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return json({ error: 'Méthode non autorisée' }, 405, corsHeaders);
    }

    // 1. Origine
    if (!ALLOWED_ORIGINS.includes(origin)) {
      console.log('rejet: origine', origin || '(absente)');
      return json({ error: 'Origine non autorisée.' }, 403, corsHeaders);
    }

    let body;
    try {
      body = await request.json();
    } catch (err) {
      return json({ error: 'JSON invalide' }, 400, corsHeaders);
    }

    const prenom = clean(body.prenom, 80);
    const email = clean(body.email, 200);
    const telephone = clean(body.telephone, 40);
    const message = clean(body.message, 4000);
    const honeypot = clean(body.site_web, 200); // ne devrait jamais être rempli par une personne
    const duree = Number(body.duree);
    const token = clean(body['cf-turnstile-response'], 2048);

    // 2. Champ piège
    if (honeypot) {
      console.log('rejet: champ piège');
      return json({ ok: true }, 200, corsHeaders);
    }

    // 3. Délai minimal
    if (!Number.isFinite(duree) || duree < MIN_DUREE_MS) {
      console.log('rejet: délai', body.duree);
      return json({ ok: true }, 200, corsHeaders);
    }

    if (!prenom || !email || !message) {
      return json({ error: 'Champs manquants (prénom, e-mail et message sont obligatoires).' }, 400, corsHeaders);
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return json({ error: 'E-mail invalide.' }, 400, corsHeaders);
    }

    // 4. Turnstile
    // Le secret a été créé sous le nom « Secret » le 16/11/2026 ;
    // TURNSTILE_SECRET reste accepté si on le renomme plus tard.
    const turnstileSecret = env.TURNSTILE_SECRET || env.Secret;
    if (turnstileSecret) {
      const ok = await verifyTurnstile(token, turnstileSecret, request.headers.get('CF-Connecting-IP'));
      if (!ok) {
        console.log('rejet: turnstile');
        return json({ error: 'Vérification anti-robot échouée.' }, 403, corsHeaders);
      }
    } else {
      console.warn('TURNSTILE_SECRET absent : vérification Turnstile désactivée');
    }

    // 5. Liens
    if (containsLink(prenom) || containsLink(message)) {
      console.log('rejet: lien');
      return json({
        error: 'Pour éviter les messages indésirables, les liens ne sont pas acceptés. Merci de retirer l’adresse du site de votre message.',
      }, 422, corsHeaders);
    }

    const toEmail = env.TO_EMAIL || 'aufildutrace@gmail.com';
    const senderEmail = env.SENDER_EMAIL;
    const senderName = env.SENDER_NAME || 'Au fil du tracé — site web';

    if (!env.BREVO_API_KEY || !senderEmail) {
      return json({ error: 'Configuration serveur incomplète.' }, 500, corsHeaders);
    }

    const htmlContent = `
      <p><strong>Nouvelle question via le site aufildutrace.fr</strong></p>
      <p><strong>Prénom :</strong> ${escapeHtml(prenom)}</p>
      <p><strong>E-mail :</strong> ${escapeHtml(email)}</p>
      <p><strong>Téléphone :</strong> ${escapeHtml(telephone) || '(non renseigné)'}</p>
      <p><strong>Message :</strong><br>${escapeHtml(message).replace(/\n/g, '<br>')}</p>
    `;

    const brevoRes = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'api-key': env.BREVO_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        sender: { name: senderName, email: senderEmail },
        to: [{ email: toEmail, name: 'Béatrice' }],
        replyTo: { email, name: prenom },
        subject: `Nouvelle question — ${prenom} (aufildutrace.fr)`,
        htmlContent,
      }),
    });

    if (!brevoRes.ok) {
      const errText = await brevoRes.text().catch(() => '');
      console.error('Brevo error', brevoRes.status, errText);
      return json({ error: 'Envoi impossible pour le moment.' }, 502, corsHeaders);
    }

    return json({ ok: true }, 200, corsHeaders);
  },
};

async function verifyTurnstile(token, secret, ip) {
  if (!token) return false;
  const form = new FormData();
  form.append('secret', secret);
  form.append('response', token);
  if (ip) form.append('remoteip', ip);
  try {
    const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const data = await res.json();
    if (!data.success) return false;
    if (data.hostname && !/(^|\.)aufildutrace\.fr$/.test(data.hostname)) return false;
    return true;
  } catch (err) {
    console.error('siteverify error', err);
    return false;
  }
}

// Repère un lien : http(s)://, www., ou un nom de domaine avec une extension
// courante chez les spammeurs. Les adresses e-mail sont retirées avant le test,
// et les domaines en .fr sont tolérés (ex. « doctolib.fr »).
function containsLink(str) {
  const sansEmails = String(str).replace(/[^\s@]+@[^\s@]+\.[^\s@]+/g, ' ');
  return /https?:\/\/|www\.|\b[a-z0-9-]{2,}\.(?:com|net|org|online|site|xyz|info|biz|ru|top|shop|store|click|link|io|co|me|live|pro|app|cc|tk|cn|id)\b/i.test(sansEmails);
}

function clean(value, maxLen) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, maxLen);
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function json(obj, status, corsHeaders) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders },
  });
}
