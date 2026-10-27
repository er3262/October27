CREATE TYPE school_year_enum AS ENUM ('Sophomore', 'Junior', 'Senior');
CREATE TYPE intro_programming_enum AS ENUM ('took_it', 'equivalent', 'neither');

CREATE TABLE students (
    netid VARCHAR(32) PRIMARY KEY,
    name TEXT NOT NULL,
    school_year school_year_enum NOT NULL
);

CREATE TABLE survey_responses (
    response_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    netid VARCHAR(32) NOT NULL UNIQUE REFERENCES students (netid) ON DELETE CASCADE,
    intro_programming intro_programming_enum NOT NULL,
    skill_programming SMALLINT NOT NULL CHECK (skill_programming BETWEEN 1 AND 5),
    skill_data_stats SMALLINT NOT NULL CHECK (skill_data_stats BETWEEN 1 AND 5),
    skill_frontend_design SMALLINT NOT NULL CHECK (skill_frontend_design BETWEEN 1 AND 5),
    skill_business_pitch SMALLINT NOT NULL CHECK (skill_business_pitch BETWEEN 1 AND 5),
    working_style TEXT NOT NULL,
    interests TEXT NOT NULL,
    semester_goal TEXT NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE tools (
    tool_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tool_name TEXT NOT NULL UNIQUE
);

CREATE TABLE student_tools (
    netid VARCHAR(32) NOT NULL REFERENCES students (netid) ON DELETE CASCADE,
    tool_id INTEGER NOT NULL REFERENCES tools (tool_id) ON DELETE CASCADE,
    PRIMARY KEY (netid, tool_id)
);

CREATE TABLE availability_slots (
    slot_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slot_name TEXT NOT NULL UNIQUE
);

CREATE TABLE student_availability (
    netid VARCHAR(32) NOT NULL REFERENCES students (netid) ON DELETE CASCADE,
    slot_id INTEGER NOT NULL REFERENCES availability_slots (slot_id) ON DELETE CASCADE,
    PRIMARY KEY (netid, slot_id)
);

INSERT INTO tools (tool_name) VALUES
    ('Python'),
    ('SQL'),
    ('Excel'),
    ('JavaScript'),
    ('R'),
    ('none yet');

INSERT INTO availability_slots (slot_name) VALUES
    ('Weekday mornings'),
    ('Weekday afternoons'),
    ('Weekday evenings'),
    ('Weekend mornings'),
    ('Weekend afternoons'),
    ('Weekend evenings');
