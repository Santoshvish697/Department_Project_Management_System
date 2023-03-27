
USE DEPT_PROJECT;
-- SELECT 
--   TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
-- FROM
--   INFORMATION_SCHEMA.KEY_COLUMN_USAGE
-- WHERE
--   REFERENCED_TABLE_SCHEMA = 'DEPT_PROJECT' AND
--   REFERENCED_TABLE_NAME = 'GUIDE';
  
ALTER TABLE DELIVERABLE_PROJECT
DROP FOREIGN KEY deliverable_project_ibfk_2;

ALTER TABLE DELIVERABLE_PROJECT
ADD CONSTRAINT fk_student_project
FOREIGN KEY (USN) REFERENCES STUDENT(USN) ON DELETE CASCADE;

ALTER TABLE DELIVERABLE_PROJECT
DROP FOREIGN KEY fk_student_project;

ALTER TABLE DELIVERABLE_PROJECT
ADD CONSTRAINT fk_student_project
FOREIGN KEY (USN) REFERENCES STUDENT(USN) ON DELETE SET NULL;

ALTER TABLE guide
DROP foreign key guide_ibfk_1;

ALTER TABLE guide
ADD CONSTRAINT fk_guide_project
FOREIGN KEY (PROJECT_ID) REFERENCES deliverable_project(PROJECT_ID) ON DELETE SET NULL;

ALTER TABLE GUIDE
DROP FOREIGN KEY guide_ibfk_2;

ALTER TABLE guide
ADD CONSTRAINT fk_guide_usn
FOREIGN KEY (USN) REFERENCES STUDENT(USN) ON DELETE SET NULL;

ALTER TABLE PANEL_MEMBERS
DROP foreign key panel_members_ibfk_1;

ALTER TABLE PANEL_MEMBERS
ADD CONSTRAINT fk_panel_usn
FOREIGN KEY (USN) REFERENCES STUDENT(USN);

ALTER TABLE PANEL_MEMBERS
DROP FOREIGN KEY fk_panel_usn;

ALTER TABLE PANEL_MEMBERS 
ADD CONSTRAINT fk_panel_usn_1
FOREIGN KEY (USN) REFERENCES STUDENT(USN) ON DELETE SET NULL;