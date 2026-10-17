/*==============================================================
PLACEMENT ANALYTICS DASHBOARD SQL
Author: Abhishek Kumar Yadav
Project: Placement Analytics Dashboard
==============================================================*/


/*==============================================================
SECTION 1 : EXECUTIVE KPIs
==============================================================*/

-- Total Students
SELECT COUNT(*) AS total_students
FROM students;

---------------------------------------------------------------

-- Eligible Students
SELECT COUNT(*) AS eligible_students
FROM students
WHERE placement_status='Eligible';

---------------------------------------------------------------

-- Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

---------------------------------------------------------------

-- Total Placement Drives
SELECT COUNT(*) AS total_drives
FROM placement_drives;

---------------------------------------------------------------

-- Total Applications
SELECT COUNT(*) AS total_applications
FROM applications;

---------------------------------------------------------------

-- Total Interviews
SELECT COUNT(*) AS total_interviews
FROM interview_rounds;

---------------------------------------------------------------

-- Total Offers
SELECT COUNT(*) AS total_offers
FROM offers;

---------------------------------------------------------------

-- Students with Internship
SELECT COUNT(*) AS internship_students
FROM students
WHERE has_internship=TRUE;

---------------------------------------------------------------

-- Average CGPA
SELECT ROUND(AVG(cgpa),2) AS average_cgpa
FROM students;

---------------------------------------------------------------

-- Average Resume Score
SELECT ROUND(AVG(resume_score),2) AS avg_resume
FROM students;

---------------------------------------------------------------

-- Average Coding Score
SELECT ROUND(AVG(coding_score),2) AS avg_coding
FROM students;

---------------------------------------------------------------

-- Average Communication Score
SELECT ROUND(AVG(communication_score),2) AS avg_communication
FROM students;



/*==============================================================
SECTION 2 : BRANCH ANALYTICS
==============================================================*/

-- Students per Branch
SELECT
b.branch_name,
COUNT(*) AS students
FROM students s
JOIN branches b
ON s.branch_id=b.branch_id
GROUP BY b.branch_name
ORDER BY students DESC;

---------------------------------------------------------------

-- Average CGPA by Branch

SELECT
b.branch_name,
ROUND(AVG(cgpa),2) AS avg_cgpa
FROM students s
JOIN branches b
ON s.branch_id=b.branch_id
GROUP BY b.branch_name
ORDER BY avg_cgpa DESC;

---------------------------------------------------------------

-- Internship % by Branch

SELECT
b.branch_name,

ROUND(
100.0*
SUM(
CASE
WHEN has_internship THEN 1
ELSE 0
END
)
/COUNT(*)
,2)
AS internship_percentage

FROM students s
JOIN branches b
ON s.branch_id=b.branch_id

GROUP BY b.branch_name;

---------------------------------------------------------------

-- Average Resume Score

SELECT
b.branch_name,
ROUND(AVG(resume_score),2)
FROM students s
JOIN branches b
ON s.branch_id=b.branch_id
GROUP BY b.branch_name;

---------------------------------------------------------------

-- Average Coding Score

SELECT
b.branch_name,
ROUND(AVG(coding_score),2)
FROM students s
JOIN branches b
ON s.branch_id=b.branch_id
GROUP BY b.branch_name;

---------------------------------------------------------------

-- Average Communication Score

SELECT
b.branch_name,
ROUND(AVG(communication_score),2)
FROM students s
JOIN branches b
ON s.branch_id=b.branch_id
GROUP BY b.branch_name;



/*==============================================================
SECTION 3 : COMPANY ANALYTICS
==============================================================*/

-- Number of Drives

SELECT

c.company_name,

COUNT(*) AS drives

FROM placement_drives d

JOIN companies c

ON d.company_id=c.company_id

GROUP BY company_name

ORDER BY drives DESC;

---------------------------------------------------------------

-- Average CTC

SELECT

c.company_name,

ROUND(AVG(ctc),2) AS average_ctc

FROM placement_drives d

JOIN companies c

ON d.company_id=c.company_id

GROUP BY company_name

ORDER BY AVG(ctc) DESC;

---------------------------------------------------------------

-- Highest Package

SELECT

company_name,

MAX(ctc) AS highest_ctc

FROM placement_drives d

JOIN companies c

ON d.company_id=c.company_id

GROUP BY company_name

ORDER BY MAX(ctc) DESC;

---------------------------------------------------------------

-- Lowest Package

SELECT

company_name,

MIN(ctc) AS lowest_ctc

FROM placement_drives d

JOIN companies c

ON d.company_id=c.company_id

GROUP BY company_name;



/*==============================================================
SECTION 4 : APPLICATION ANALYTICS
==============================================================*/

-- Applications by Status

SELECT

application_status,

COUNT(*)

FROM applications

GROUP BY application_status;

---------------------------------------------------------------

