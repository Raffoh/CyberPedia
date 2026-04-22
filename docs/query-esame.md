# Query SQL richieste

Queste sono le **interrogazioni significative** che CyberPedia deve supportare,
scelte per dimostrare competenze SQL avanzate durante l'orale.

## Categorie di competenze da mostrare

- **JOIN multipli** (Q1, Q3, Q5)
- **GROUP BY + HAVING** (Q3, Q6)
- **Subquery correlate** (Q5, Q8)
- **Funzioni aggregate** (Q2, Q7)
- **Auto-join** (Q6 — su `seguito`)
- **LEFT JOIN per ricerca "non associati"** (Q5, Q8)
- **UNION su generalizzazione** (Q9)

---

## Q1 — Top 5 attacchi con più casi reali documentati
```sql
SELECT a.nome, COUNT(c.id_caso) AS n_casi
FROM attacco a
JOIN caso_reale c ON c.id_attacco = a.id_attacco
GROUP BY a.id_attacco, a.nome
ORDER BY n_casi DESC
LIMIT 5;
```

## Q2 — Media CVSS per famiglia di attacco
```sql
SELECT
  CASE
    WHEN ar.id_attacco IS NOT NULL THEN 'Rete'
    WHEN aw.id_attacco IS NOT NULL THEN 'Web'
    WHEN as_.id_attacco IS NOT NULL THEN 'Social'
    WHEN am.id_attacco IS NOT NULL THEN 'Malware'
  END AS famiglia,
  AVG(v.cvss_score) AS media_cvss
FROM attacco a
JOIN sfrutta s ON s.id_attacco = a.id_attacco
JOIN vulnerabilita v ON v.id_vulnerabilita = s.id_vulnerabilita
LEFT JOIN attacco_rete ar ON ar.id_attacco = a.id_attacco
LEFT JOIN attacco_web aw ON aw.id_attacco = a.id_attacco
LEFT JOIN attacco_social as_ ON as_.id_attacco = a.id_attacco
LEFT JOIN attacco_malware am ON am.id_attacco = a.id_attacco
GROUP BY famiglia;
```

## Q3 — Contromisure che mitigano ≥ 3 famiglie di attacco diverse
```sql
SELECT c.nome, COUNT(DISTINCT famiglia) AS famiglie_coperte
FROM contromisura c
JOIN mitiga m ON m.id_contromisura = c.id_contromisura
JOIN (
  SELECT id_attacco, 'rete' AS famiglia FROM attacco_rete
  UNION ALL SELECT id_attacco, 'web' FROM attacco_web
  UNION ALL SELECT id_attacco, 'social' FROM attacco_social
  UNION ALL SELECT id_attacco, 'malware' FROM attacco_malware
) f ON f.id_attacco = m.id_attacco
GROUP BY c.id_contromisura, c.nome
HAVING COUNT(DISTINCT famiglia) >= 3;
```

## Q4 — Utenti con livello ≥ 10 ordinati per n. articoli
```sql
SELECT u.username, u.livello, COUNT(a.id_articolo) AS n_articoli
FROM utenti u
LEFT JOIN articolo a ON a.id_autore = u.id_utente
WHERE u.livello >= 10
GROUP BY u.id_utente, u.username, u.livello
ORDER BY n_articoli DESC;
```

## Q5 — Attacchi web con categoria OWASP A03 mai commentati
```sql
SELECT a.nome
FROM attacco a
JOIN attacco_web aw ON aw.id_attacco = a.id_attacco
WHERE aw.owasp_category = 'A03'
  AND NOT EXISTS (
    SELECT 1 FROM interazione_attacco ia
    JOIN interazione i ON i.id_interazione = ia.id_interazione
    WHERE ia.id_attacco = a.id_attacco AND i.tipo = 'commento'
  );
```

## Q6 — Ricercatori seguiti da ≥ 5 persone
```sql
SELECT u.username, COUNT(s.id_seguace) AS n_follower
FROM utenti u
JOIN seguito s ON s.id_utente_seguito = u.id_utente
GROUP BY u.id_utente, u.username
HAVING COUNT(s.id_seguace) >= 5
ORDER BY n_follower DESC;
```

## Q7 — Danno totale per anno (solo casi > 100M USD)
```sql
SELECT anno, SUM(danno_stimato_usd) AS danno_annuo
FROM caso_reale
WHERE danno_stimato_usd > 100000000
GROUP BY anno
ORDER BY anno DESC;
```

## Q8 — Vulnerabilità recenti senza contromisure
```sql
SELECT v.codice_cve, v.descrizione, v.cvss_score
FROM vulnerabilita v
WHERE v.anno_scoperta >= 2023
  AND NOT EXISTS (
    SELECT 1 FROM sfrutta s
    JOIN mitiga m ON m.id_attacco = s.id_attacco
    WHERE s.id_vulnerabilita = v.id_vulnerabilita
  );
```

## Q9 — Tutte le interazioni di un utente (via UNION)
```sql
SELECT 'attacco' AS target, ia.id_attacco AS id_target, i.data
FROM interazione i JOIN interazione_attacco ia USING (id_interazione)
WHERE i.id_utente = :user_id
UNION ALL
SELECT 'articolo', iart.id_articolo, i.data
FROM interazione i JOIN interazione_articolo iart USING (id_interazione)
WHERE i.id_utente = :user_id
UNION ALL
SELECT 'caso', ic.id_caso, i.data
FROM interazione i JOIN interazione_caso ic USING (id_interazione)
WHERE i.id_utente = :user_id
ORDER BY data DESC;
```

## Q10 — Attacco più "pericoloso" per ogni vittima
```sql
SELECT c.vittima, a.nome, c.danno_stimato_usd
FROM caso_reale c
JOIN attacco a ON a.id_attacco = c.id_attacco
WHERE c.danno_stimato_usd = (
  SELECT MAX(c2.danno_stimato_usd)
  FROM caso_reale c2 WHERE c2.vittima = c.vittima
);
```

## File correlati

- Schema logico → @schema-logico.md
- Modello ER → @er-model.md
