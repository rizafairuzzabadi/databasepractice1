import os, sqlite3, csv

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Creating tables

create_tables_commands = [
    """
        CREATE TABLE IF NOT EXISTS abbrev (
            Type TEXT,
            Code TEXT,
            FullName TEXT
        )""",
    """
        CREATE TABLE IF NOT EXISTS AwardsCoaches (
            CoachId TEXT REFERENCES Coaches (coachID),
            Award TEXT,
            Year INTEGER,
            LgId TEXT,
            Note TEXT
        )""",
    """
        CREATE TABLE IF NOT EXISTS AwardsPlayers (
            awardsPlayersId INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayerId TEXT REFERENCES Master (playerID),
            Award TEXT,
            Year INTEGER,
            LgId TEXT,
            Note TEXT,
            Pos TEXT
        )""",
    """
        CREATE TABLE IF NOT EXISTS Coaches (
            CoachId TEXT REFERENCES Master (coachID),
            Year INTEGER,
            TmId TEXT REFERENCES Teams (TmId),
            LgId TEXT,
            Stint INTEGER,
            notes TEXT,
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            postG INTEGER,
            postW INTEGER,
            postL INTEGER,
            postT INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS CombinedShutouts (
            Year INTEGER,
            Month INTEGER,
            date INTEGER,
            TmId TEXT REFERENCES Teams (year),
            OppId TEXT,
            RP TEXT,
            IDgoalie1 TEXT,
            IDgoalie2 TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Goalies (
            GoaliesID INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayerId TEXT REFERENCES Master (playerID),
            Year INTEGER,
            Stint INTEGER,
            TmId TEXT REFERENCES Teams (TmId),
            LgId TEXT,
            GP INTEGER,
            Min INTEGER,
            W INTEGER,
            L INTEGER, 
            TOL INTEGER,
            ENG INTEGER,
            SHO INTEGER,
            GA INTEGER,
            SA INTEGER,
            POSTGP INTEGER,
            POSTMIN INTEGER,
            POSTW INTEGER,
            POSTL INTEGER,
            POSTT INTEGER,
            POSTENG INTEGER,
            POSTSHO INTEGER,
            POSTGA INTEGER,
            POSTSA INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS GoaliesSC (
            PlayerId TEXT REFERENCES Master (playerID),
            Year INTEGER,
            TmId TEXT REFERENCES Teams (TmId),
            LgId TEXT,
            GP INTEGER,
            Min INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            SHO INTEGER,
            GA INTEGER,
            GoaliesSCId INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS GoaliesShootout (
            PlayerId TEXT REFERENCES Master (playerID),
            Year INTEGER REFERENCES Teams (TmId),
            Stint INTEGER,
            TmId TEXT,
            W INTEGER,
            L INTEGER,
            SA INTEGER,
            GA INTEGER,
            ShootoutID INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS HOF (
            Year INTEGER,
            HOFId TEXT,
            Name TEXT,
            Category TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Master (
            PlayerId TEXT,
            CoachId TEXT REFERENCES Coaches (coachID),
            HOFId TEXT REFERENCES HOF (hofID),
            FirstName TEXT,
            LastName TEXT,
            NameNote TEXT,
            NameGiven TEXT,
            NameNick TEXT,
            Height INTEGER,
            Weight INTEGER,
            ShootCatch TEXT,
            LegendsId TEXT,
            IhdbId TEXT,
            HrefId TEXT,
            FirstNHL INTEGER,
            LastNHL INTEGER,
            FirstWHA INTEGER,
            LastWHA INTEGER,
            Pos TEXT,
            BirthYear INTEGER,
            BirthMon INTEGER,
            BirthDay INTEGER,
            BirthCountry TEXT,
            BirthState TEXT,
            BirthCity TEXT,
            DeathYear INTEGER,
            DeathMon INTEGER,
            DeathDay INTEGER,
            DeathCountry TEXT,
            DeathState TEXT,
            DeathCity TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Scoring (
            scoringId INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayerId TEXT REFERENCES Master (playerID),
            Year INTEGER,
            Stint INTEGER,
            TmId TEXT REFERENCES Teams (TmId),
            LgId TEXT,
            Pos TEXT,
            GP INTEGER,
            G INTEGER CHECK (G >= 0),
            A INTEGER CHECK (A >= 0),
            Pts INTEGER CHECK (Pts >= 0),
            PIM INTEGER,
            PlusMinus INTEGER,
            PPG INTEGER,
            PPA INTEGER,
            SHG INTEGER,
            SHA INTEGER,
            GWG INTEGER,
            GTG INTEGER,
            SOG INTEGER,
            PostGP INTEGER,
            PostG INTEGER,
            PostA INTEGER,
            PostPts INTEGER,
            PostPIM INTEGER,
            PostPlusMinus INTEGER,
            PostPPG INTEGER,
            PostPPA INTEGER,
            PostSHG INTEGER,
            PostSHA INTEGER,
            PostGWG INTEGER,
            PostSOG INTEGER
            )
    """,
    """
        CREATE TABLE IF NOT EXISTS ScoringSC (
            PlayerId TEXT REFERENCES Master (playerID),
            Year INTEGER,
            TmId TEXT REFERENCES Teams (TmId),
            LgId TEXT,
            Pos TEXT,
            GP INTEGER,
            G INTEGER,
            A INTEGER,
            Pts INTEGER,
            PIM INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ScoringShootout (
            PlayerId TEXT REFERENCES Master (playerID),
            Year INTEGER,
            Stint INTEGER,
            TmId TEXT REFERENCES Teams (TmId),
            S INTEGER,
            G INTEGER,
            GDG INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS SeriesPost (
            Year INTEGER,
            Round TEXT,
            Series TEXT,
            TmIdWinner TEXT,
            LgIdWinner TEXT,
            TmIdLoser TEXT,
            LgIdLoser TEXT,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            GoalsWinner INTEGER,
            GoalsLoser INTEGER,
            Note TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Teams (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT,
            FranchId TEXT,
            confID TEXT,
            DivId TEXT,
            Rank INTEGER,
            Playoff TEXT,
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            OTL INTEGER,
            Pts INTEGER,
            SoW INTEGER,
            SoL INTEGER,
            GF INTEGER,
            GA INTEGER,
            Name TEXT,
            PIM INTEGER,
            BenchMinor INTEGER,
            PPG INTEGER,
            PPC INTEGER,
            SHA INTEGER,
            PKG INTEGER,
            PKC INTEGER,
            SHF INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamsHalf (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT REFERENCES Teams (TmId),
            Half INTEGER,
            Rank INTEGER,
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            GF INTEGER,
            GA INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamSplits (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT REFERENCES Teams (TmId),
            HW INTEGER,
            HL INTEGER,
            HT INTEGER,
            HOTL INTEGER,
            RW INTEGER,
            RL INTEGER,
            RT INTEGER,
            ROTL INTEGER,
            SepW INTEGER,
            SepL INTEGER,
            SepT INTEGER,
            SepOL INTEGER,
            OctW INTEGER,
            OctL INTEGER,
            OctT INTEGER,
            OctOL INTEGER,
            NovW INTEGER,
            NovL INTEGER,
            NovT INTEGER,
            NovOL INTEGER,
            DecW INTEGER,
            DecL INTEGER,
            DecT INTEGER,
            DecOL INTEGER,
            JanW INTEGER,
            JanL INTEGER,
            JanT INTEGER,
            JanOL INTEGER,
            FebW INTEGER,
            FebL INTEGER,
            FebT INTEGER,
            FebOL INTEGER,
            MarW INTEGER,
            MarL INTEGER,
            MarT INTEGER,
            MarOL INTEGER,
            AprW INTEGER,
            AprL INTEGER,
            AprT INTEGER,
            AprOL INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamsPost (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT REFERENCES Teams (TmId),
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            GF INTEGER,
            GA INTEGER,
            PIM INTEGER,
            BenchMinor INTEGER,
            PPG INTEGER,
            PPC INTEGER,
            SHA INTEGER,
            PKG INTEGER,
            PKC INTEGER,
            SHF INTEGER
            )
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamsSC (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT REFERENCES Teams (TmId),
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            GF INTEGER,
            GA INTEGER,
            PIM INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamVsTeam (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT REFERENCES Teams (TmId),
            OppId TEXT,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            OTL INTEGER
        )
    """,
]

conn.commit()
for command in create_tables_commands:
    c.execute(command)
csv_files = os.listdir('data')

import pandas as pd
for csv_file in csv_files:

    df = pd.read_csv('data/' + csv_file, on_bad_lines='skip')
    df.to_sql(csv_file[:-4], conn, if_exists='append', index=False)

conn.commit()
conn.close()

