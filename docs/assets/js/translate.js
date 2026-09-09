(function() {
    // Create hidden div for Google Translate
    var gtDiv = document.createElement('div');
    gtDiv.id = 'google_translate_element';
    gtDiv.style.display = 'none';
    document.documentElement.appendChild(gtDiv);

    // Global init callback for Google Translate
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            autoDisplay: false,
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE
        }, 'google_translate_element');
        
        // Restore language if previously selected or set in cookie/localStorage
        setTimeout(restoreLanguageState, 500);
    };

    // Inject Google Translate script
    var gtScript = document.createElement('script');
    gtScript.type = 'text/javascript';
    gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.head.appendChild(gtScript);

    // Function to trigger language switch
    window.switchDocLanguage = function(targetLang) {
        var currentLang = localStorage.getItem('doc_selected_lang') || 'en';
        if (targetLang === currentLang && targetLang !== 'en') {
            return; // Already in target language
        }

        if (!targetLang || targetLang === 'en') {
            // Revert to English
            clearTranslateCookie();
            if (currentLang !== 'en') {
                window.location.reload();
            }
        } else {
            // Set cookie and trigger combo for instant in-place translation
            setTranslateCookie(targetLang);
            var combo = document.querySelector('.goog-te-combo');
            if (combo) {
                combo.value = targetLang;
                combo.dispatchEvent(new Event('change'));
            } else {
                // If script is still loading, wait up to 2.5s for combo, otherwise reload
                var attempts = 0;
                var interval = setInterval(function() {
                    combo = document.querySelector('.goog-te-combo');
                    attempts++;
                    if (combo) {
                        clearInterval(interval);
                        combo.value = targetLang;
                        combo.dispatchEvent(new Event('change'));
                    } else if (attempts > 25) {
                        clearInterval(interval);
                        window.location.reload();
                    }
                }, 100);
            }
        }
        updateDropdownUI(targetLang || 'en');
    };

    function setTranslateCookie(lang) {
        var domain = window.location.hostname;
        document.cookie = "googtrans=/en/" + lang + "; path=/; domain=" + domain + ";";
        document.cookie = "googtrans=/en/" + lang + "; path=/;";
        localStorage.setItem('doc_selected_lang', lang);
    }

    function clearTranslateCookie() {
        var domain = window.location.hostname;
        document.cookie = "googtrans=/en/en; path=/; domain=" + domain + "; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
        document.cookie = "googtrans=/en/en; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
        document.cookie = "googtrans=; path=/; domain=" + domain + "; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
        document.cookie = "googtrans=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
        localStorage.setItem('doc_selected_lang', 'en');
    }

    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        if (match) return match[2];
        return null;
    }

    function restoreLanguageState() {
        var savedLang = localStorage.getItem('doc_selected_lang');
        var cookieLang = getCookie('googtrans');
        var currentLang = 'en';
        
        if (cookieLang) {
            var parts = cookieLang.split('/');
            if (parts.length >= 3 && parts[2] && parts[2] !== 'en') {
                currentLang = parts[2];
            }
        } else if (savedLang && savedLang !== 'en') {
            currentLang = savedLang;
            switchDocLanguage(currentLang);
            return;
        }
        
        // If already in target language, make sure combo matches if present
        if (currentLang !== 'en') {
            var combo = document.querySelector('.goog-te-combo');
            if (combo && combo.value !== currentLang) {
                combo.value = currentLang;
                combo.dispatchEvent(new Event('change'));
            }
        }
        updateDropdownUI(currentLang);
    }

    function updateDropdownUI(activeLang) {
        var links = document.querySelectorAll('.md-select__link');
        links.forEach(function(link) {
            var lang = link.getAttribute('hreflang') || 'en';
            if (lang === activeLang || (activeLang === 'en' && lang === 'en')) {
                link.style.fontWeight = 'bold';
                link.style.color = 'var(--md-default-fg-color--light, #3f51b5)';
            } else {
                link.style.fontWeight = 'normal';
                link.style.color = '';
            }
        });
    }

    // Attach event listeners to Material for MkDocs alternate language dropdown
    function attachListeners() {
        var links = document.querySelectorAll('.md-select__link');
        if (links.length === 0) {
            setTimeout(attachListeners, 300);
            return;
        }
        links.forEach(function(link) {
            if (link.getAttribute('data-translate-bound') === 'true') return;
            link.setAttribute('data-translate-bound', 'true');
            
            link.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                var lang = link.getAttribute('hreflang');
                if (!lang) {
                    var href = link.getAttribute('href') || '';
                    if (href.indexOf('#') !== -1) {
                        lang = href.split('#')[1];
                    }
                }
                if (lang) {
                    switchDocLanguage(lang);
                    var activeElement = document.activeElement;
                    if (activeElement && activeElement.blur) activeElement.blur();
                    document.body.click();
                }
            });
        });
        restoreLanguageState();
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', attachListeners);
    } else {
        attachListeners();
    }

    // Hook into Material for MkDocs instant navigation
    if (typeof document$ !== 'undefined' && document$.subscribe) {
        document$.subscribe(function() {
            setTimeout(attachListeners, 200);
            setTimeout(restoreLanguageState, 300);
        });
    } else {
        window.addEventListener('hashchange', function() {
            setTimeout(attachListeners, 200);
        });
    }
})();
