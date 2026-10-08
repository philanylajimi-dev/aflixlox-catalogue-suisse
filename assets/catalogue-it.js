/**
 * AF Lix Lox — Svizzera Italiana.
 *
 * catalogue.js tient déjà la barre collante et la section active ; ses
 * sélecteurs d'apparition visent les blocs du catalogue français, qui n'existent
 * pas ici. Ce complément se contente donc de faire apparaître les blocs
 * italiens, avec exactement la même courbe et le même respect de
 * `prefers-reduced-motion`.
 */

(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  var blocs = document.querySelectorAll('.i-tessera, .i-banda, .i-carta, .i-gamma');
  if (!blocs.length) return;

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
