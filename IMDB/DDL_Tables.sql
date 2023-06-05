/* TABLE CREATION */

CREATE TABLE IF NOT EXISTS us_congress (
    bioguide_id text CONSTRAINT p_key_uscongress PRIMARY KEY,
    date_added date DEFAULT CURRENT_DATE NOT NULL,
    last_updated timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_name text NOT NULL,
    first_name text NOT NULL,
    middle_name text,
    suffix text,
    nickname text,
    full_name text NOT NULL,
    birthday date NOT NULL,
    gender text,
    type text NOT NULL,
    state text NOT NULL,
    district integer,
    senate_class integer,
    party text NOT NULL,
    url text,
    address text,
    phone text,
    fax_number text,
    fax_zero_url text,
    contact_form text,
    rss_url text UNIQUE,
    twitter text UNIQUE,
    twitter_id bigint UNIQUE,
    facebook text UNIQUE,
    youtube text UNIQUE,
    youtube_id text UNIQUE,
    mastodon text UNIQUE,
    thomas_id integer UNIQUE,
    opensecrets_id text UNIQUE,
    lis_id text UNIQUE,
    fec_ids text UNIQUE,
    cspan_id integer UNIQUE,
    govtrack_id integer UNIQUE,
    votesmart_id integer UNIQUE,
    ballotpedia_id text UNIQUE,
    washington_post_id text UNIQUE,
    icpsr_id integer UNIQUE,
    wikipedia_id text UNIQUE
    );

CREATE TABLE IF NOT EXISTS letter_part (
    part_id uuid CONSTRAINT pkey_letterpart  PRIMARY KEY DEFAULT gen_random_uuid (),
    part_placement text NOT NULL,
    subject text NOT NULL,
    recipient_sentiment int NOT NULL,
    government_level text NOT NULL,
    chamber text,
    geography text NOT NULL,
    bill_referenced text,
    part_text text NOT NULL
);

CREATE TABLE IF NOT EXISTS representative_sentiment (
    full_name text,
    state text,
    subject text,
    sentiment int NOT NULL,
    bioguide_id text,
    CONSTRAINT pkey_representativesentiment PRIMARY KEY (full_name,state,subject)
);

CREATE TABLE IF NOT EXISTS sentiment_level (
    level int CONSTRAINT pkey_sentimentlevel PRIMARY KEY,
    description text
);

CREATE TABLE IF NOT EXISTS federal_sponsor (
    bill text,
    sponsor_bioguide_id text,
    CONSTRAINT pkey_federalsponsor PRIMARY KEY (bill,sponsor_bioguide_id)
);

CREATE TABLE IF NOT EXISTS state_sponsor (
    state text,
    bill text,
    sponsor_name text,
    CONSTRAINT pkey_statesponsor PRIMARY KEY (state,bill,sponsor_name)
);

/* FOREIGN KEY CREATION */

ALTER TABLE letter_part
    ADD CONSTRAINT fkey_letterpart_sentimentlevel FOREIGN KEY(recipient_sentiment) REFERENCES sentiment_level(level)
;

ALTER TABLE representative_sentiment 
    ADD CONSTRAINT fkey_representativesentiment_uscongress FOREIGN KEY(bioguide_id) REFERENCES us_congress(bioguide_id),
    ADD CONSTRAINT fkey_representativesentiment_sentimentlevel FOREIGN KEY(sentiment) REFERENCES sentiment_level(level)
;	
