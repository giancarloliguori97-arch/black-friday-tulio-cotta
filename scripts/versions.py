"""Gera v2.html, v3.html e v4.html a partir do index.html (v1),
trocando só a copy da primeira dobra. Rodar após qualquer mudança no index.html:
    python3 scripts/versions.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")

VERSIONS = {
    "v2": {
        "h1": 'Seja a profissional mais completa e procurada da sua região, garantindo acesso vitalício à TODAS as formações online de Túlio Cotta <em class="gold">— as que existem e as próximas tendências que estão chegando</em>',
        "sub": None,  # mantém o subtítulo da v1
    },
    "v3": {
        "h1": 'PROFISSIONAL DA BELEZA: <em class="gold">VOCÊ NUNCA MAIS VAI PRECISAR PAGAR PRA APRENDER UMA NOVA TÉCNICA COMIGO</em>',
        "sub": 'Na BlackFriday Infinita, você leva todas as formações atuais e às futuras, com acesso vitalício. Inclusive a <strong>Reconstrução 360º Brows</strong>. E por uma fração do que elas custariam separadas.',
    },
    "v4": {
        "h1": 'Na próxima tendência da beleza, você será a 1ª profissional da sua região a saber fazer, <em class="gold">e vai se tornar referência na cidade</em>',
        "sub": 'Novas técnicas aparecem sempre. Novos procedimentos despertam o desejo das clientes. E as profissionais que aprendem primeiro se tornam referência',
    },
}

for name, v in VERSIONS.items():
    html = SRC
    html, n = re.subn(r"<h1>.*?</h1>", f'<h1 class="h1-{name}">{v["h1"]}</h1>', html, count=1, flags=re.S)
    assert n == 1
    if v["sub"]:
        html, n = re.subn(r'<p class="sub">.*?</p>', f'<p class="sub">{v["sub"]}</p>', html, count=1, flags=re.S)
        assert n == 1
    (ROOT / f"{name}.html").write_text(html, encoding="utf-8")
    print("ok", name)