-- Placement Rate: students with at least one offer / all students

SELECT
    ROUND(
        100.0 * COUNT(DISTINCT s.student_id)
            FILTER (WHERE o.offer_id IS NOT NULL)
            / NULLIF(COUNT(DISTINCT s.student_id), 0),
        2
    ) AS placement_rate_pct
FROM students s
LEFT JOIN applications a
    ON a.student_id = s.student_id
LEFT JOIN offers o
    ON o.application_id = a.application_id;

---------------------------------------------------------------

-- Application Conversion Rate: applications with an offer / all applications

SELECT
    ROUND(
        100.0 * COUNT(DISTINCT o.application_id)
            / NULLIF(COUNT(DISTINCT a.application_id), 0),
        2
    ) AS application_conversion_rate_pct
FROM applications a
LEFT JOIN offers o
    ON o.application_id = a.application_id;

---------------------------------------------------------------

-- Recruitment Funnel Counts

SELECT 'Applications' AS stage, COUNT(*) AS application_count
FROM applications
UNION ALL
SELECT 'Assessment cleared (OA score >= 70)', COUNT(*)
FROM applications
WHERE oa_score >= 70
UNION ALL
SELECT 'Reached interview', COUNT(DISTINCT application_id)
FROM interview_rounds
UNION ALL
SELECT 'Received offer', COUNT(DISTINCT application_id)
FROM offers;

---------------------------------------------------------------

-- Applications per Company

SELECT

c.company_name,

COUNT(*)

FROM applications a

JOIN placement_drives d

ON a.drive_id=d.drive_id

JOIN companies c

ON d.company_id=c.company_id

GROUP BY company_name

ORDER BY COUNT(*) DESC;



/*==============================================================
SECTION 5 : OFFER ANALYTICS
==============================================================*/

-- Accepted Offers

SELECT

accepted,

COUNT(*)

FROM offers

GROUP BY accepted;

---------------------------------------------------------------

-- Average Offered CTC

SELECT

ROUND(AVG(offered_ctc),2)

FROM offers;

---------------------------------------------------------------

-- Highest Offer

SELECT

MAX(offered_ctc)

FROM offers;

---------------------------------------------------------------

-- Lowest Offer

SELECT

MIN(offered_ctc)

FROM offers;



/*==============================================================
SECTION 6 : INTERVIEW ANALYTICS
==============================================================*/

-- Interview Result

SELECT

result,

COUNT(*)

FROM interview_rounds

GROUP BY result;

---------------------------------------------------------------

-- Interview Round Wise Count

SELECT

round_name,

COUNT(*)

FROM interview_rounds

GROUP BY round_name;



/*==============================================================
SECTION 7 : TOP PERFORMERS
==============================================================*/

-- Top 10 CGPA

SELECT

student_id,

cgpa

FROM students

ORDER BY cgpa DESC

LIMIT 10;

---------------------------------------------------------------

-- Top Resume Score

SELECT

student_id,

resume_score

FROM students

ORDER BY resume_score DESC

LIMIT 10;

---------------------------------------------------------------

-- Top Coding Score

SELECT

student_id,

coding_score

FROM students

ORDER BY coding_score DESC

LIMIT 10;

---------------------------------------------------------------

-- Top Communication Score

SELECT

student_id,

communication_score

FROM students

ORDER BY communication_score DESC

LIMIT 10;



/*==============================================================
SECTION 8 : ADVANCED SQL
==============================================================*/

-- Rank Students by CGPA

SELECT

student_id,

cgpa,

DENSE_RANK()

OVER(

ORDER BY cgpa DESC

)

AS rank

FROM students;

---------------------------------------------------------------

-- Running Average Package

SELECT

offer_id,

offered_ctc,

AVG(offered_ctc)

OVER(

ORDER BY offered_ctc

)

AS running_avg

FROM offers;

---------------------------------------------------------------

-- Company Package Rank

SELECT

company_name,

ctc,

RANK()

OVER(

ORDER BY ctc DESC

)

AS package_rank

FROM placement_drives d

JOIN companies c

ON d.company_id=c.company_id;

---------------------------------------------------------------

-- Students above Branch Average

WITH branch_avg AS

(

SELECT

branch_id,

AVG(cgpa) avg_cgpa

FROM students

GROUP BY branch_id

)

SELECT

s.student_id,

s.cgpa

FROM students s

JOIN branch_avg b

ON s.branch_id=b.branch_id

WHERE s.cgpa>b.avg_cgpa;

---------------------------------------------------------------

-- Branch Wise Placement Count

SELECT

b.branch_name,

COUNT(o.offer_id)

FROM students s

JOIN branches b

ON s.branch_id=b.branch_id

JOIN applications a

ON s.student_id=a.student_id

JOIN offers o

ON a.application_id=o.application_id

GROUP BY b.branch_name

ORDER BY COUNT(o.offer_id) DESC;