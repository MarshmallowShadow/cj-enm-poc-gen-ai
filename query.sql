id SERIAL PRIMARY KEY,
category VARCHAR(255),
title VARCHAR(255),
author VARCHAR(255),
publisher VARCHAR(255),
publication_date DATE,
work_category VARCHAR(255),
description TEXT,
author_info TEXT,
other_works TEXT,
isbn VARCHAR(20),
page_count INT,
awards TEXT,
original_title VARCHAR(255),
rating FLOAT, -- 평점 (예: 4.50)
rating_count INT, -- 평점자 수
md_recommended BOOLEAN -- MD 추천작 여부 (TRUE/FALSE)