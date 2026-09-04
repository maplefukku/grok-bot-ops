CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE intent_atom (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    kind text NOT NULL,
    source text NOT NULL,
    tags text[] NOT NULL DEFAULT '{}',
    body text NOT NULL,
    related_ids uuid[] NOT NULL DEFAULT '{}',
    embedding vector(1536),
    actor text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    expires_at timestamptz,
    CONSTRAINT intent_atom_kind CHECK (
        kind IN (
            'intent',
            'decision',
            'belief',
            'feeling',
            'critique_human',
            'critique_bot'
        )
    ),
    CONSTRAINT intent_atom_source CHECK (source IN ('human', 'bot')),
    CONSTRAINT intent_atom_pairing CHECK (
        (kind = 'critique_bot') = (source = 'bot')
    ),
    CONSTRAINT intent_atom_feeling CHECK (
        kind <> 'feeling' OR expires_at IS NOT NULL
    ),
    CONSTRAINT intent_atom_critique_human CHECK (
        kind <> 'critique_human' OR expires_at IS NULL
    )
);

COMMENT ON TABLE intent_atom IS
    '艦隊の intent/memory オーバーレイ。GitHub の LOCK コメント URL を法的・仕様の正本として置き換えない。';

CREATE INDEX intent_atom_tags_gin ON intent_atom USING GIN (tags);

CREATE OR REPLACE FUNCTION intent_atom_by_tags(
    requested text[],
    p_source text,
    p_now timestamptz
)
RETURNS SETOF intent_atom
LANGUAGE sql
STABLE
AS $$
    SELECT *
    FROM intent_atom
    WHERE source = p_source
      AND (expires_at IS NULL OR expires_at > p_now)
      AND tags @> requested;
$$;

CREATE OR REPLACE FUNCTION intent_atom_similar(
    query vector(1536),
    p_source text,
    p_limit integer,
    p_now timestamptz
)
RETURNS SETOF intent_atom
LANGUAGE sql
STABLE
AS $$
    SELECT *
    FROM intent_atom
    WHERE source = p_source
      AND (expires_at IS NULL OR expires_at > p_now)
      AND embedding IS NOT NULL
    ORDER BY embedding <=> query
    LIMIT p_limit;
$$;
