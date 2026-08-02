(function () {
        // Base de données des textes et visuels par marque
        const cardsData = {
          neosurf: {
            badge: "Neosurf",
            title: "Neosurf",
            visual: `<img src="assets/image/neosurf.png" alt="Neosurf" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Vos recharges Neosurf sont contrôlées de manière ultra-sécurisée. Effectuez vos paiements sur le web en toute tranquillité d'esprit sans révéler vos coordonnées bancaires."
          },
          pcs: {
            badge: "PCS Mastercard",
            title: "PCS Mastercard",
            visual: `<img src="assets/image/pcs.png" alt="PCS Mastercard" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Contrôle instantané pour coupons PCS. Assurez-vous du solde et de la validité de votre recharge avant de créditer votre carte prépayée."
          },
          transcash: {
            badge: "Transcash",
            title: "Transcash",
            visual: `<img src="assets/image/transcash.png" alt="Transcash" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Authentification garantie de votre recharge Transcash. Profitez d'un transfert de fond sûr et immédiat sur votre carte de paiement."
          },
          paysafecard: {
            badge: "Paysafecard",
            title: "Paysafecard",
            visual: `<img src="assets/image/paysafecard.png" alt="Paysafecard" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Solution de paiement prépayée leader du marché. Ce vérificateur contrôle la conformité et l'activation de votre ticket d'achat."
          },
          orange: {
            badge: "Recharge Orange",
            title: "Recharge Orange",
            visual: `<img src="assets/image/orange.png" alt="Recharge Orange" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Vérifiez vos crédits téléphoniques et pass Internet Orange. Transaction garantie et validation directe auprès de l'opérateur."
          },
          lycamobile: {
            badge: "Lycamobile",
            title: "Lycamobile",
            visual: `<img src="assets/image/lycamobile.png" alt="Lycamobile" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Contrôlez l'état de votre recharge d'appel nationale ou internationale Lycamobile pour rester connecté en toute sérénité."
          },
          sfr: {
            badge: "Recharge SFR",
            title: "Recharge SFR",
            visual: `<img src="assets/image/sfr.png" alt="Recharge SFR" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Contrôle rapide des codes de recharge SFR La Carte. Assurez-vous que votre coupon est prêt à recharger votre mobile."
          },
          roblox: {
            badge: "Roblox Robux",
            title: "Roblox Robux",
            visual: `<img src="assets/image/roblox.png" alt="Roblox Robux" class="img-fluid" style="max-height: 120px; object-fit: contain">`,
            description: "Vérifiez vos cartes cadeaux Roblox en toute sécurité avant d'ajouter vos Robux ou d'activer votre abonnement Premium."
          }
        };

        const defaultCard = {
          badge: "Sécurité Officielle",
          title: "Vérification de Ticket",
          visual: `<div class="d-flex align-items-center justify-content-center" style="min-height: 140px;"><i class="fa-solid fa-shield-halved fa-5x text-primary"></i></div>`,
          description: "Entrez votre code ou votre e-mail pour vérifier l'authenticité et le statut de votre recharge en toute sécurité."
        };

        const form = document.getElementById('statusForm');
        if (!form) return;

        // Éléments du DOM (Bloc Gauche)
        const cardBadge = document.getElementById('cardBadge');
        const cardTitle = document.getElementById('cardTitle');
        const cardVisual = document.getElementById('cardVisual');
        const cardTrustText = document.getElementById('cardTrustText');

        function updateCardDisplay(type) {
          const data = cardsData[type] || defaultCard;
          cardBadge.textContent = data.badge;
          cardTitle.textContent = data.title;
          cardVisual.innerHTML = data.visual;
          cardTrustText.textContent = data.description;
        }

        updateCardDisplay('default');

        const queryInput = document.getElementById('query');
        const result = document.getElementById('result');
        const btnText = document.getElementById('btnText');
        const btnSpinner = document.getElementById('btnSpinner');
        const btnSearch = document.getElementById('btnSearch');

        function getStatusBadge(statut) {
          const statusLower = (statut || '').toLowerCase();
          if (statusLower.includes('valide') || statusLower.includes('traité') || statusLower.includes('succès')) {
            return `<span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-1">Valide / Traité</span>`;
          } else if (statusLower.includes('attente') || statusLower.includes('encours')) {
            return `<span class="badge bg-warning-subtle text-warning border border-warning-subtle rounded-pill px-3 py-1">En cours</span>`;
          } else if (statusLower.includes('invalide') || statusLower.includes('expiré') || statusLower.includes('rejeté')) {
            return `<span class="badge bg-danger-subtle text-danger border border-danger-subtle rounded-pill px-3 py-1">Invalide</span>`;
          }
          return `<span class="badge bg-secondary-subtle text-secondary border border-secondary-subtle rounded-pill px-3 py-1">${statut}</span>`;
        }

        form.addEventListener('submit', async function (e) {
          e.preventDefault();
          const q = queryInput.value.trim();
          if (!q) return;

          btnText.textContent = "Vérification...";
          btnSpinner.classList.remove('d-none');
          btnSearch.disabled = true;
          result.innerHTML = '';

          try {
            const res = await fetch(`/api/tickets/status?q=${encodeURIComponent(q)}`);

            if (res.ok) {
              const json = await res.json();
              const tickets = Array.isArray(json) ? json : (json?.tickets || []);
              if (tickets.length) {
                let html = '<div class="d-flex flex-column gap-2 mt-2">';

                tickets.forEach(t => {
                  if (t.type_carte) {
                    updateCardDisplay(t.type_carte.toLowerCase());
                  }

                  const dateFormatted = t.created_at ? new Date(t.created_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) : 'N/A';

                  html += `
                    <div class="card border bg-light rounded-3 p-3">
                      <div class="d-flex justify-content-between align-items-center mb-1">
                        <span class="fw-bold text-dark">${t.type_carte}</span>
                        <span class="fw-bold text-primary fs-5">${t.montant} €</span>
                      </div>
                      <div class="d-flex justify-content-between align-items-center mt-2">
                        <small class="text-muted" style="font-size: 0.8rem;">Créé le : ${dateFormatted}</small>
                        ${getStatusBadge(t.statut)}
                      </div>
                    </div>
                  `;
                });

                html += '</div>';
                result.innerHTML = html;
              } else {
                result.innerHTML = `
                  <div class="alert alert-warning border-0 rounded-3 text-center my-2 small">
                    Aucun ticket correspondant trouvé.
                  </div>`;
                updateCardDisplay('default');
              }
            } else {
              result.innerHTML = `
                <div class="alert alert-danger border-0 rounded-3 text-center my-2 small">
                  Erreur serveur lors de la recherche.
                </div>`;
            }
          } catch (err) {
            result.innerHTML = `
              <div class="alert alert-danger border-0 rounded-3 text-center my-2 small">
                Impossible de contacter le serveur.
              </div>`;
          } finally {
            btnText.textContent = "Rechercher le statut";
            btnSpinner.classList.add('d-none');
            btnSearch.disabled = false;
          }
        });
      })();