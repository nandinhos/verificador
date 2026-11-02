#!/usr/bin/env python3
"""Suite de testes do verificador-independente (stdlib unittest, sem dependências).

Testa as funções puras dos scripts de auditoria com entradas de resultado
conhecido. Rodar: python3 tests/test_auditoria.py
"""
import importlib.util
import os
import sys
import unittest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")


def carregar(nome):
    """Importa um script de scripts/ como módulo (sem executar main)."""
    caminho = os.path.join(SCRIPTS, nome)
    spec = importlib.util.spec_from_file_location(nome[:-3], caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = [nome]  # evita argparse rodar com args do teste
    spec.loader.exec_module(mod)
    return mod


e5 = carregar("etapa5_estatistica.py")
ea = carregar("estatistica_avancada.py")
ast = carregar("analise_secoes_turnos.py")


class TestBenjaminiHochberg(unittest.TestCase):
    def test_todos_significativos(self):
        # p-valores todos minúsculos → todos sobrevivem
        self.assertEqual(ea.bh([1e-6] * 100, 0.05), 100)

    def test_nenhum_significativo(self):
        # p-valores todos altos → nenhum sobrevive
        self.assertEqual(ea.bh([0.9] * 100, 0.05), 0)

    def test_fdr_monotonia(self):
        # q maior nunca rejeita menos hipóteses que q menor
        p = [0.001, 0.01, 0.02, 0.2, 0.5, 0.8]
        self.assertGreaterEqual(ea.bh(p, 0.10), ea.bh(p, 0.01))

    def test_caso_classico(self):
        # exemplo controlado: com m=5 e um p muito baixo
        self.assertGreaterEqual(ea.bh([0.001, 0.4, 0.5, 0.6, 0.7], 0.05), 1)


class TestPhiNormal(unittest.TestCase):
    def test_simetria(self):
        self.assertAlmostEqual(ea.phi(1.0), ea.phi(-1.0), places=12)

    def test_valores_conhecidos(self):
        # P(|Z|>1.96) ~ 0.05 bicaudal
        self.assertAlmostEqual(ea.phi(1.96), 0.05, places=2)
        # P(|Z|>0) = 1
        self.assertAlmostEqual(ea.phi(0.0), 1.0, places=6)


class TestDiD(unittest.TestCase):
    def _sec(self, v13, v):
        return {"v": v, "v13": v13}

    def test_did_nulo_sem_efeito(self):
        # painel idêntico em tarde/pontual → DiD = 0
        s1 = {("1", "1", str(i)): {"validos": 100, "v13": 50, "v22": 50, "fech": 1000} for i in range(60)}
        s2 = {k: dict(v) for k, v in s1.items()}
        # metade "tarde", metade "pontual"
        trat = lambda k: int(k[2]) < 30
        r = e5.did(s1, s2, "13", trat)
        self.assertIsNotNone(r)
        self.assertAlmostEqual(r[0], 0.0, places=6)

    def test_did_detecta_efeito(self):
        # tarde ganha +10pp no 2T, pontual estável → DiD = +10
        s1, s2 = {}, {}
        for i in range(60):
            k = ("1", "1", str(i))
            tarde = i < 30
            s1[k] = {"validos": 100, "v13": 50, "v22": 50, "fech": 1200 if tarde else 900}
            v13_2 = 60 if tarde else 50
            s2[k] = {"validos": 100, "v13": v13_2, "v22": 100 - v13_2, "fech": 1200 if tarde else 900}
        trat = lambda k: s2[k]["fech"] > 18 * 60
        r = e5.did(s1, s2, "13", trat)
        self.assertIsNotNone(r)
        self.assertAlmostEqual(r[0], 10.0, places=6)


class TestMadZ(unittest.TestCase):
    def test_mediana_centro(self):
        med, mad, z = ea_madz([1, 2, 3, 4, 5])
        self.assertEqual(med, 3)
        self.assertAlmostEqual(z(3), 0.0)

    def test_outlier_alto_z(self):
        med, mad, z = ea_madz([1, 1, 1, 1, 100])
        self.assertGreater(abs(z(100)), 3)


def ea_madz(vals):
    # usa a implementação do etapa5 (mad_z)
    return ast.mad_z(vals)


class TestIdentidadesContabeis(unittest.TestCase):
    """comparecimento = válidos + brancos + nulos (por seção, dados reais)."""

    def test_identidade_em_bu_real(self):
        import zipfile, io, csv
        raw = "/root/auditoria-raw/bweb_2t_AC.zip"
        if not os.path.exists(raw):
            self.skipTest("BU AC 2T não disponível")
        z = zipfile.ZipFile(raw)
        n = [x for x in z.namelist() if x.endswith(".csv")][0]
        fh = io.TextIOWrapper(z.open(n), encoding="latin-1", newline="")
        sec = {}
        for linha in fh:
            if '"Presidente"' not in linha:
                continue
            c = next(csv.reader([linha], delimiter=";", quotechar='"'))
            if c[17] != "Presidente":
                continue
            k = (c[11], c[13], c[14])
            r = sec.setdefault(k, {"comp": int(c[23] or 0), "nom": 0, "br": 0, "nulo": 0})
            t, v = c[28], int(c[31] or 0)
            if t == "Nominal":
                r["nom"] += v
            elif t == "Branco":
                r["br"] += v
            elif t == "Nulo":
                r["nulo"] += v
        self.assertGreater(len(sec), 1000)
        falhas = [k for k, r in sec.items() if r["nom"] + r["br"] + r["nulo"] != r["comp"]]
        self.assertEqual(falhas, [], f"{len(falhas)} seções violam a identidade contábil")


if __name__ == "__main__":
    unittest.main(verbosity=2)
