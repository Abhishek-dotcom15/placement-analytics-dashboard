-- PostgreSQL schema for the CSV datasets in data/.
-- Branch names are not present in the CSVs, so the checked-in branch IDs are
-- seeded as their own display labels.

CREATE TABLE branches (
    branch_id SMALLINT PRIMARY KEY,
    branch_name TEXT NOT NULL UNIQUE
);

INSERT INTO branches (branch_id, branch_name) VALUES
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5');

CREATE TABLE students (
    student_id TEXT PRIMARY KEY,
    branch_id SMALLINT NOT NULL REFERENCES branches (branch_id),
    cgpa NUMERIC(4, 2) NOT NULL,
    active_backlogs SMALLINT NOT NULL,
    has_internship BOOLEAN NOT NULL,
    gender TEXT NOT NULL,
    current_degree TEXT NOT NULL,
    internship_count SMALLINT NOT NULL,
    resume_score SMALLINT NOT NULL,
    coding_score SMALLINT NOT NULL,
    communication_score SMALLINT NOT NULL,
    placement_status TEXT NOT NULL,
    graduation_year SMALLINT NOT NULL
);

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL,
    company_type TEXT NOT NULL,
    headquarters TEXT NOT NULL,
    website TEXT NOT NULL,
    returning_company BOOLEAN NOT NULL
);

CREATE TABLE placement_drives (
    drive_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies (company_id),
    role TEXT NOT NULL,
    hiring_type TEXT NOT NULL,
    ctc NUMERIC(5, 2) NOT NULL,
    minimum_cgpa NUMERIC(3, 2) NOT NULL,
    location TEXT NOT NULL,
    drive_date DATE NOT NULL
);

CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students (student_id),
    drive_id INTEGER NOT NULL REFERENCES placement_drives (drive_id),
    application_date DATE NOT NULL,
    application_status TEXT NOT NULL,
    oa_score SMALLINT
);

CREATE TABLE interview_rounds (
    round_id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL REFERENCES applications (application_id),
    round_name TEXT NOT NULL,
    round_date DATE NOT NULL,
    result TEXT NOT NULL
);

CREATE TABLE offers (
    offer_id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL REFERENCES applications (application_id),
    offered_ctc NUMERIC(5, 2) NOT NULL,
    offer_date DATE NOT NULL,
    accepted BOOLEAN NOT NULL
);
