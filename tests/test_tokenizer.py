from docarchive.tokenizer import tokenize, STOPWORDS


def test_lowercase_and_split():
    assert tokenize("Hello, WORLD!") == ["hello", "world"]


def test_stopwords_removed():
    toks = tokenize("the grid and the reserves")
    assert "the" not in toks
    assert "and" not in toks
    assert "grid" in toks and "reserves" in toks


def test_keep_stopwords_flag():
    toks = tokenize("the grid", keep_stopwords=True)
    assert "the" in toks


def test_min_length_drops_single_char():
    assert "x" not in tokenize("x ray")
    assert "ray" in tokenize("x ray")


def test_hyphenated_token_preserved():
    assert "supply-chain" in tokenize("supply-chain fragility")


def test_stopword_list_is_lowercase():
    assert all(w == w.lower() for w in STOPWORDS)
