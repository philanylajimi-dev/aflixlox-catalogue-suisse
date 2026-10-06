/**
 * AF Lix Lox — catalogue.
 *
 * Deux comportements, pas un de plus : savoir où l'on se trouve dans la barre
 * de navigation, et laisser les blocs apparaître à l'arrivée. Le catalogue
 * reste intégralement lisible sans JavaScript.
 */

(function () {
  'use strict';

  var reduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Hauteur de la barre collante ---------------------------------- */

  /* Les ancres doivent s'arrêter sous la barre, pas derrière. La barre a deux
     rangées et sa hauteur dépend de la police chargée : on la mesure. */
  var barre = document.querySelector('.h-bar');

  if (barre) {
    var mesurer = function () {
      document.documentElement.style.setProperty(
        '--nav-h', barre.getBoundingClientRect().height + 'px'
      );
    };
    mesurer();
    window.addEventListener('resize', mesurer, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(mesurer);
  }

  /* ---- Section active dans la barre ---------------------------------- */

  var liens = Array.prototype.slice.call(
    document.querySelectorAll('.h-nav a[href^="#"]')
  );

  if (liens.length && 'IntersectionObserver' in window) {
    var parSection = {};
    var cibles = [];

    liens.forEach(function (lien) {
      var section = document.querySelector(lien.getAttribute('href'));
      if (!section) return;
      parSection[section.id] = lien;
      cibles.push(section);
    });

    var visibles = new Set();

    var marquer = function () {
      // Celle qui est le plus haut dans le document parmi les visibles.
      var active = cibles.filter(function (s) { return visibles.has(s.id); })[0];
      liens.forEach(function (l) { l.removeAttribute('aria-current'); });
      if (active && parSection[active.id]) {
        var lien = parSection[active.id];
        lien.setAttribute('aria-current', 'true');
        // On garde la chip active dans le champ de vision sur mobile.
        var piste = lien.parentElement;
        if (piste.scrollWidth > piste.clientWidth) {
          var decalage = lien.offsetLeft - piste.clientWidth / 2 + lien.offsetWidth / 2;
          piste.scrollTo({ left: decalage, behavior: reduit ? 'auto' : 'smooth' });
        }
      }
    };

    var observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (entree.isIntersecting) visibles.add(entree.target.id);
        else visibles.delete(entree.target.id);
      });
      marquer();
    }, { rootMargin: '-25% 0px -60% 0px' });

    cibles.forEach(function (s) { observateur.observe(s); });
  }

  /* ---- Apparition ----------------------------------------------------- */

  if (reduit || !('IntersectionObserver' in window)) return;

  var blocs = document.querySelectorAll(
    '.o-carte, .g-carte, .a-bloc, .r-bloc, .c-groupe, .s-hero__chiffres'
  );

  var apparition = new IntersectionObserver(function (entrees, obs) {
    entrees.forEach(function (entree) {
      if (!entree.isIntersecting) return;
      entree.target.classList.add('is-in');
      obs.unobserve(entree.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });

  blocs.forEach(function (bloc) {
    bloc.classList.add('js-reveal');
    apparition.observe(bloc);
  });
})();
