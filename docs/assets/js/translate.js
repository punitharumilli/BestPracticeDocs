// Language menu (English / Deutsch).
//
// "Deutsch" shows the current page machine-translated by Google Translate. Nothing from Google is
// loaded into this site: the translated page opens on Google's translation address
// (…translate.goog), and only after a reader picks Deutsch. "English" returns to the original page.
// No cookie and no browser storage are used.
(function () {
    var PROXY = '.translate.goog';

    function isTranslated() {
        var h = window.location.hostname;
        return h.length > PROXY.length && h.slice(-PROXY.length) === PROXY;
    }

    // punitharumilli-github-io.translate.goog → punitharumilli.github.io
    // (Google writes the dots of the host as "-", and a "-" of the host as "--").
    function originalUrl() {
        var label = window.location.hostname.slice(0, -PROXY.length);
        var host = label.split('--').map(function (part) { return part.replace(/-/g, '.'); }).join('-');
        var params = new URLSearchParams(window.location.search);
        Array.from(params.keys()).forEach(function (k) { if (k.indexOf('_x_tr_') === 0) params.delete(k); });
        var query = params.toString();
        return 'https://' + host + window.location.pathname + (query ? '?' + query : '') + window.location.hash;
    }

    function switchTo(lang) {
        if (lang === 'de' && !isTranslated()) {
            window.location.href = 'https://translate.google.com/translate?sl=en&tl=de&hl=de&u=' + encodeURIComponent(window.location.href);
        } else if (lang === 'en' && isTranslated()) {
            window.location.href = originalUrl();
        }
    }

    function langOf(link) {
        var lang = link.getAttribute('hreflang');
        if (!lang) {
            var href = link.getAttribute('href') || '';
            lang = href.indexOf('#') !== -1 ? href.split('#')[1] : '';
        }
        return lang;
    }

    // Marks the language that is shown, and says where "Deutsch" leads.
    function updateMenu() {
        var active = isTranslated() ? 'de' : 'en';
        document.querySelectorAll('.md-select__link').forEach(function (link) {
            var lang = langOf(link);
            if (lang === 'de') link.title = 'Machine translation by Google Translate (opens the page on translate.goog)';
            link.style.fontWeight = lang === active ? 'bold' : 'normal';
            if (lang === active) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current');
        });
    }

    // One listener for the whole page, so it also covers the menu after instant navigation.
    document.addEventListener('click', function (e) {
        var link = e.target && e.target.closest ? e.target.closest('.md-select__link') : null;
        if (!link) return;
        var lang = langOf(link);
        if (lang !== 'en' && lang !== 'de') return;
        e.preventDefault();
        e.stopPropagation();
        switchTo(lang);
    }, true);

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', updateMenu);
    else updateMenu();
    if (typeof document$ !== 'undefined' && document$.subscribe) document$.subscribe(updateMenu);
})();
