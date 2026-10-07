#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Market Kasa Sırası Yargıtayı.

Üç ürün istisnasını, şerit değişimini ve 'sadece bir şey soracaktım'
savunmasını yargılar. Çıktı Türkçedir. Patates içermez.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys


MADDELER = {
    "3/1": "Üç ürün istisnasının kötüye kullanılması",
    "7/2": "Şerit değiştirip eski sırayı inkâr",
    "9/4": "Kasada fiyat sorma suretiyle rehin",
    "12": "Poşet açmama direnişi",
    "0/0": "Suç yok, sadece yorgunluk",
}


def hukum(urun: int, sira: int, serit: bool, soru: bool, tohum: int | None) -> dict:
    rng = random.Random(tohum if tohum is not None else (urun * 17 + sira * 3 + int(serit)))
    suc = []
    if urun > 3 and sira <= 2:
        suc.append("3/1")
    if serit:
        suc.append("7/2")
    if soru:
        suc.append("9/4")
    if urun >= 15 and not soru:
        suc.append("12")
    if not suc:
        suc.append("0/0")

    agirlik = sum(3 if m != "0/0" else 0 for m in suc) + max(0, urun - 3) + (4 if serit else 0)
    if agirlik == 0:
        karar = "BERAAT"
        gerekce = "Sıra bozulmamış. Market şaşırmış ama mahkeme şaşırmamış."
    elif agirlik < 6:
        karar = "ADLİ PARA: bir sonraki alışverişte poşet ücreti"
        gerekce = "Fiil var, kasıt market ışığında kaybolmuş."
    elif agirlik < 12:
        karar = "ŞERİT MEN: 1 kasa boyu geri"
        gerekce = "Sanık sırayı değil, sıranın hafızasını çiğnemiş."
    else:
        karar = "TEDBİR: express kasa yasağı, normal kuyruk"
        gerekce = "İstisna istisna olmaktan çıkmış, kural olmuş, kural da kızgın."

    muhalefet = rng.choice([
        "Karşı oy: teyze haklıydı.",
        "Karşı oy: fiş çıkmadan hüküm olmaz.",
        "Karşı oy yok, herkes poşetin bitmesini bekliyor.",
        "Karşı oy: üç ürün sayılırken sakız ayrı madde midir?",
    ])
    return {
        "suc": suc,
        "karar": karar,
        "gerekce": gerekce,
        "muhalefet": muhalefet,
        "agirlik": agirlik,
    }


def yaz(sonuc: dict) -> str:
    maddeler = ", ".join(f"{m} ({MADDELER[m]})" for m in sonuc["suc"])
    return (
        "MARKET KASA SIRASI YARGITAYI\n"
        "----------------------------\n"
        f"Suçlar: {maddeler}\n"
        f"Ağırlık: {sonuc['agirlik']}\n"
        f"Hüküm: {sonuc['karar']}\n"
        f"Gerekçe: {sonuc['gerekce']}\n"
        f"Muhalefet şerhi: {sonuc['muhalefet']}\n"
    )


def demo() -> str:
    ornekler = [
        (2, 1, False, False, 1),
        (11, 1, True, True, 8),
        (4, 6, False, True, 3),
        (20, 3, True, False, 12),
    ]
    parcalar = []
    for i, args in enumerate(ornekler, 1):
        parcalar.append(f"Dosya {i}\n" + yaz(hukum(*args)))
    return "\n".join(parcalar)


def parmak_izi(metin: str) -> str:
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Market kasa sırasını yargıla.")
    p.add_argument("--urun", type=int, default=1, help="Sepetteki ürün sayısı")
    p.add_argument("--sira", type=int, default=5, help="Kaçıncı sıradasın")
    p.add_argument("--serit-degistir", action="store_true")
    p.add_argument("--soru-soracaktim", action="store_true")
    p.add_argument("--tohum", type=int, default=None)
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.urun < 0 or a.sira < 1:
        print("Ürün eksi, sıra sıfır olamaz. Market de olmaz.", file=sys.stderr)
        return 2
    metin = demo() if a.demo else yaz(hukum(a.urun, a.sira, a.serit_degistir, a.soru_soracaktim, a.tohum))
    print(metin, end="")
    print(f"Dosya parmak izi: {parmak_izi(metin)}")
    print("Damga: 8 Ekim 2026 | Kayyum Grok | ~~~kasa-fisi-muhuru-041~~~")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
