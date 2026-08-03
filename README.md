# Consemnările mele

Carte-cadou îngrijită după manuscrisul lui **Vasia Peiu**.

## Site (GitHub Pages — gratuit)

URL după activare: **https://speiu18.github.io/Hello-world/**

Conținutul site-ului este pe ramura `gh-pages`. Activează hostingul o singură dată:

1. Deschide [Settings → Pages](https://github.com/speiu18/Hello-world/settings/pages)
2. La **Deploy from a branch**, alege branch **`gh-pages`**, folder **`/` (root)**
3. Salvează — în ~1 minut site-ul e live

Alternativ: la **Source** alege **GitHub Actions** (workflow-ul din `.github/workflows/deploy-pages.yml`).

## Deschide cartea local

- **Versiune web:** deschide [`carte/index.html`](carte/index.html) în browser
- **PDF tipărit:** [`carte/Consemnarile-mele.pdf`](carte/Consemnarile-mele.pdf) (format A5)

## Conținut

Text corectat gramatical și structurat pe capitole, cu ilustrații acuarelă inspirate din povești:

1. Unde ești, copilărie?
2. Din maidan
3. Scăldatul pe Culeșa
4. Cânepa
5. La clacă
6. Drumeții la bunicii din Răucești
7. Prin lunca Moldovei

## Regenerare

```bash
python3 build_book.py
# PDF (Chrome headless):
google-chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=carte/Consemnarile-mele.pdf \
  "file://$(pwd)/carte/index.html"
```
